
import pandas as pd
from statement.models import StatementUpload
from datetime import datetime

class Base:
    GLOBAL_DATE_FORMAT = "%Y-%m-%d"

    def __init__(self):
        objs = StatementUpload.objects.filter(bank__name=self.__class__.__name__)
        self.ranges = []
        for each in objs:
            if each.startDate and each.endDate:
                self.ranges.append([str(each.startDate), str(each.endDate)])
        print(self.ranges)
        #
        self.df = pd.DataFrame()

    def convert_date_format(self,date):
        d = datetime.strptime(date, self.DATE_FORMAT)
        date = d.strftime(self.GLOBAL_DATE_FORMAT)
        return date

    def check_date_range(self,date):
        for each in self.ranges:
            start = each[0]
            end = each[1]
            if start <= date <= end:
                return True
        else:
            return False

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
            print(e)
            errorMessage = str(e)
            stat_bank_upl_obj.errorMessage = errorMessage
            stat_bank_upl_obj.error = True
        stat_bank_upl_obj.save()
        return rows_statements