from Parser.Base import Base
import pandas as pd
from datetime import datetime
from statement.models import Statement,StatementUpload
class Hdfc(Base):

    def __init__(self,filepath):
        super().__init__(filepath)


    def check_date_range(self,date):
        for each in self.ranges:
            start = each[0]
            end = each[1]
            if start <= date <= end:
                return True
        else:
            return False

    def get_parsed_frame(self,bank_obj,stat_bank_upl_obj):
        for each in self.df_list:
            self.df = self.df.append(each)
        self.df.reset_index(drop=True, inplace=True)
        self.df.columns = self.df.iloc[0]
        self.df = self.df[1:]
        index_lst = self.df.index[self.df['Narration'].str.contains("STATEMENT SUMMARY")].tolist()
        if index_lst:
            self.df = self.df.iloc[:index_lst[-1] - 1, :]
        date_indexes = self.df[self.df['Date'].notnull()].index.tolist()
        for index, each in enumerate(date_indexes):
            if index == len(date_indexes) - 1:
                string = ''.join(self.df.loc[each:self.df.index[-1]].Narration)
                # print(self.df.loc[self.df.index[-1]])
                self.df["Narration"][each] = string
            else:
                string = ''.join(self.df.loc[each:date_indexes[index + 1] - 1].Narration)
                self.df["Narration"][each] = string
        df1 = self.df[self.df['Date'].notna()]
        df1.reset_index(drop=True, inplace=True)
        frame = df1.where(pd.notnull(df1), None)
        rows_statements = []
        startDate,endDate = None,None
        for index, row in frame.iterrows():
            date, description, reference, debit, credit = (
            row['Date'], row['Narration'], row['Chq./Ref.No.'], row['Withdrawal Amt.'], row['Deposit Amt.'])
            d = datetime.strptime(date, "%d/%m/%y")
            date = d.strftime("%Y-%m-%d")
            if not self.check_date_range(date):
                if credit is None:
                    credit = 0
                else:
                    credit = credit.replace(",", "")
                    credit = float(credit)
                if debit is None:
                    debit = 0
                else:
                    debit = debit.replace(",", "")
                    debit = float(debit)
                balance = debit if debit else credit
                stat = Statement(bank=bank_obj,statementUpload=stat_bank_upl_obj, date=date, description=description, reference=reference, credit=credit,
                                 debit=debit,
                                 balance=balance)
                rows_statements.append(stat)
            if index == 0:
                startDate = date
            else:
                endDate = date

        return rows_statements,startDate,endDate

