import pandas as pd


class DataUtilities:

    def transformCsvToPandasDf(csvFile):
        return pd.read_csv(csvFile, index_col=False)
