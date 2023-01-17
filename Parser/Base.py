import tabula
import pandas as pd
from statement.models import StatementUpload

class Base:
    def __init__(self,filepath):
        objs = StatementUpload.objects.filter(bank__name=self.__class__.__name__)
        self.ranges = []
        for each in objs:
            if each.startDate and each.endDate:
                self.ranges.append([str(each.startDate), str(each.endDate)])
        print(self.ranges)
        try:
            self.df_list = tabula.read_pdf(filepath, stream=True, guess=True, pages='all',
                                      multiple_tables=True,
                                      pandas_options={
                                          'header': None}
                                      )
            print(type(self.df_list))
        except Exception as e:
            print('The Error is', e)
        self.df = pd.DataFrame()


    def parse_statement(self,bank_obj,stat_bank_upl_obj):
        rows_statements = []
        try:
            rows_statements,startDate,endDate =  self.get_parsed_frame(bank_obj,stat_bank_upl_obj)
            stat_bank_upl_obj.parse = True
            if not StatementUpload.objects.filter(startDate=startDate,endDate=endDate):
                stat_bank_upl_obj.startDate = startDate
                stat_bank_upl_obj.endDate = endDate
            else:
                stat_bank_upl_obj.errorMessage = "File already uploaded"
                stat_bank_upl_obj.error = True
        except Exception as e:
            errorMessage = str(e)
            stat_bank_upl_obj.errorMessage = errorMessage
            stat_bank_upl_obj.error = True
        stat_bank_upl_obj.save()
        return rows_statements