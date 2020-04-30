# Name:                                            Renacin Matadeen
# Date:                                               04/05/2020
# Title                                    2016 Canadian Census Data Parsing
#
# ----------------------------------------------------------------------------------------------------------------------
import csv
import pandas as pd
import numpy as np
import time
# ----------------------------------------------------------------------------------------------------------------------

"""
Open The CSV, and Pull Information You Need
"""
def parse_toronto_csv(in_path, out_path):
    temp_df = pd.DataFrame()

    # [1.] File Is Too Large To Hold In Memory, Read In 1'000'000 Line Chunks
    chunksize = 10 ** 6

    # [2.] Filter Geo Polygons Based On GEO_NAME, Append To New DF
    counter = 1
    for chunk in pd.read_csv(in_path, chunksize=chunksize):

        chunk = chunk[pd.to_numeric(chunk['GEO_NAME'], errors='coerce').notnull()]
        chunk['GEO_NAME'] = chunk['GEO_NAME'].astype(int)

        temp_focus_df = chunk[chunk["GEO_NAME"].between(35200000, 35205000)] # CoT DAs

        frames = [temp_df, temp_focus_df]
        temp_df = pd.concat(frames)

        print("Progress: Chunk {}/47".format(counter)) # Write To A CSV, This Takes Up Too Much Memory
        counter += 1

    # [3.] Write To CSV, Don't Repeat Intensive Processes
    temp_df.to_csv(out_path, index=False)


"""
Only Keep A Few Columns
"""
def clean_data(in_path, out_path):
    tc_data = pd.read_csv(in_path)

    # [1.] Remove Unneeded Columns
    tc_data = tc_data.drop(columns=["CENSUS_YEAR", "GEO_LEVEL", "GEO_CODE (POR)", "GNR", "GNR_LF",
                                    "DATA_QUALITY_FLAG", "ALT_GEO_CODE",  "Notes: Profile of Dissemination Areas (2247)",
                                    "Dim: Sex (3): Member ID: [2]: Male", "Dim: Sex (3): Member ID: [3]: Female"])

    # [2.] Rename Columns
    tc_data = tc_data.rename(columns={"GEO_NAME": "DA_ID", "DIM: Profile of Dissemination Areas (2247)": "Column",
                                      "Member ID: Profile of Dissemination Areas (2247)": "ColumnID",
                                      "Dim: Sex (3): Member ID: [1]: Total - Sex": "Count"})

    # [3.] Export Data
    tc_data.to_csv(out_path, index=False)
    print(tc_data.info())


"""
Reorganize Data So Accesible By GIS
"""
def reorg_df(in_path, out_path):
    tc_data = pd.read_csv(in_path)

    # [1.] Grab Names For Columns
    unq_census_fields = list(tc_data["Column"][0:2247])

    columns_list = []
    for idx, field in enumerate(unq_census_fields):
        toreplace = [" ", "_", ",", "-", "..."]
        for char in toreplace:
            field = field.replace(char, "")

        columns_list.append(str(idx + 1) + "_" + field)

    # [2.] Get Unique Values DA_IDs, And Create A DA_ID Column
    unq_da = list(tc_data["DA_ID"].unique())

    # [3.] Create a List of Lists To Store Data For Each Row
    rows_list = []
    start_idx = 0
    end_idx = 2247

    for idx, da in enumerate(unq_da):
        idx += 1

        # Increase Index To Accomodate
        if idx != 1:
            start_idx += 2247
            end_idx += 2247

        rows_list.append(list(tc_data["Count"][start_idx:end_idx]))

    # [4.] Create a new DF with data
    cleaned_df = pd.DataFrame(rows_list, columns = columns_list)

    # [5.] First Row Needs DA_IDs
    cleaned_df.insert(loc=0, column="DA_ID", value=unq_da)
    cleaned_df.to_csv(out_path, index=False)


"""
Fill In Missing Data | Which Methodology Works Best?
1). Mean, Median, or Mode | Median Best Of Three, But Still Not As Accurate
2). Nearest neighbour Fill?

THINGS TO DO:
    + How Do I beat Random Rounding?
        - Create a neural network that can predict counts based on other fields
        - DO NOT USE NaN counts
"""
def fill_df(in_path, out_path):
    df = pd.read_csv(in_path, low_memory=False)

    # [1.] Convert All Non-Numeric Values To Nan
    df = df.convert_objects(convert_numeric=True)
    df = df.replace('...', np.NaN)

    # [2.] Loop Through Each Column And Fill Nan With Column Average
    column_names = list(df.columns.values)

    for field_name in column_names:

        if field_name != "DA_ID":
            column_average = round(df[field_name].median(), 2)
            df[field_name] = df[field_name].fillna(column_average)
            del column_average

    # [3.] Export Data
    df.to_csv(out_path, index=False)


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # parse_toronto_csv(r"D:\Data\CanadianCensus\2016\RawData\Census_2016_RawData.csv",
    #                   r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Data\Step_1_CensusData.csv")
    #
    # clean_data(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Data\Step_1_CensusData.csv",
    #            r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Data\Step_2_CensusData.csv")
    #
    # reorg_df(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Data\Step_2_CensusData.csv",
    #          r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Data\Step_3_CensusData.csv")

    fill_df(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Data\Step_3_CensusData.csv",
             r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Data\Step_4_CensusData.csv")
