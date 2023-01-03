from Parser.Base import Base


class Hdfc(Base):
    def __init__(self,filepath):
        super().__init__(filepath)

    def get_parsed_frame(self):
        for each in self.df_list:
            self.df = self.df.append(each)
        self.df.reset_index(drop=True, inplace=True)
        self.df.columns = self.df.iloc[0]
        self.df = self.df[1:]
        index_lst = self.df.index[self.df['Narration'].str.contains("STATEMENT SUMMARY")].tolist()
        if index_lst:
            self.df = self.df.iloc[:index_lst[-1] - 1, :]
        date_indexes = self.df[self.df['Date'].notnull()].index.tolist()
        print(self.df.columns)
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

obj = Hdfc(r"C:\Users\AbdulRashid\Desktop\BlessedTree\AutoCountApi\media\pdfs\sampleOut2.pdf")
obj.parse_statement()