from Parser.Base import Base
import pdfplumber
import pandas as pd
import tabula
from pprint import pprint
from statement.models import Statement


class Maharashtra(Base):
    DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, filepath):
        super().__init__()
        self.df_list = []
        with pdfplumber.open(filepath) as pdf:
            first_page = pdf.pages[0]
            table = first_page.extract_tables()
            table = table[1][1:]
            columns = [each.replace("\n","") for each in table[0]]
            print(columns)
            df = pd.DataFrame(table[1:], columns=columns)
            df.replace(to_replace='\n', value=' ', inplace=True, limit=None, regex=True, method='pad')
            self.df_list.append(df)
        try:
            df_list = tabula.read_pdf(filepath, multiple_tables=True, pages='all')
            for each in df_list[2:-1]:
                df_data = each.iloc[1:, :]
                df_data.columns = columns
                self.df_list.append(df_data)
            print(type(self.df_list))
        except Exception as e:
            print('The Error is', e)


    def get_parsed_frame(self, bank_obj=None, stat_bank_upl_obj=None):
        for each in self.df_list:
            self.df = self.df.append(each)
        df1 = self.df[self.df['Date'].notna()]
        df1.reset_index(drop=True, inplace=True)
        frame = df1.where(pd.notnull(df1), None)
        rows_statements = []
        startDate, endDate = None, None
        for index, row in frame.iterrows():
            date, description, reference, debit, credit = (
                row['Date'], row['Particulars'], row['Cheque/Reference No'], row['Debit'], row['Credit'])
            date = self.convert_date_format(date)
            if not self.check_date_range(date):
                if not credit or credit is None:
                    credit = 0
                else:
                    credit = credit.replace(",", "")
                    credit = float(credit)
                if not debit or debit is None:
                    debit = 0
                else:
                    debit = debit.replace(",", "")
                    debit = float(debit)
                balance = debit if debit else credit
                stat = Statement(bank=bank_obj, statementUpload=stat_bank_upl_obj, date=date, description=description,
                                 reference=reference, credit=credit,
                                 debit=debit,
                                 balance=balance)
                rows_statements.append(stat)
            if index == 0:
                startDate = date
            else:
                endDate = date
        return rows_statements, startDate, endDate
#         print("HERE")
# obj = Maharashtra(r"C:\Users\AbdulRashid\Desktop\BlessedTree\jupyter notebook\sample_mh.pdf")
# obj.get_parsed_frame()