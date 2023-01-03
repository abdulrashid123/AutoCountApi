import tabula
import pandas as pd


class Base:
    def __init__(self,filepath):
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


    def parse_statement(self):
        self.get_parsed_frame()