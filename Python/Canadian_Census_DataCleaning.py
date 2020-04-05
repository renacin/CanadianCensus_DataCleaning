# Name:                                            Renacin Matadeen
# Date:                                               04/05/2020
# Title                                    2016 Canadian Census Data Parsing
#
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
from os import listdir
# ----------------------------------------------------------------------------------------------------------------------

# Open The CSV, and Pull Information You Need
def parse_toronto_csv(in_path, out_path):
    raw_census_data = pd.read_csv(in_path)
    da_census_data = raw_census_data[raw_census_data["GEO_CODE (POR)"].between(35200000, 35205000)] # City Of Toronto
    da_census_data.to_csv(out_path)

# Keep Only A Few Columns
def clean_data(in_path, out_path):
    tc_data = pd.read_csv(in_path)

    tc_data = tc_data.drop(columns=["Unnamed: 0", "CENSUS_YEAR", "GEO_LEVEL", "GEO_NAME", "GNR", "GNR_LF",
                                    "DATA_QUALITY_FLAG", "ALT_GEO_CODE",  "Notes: Profile of Dissemination Areas (2247)",
                                    "Dim: Sex (3): Member ID: [2]: Male", "Dim: Sex (3): Member ID: [3]: Female"])

    tc_data.to_csv(out_path)
    print(tc_data.info())

# Reorganize Data So Easily Accessible By GIS | Transpose Data!
def reorg_df(in_path, out_path):
    tc_data = pd.read_csv(in_path)

    # Get Unique Values




# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # parse_toronto_csv(r"C:\Users\renac\Documents\Programming\Python\CanadianCensusExploration\Data\Census_2016_RawData.csv",
    #           r"C:\Users\renac\Documents\Programming\Python\CanadianCensusExploration\Data\TorontoDa_2016_Data.csv")

    # clean_data(r"C:\Users\renac\Documents\Programming\Python\CanadianCensusExploration\Data\TorontoDa_2016_Data.csv",
    #            r"C:\Users\renac\Documents\Programming\Python\CanadianCensusExploration\Data\T_DA_Census2016_Data.csv")

    reorg_df(r"C:\Users\renac\Documents\Programming\Python\CanadianCensusExploration\Data\Test_Data.csv")
