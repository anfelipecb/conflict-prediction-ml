import os
import pandas as pd


def files_not_hidden_and_countries(path):
    """
    Return list of files not hidden from a directory
    Input:
        - path to directory: str
    Return:
        - list with not hidden files: list
    """
    elements = os.listdir(path)
    elements = list(item for item in elements if not item.startswith("."))
    countries = set(elem[:3] for elem in elements)
    return countries, elements

def concatenates_df(df1: pd.DataFrame, df2: pd.DataFrame):
    """ Returns a concatenated df when have same columns
    Input:
        df1: pd.Dataframe
        df2: pd.Dataframe
    Return:
        pd.Dataframe
    """
    dfs = [df1, df2]
    return pd.concat(dfs, axis= 0, join="inner")

africa_countries= set([
    'DZA', 'AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CMR', 'CPV', 'CAF', 'TCD',
    'COM', 'COG', 'CIV', 'DJI', 'EGY', 'GNQ', 'ERI', 'SWZ', 'ETH', 'GAB',
    'GMB', 'GHA', 'GIN', 'GNB', 'KEN', 'LSO', 'LBR', 'LBY', 'MDG', 'MWI',
    'MLI', 'MRT', 'MUS', 'MYT', 'MAR', 'MOZ', 'NAM', 'NER', 'NGA', 'REU',
    'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'SOM', 'ZAF', 'SSD', 'SDN', 'TZA',
    'TGO', 'TUN', 'UGA', 'ESH', 'ZMB', 'ZWE'])

def main():
    """
    Writes a csv with all the data from the Africa countries, ignoring others
    """
    repo_path = "Wealth Index/"
    countries, all_csv = files_not_hidden_and_countries(repo_path)
    countries_to_review = set.intersection(countries, africa_countries)
    df = None
    counter = 0
    for csv in all_csv:
        country = csv[0:3]
        if not isinstance(df, pd.DataFrame):
            if country in countries_to_review:
                df = pd.read_csv(repo_path + csv)
                df["country"] = country
                counter += 1
        else:
            if country in countries_to_review:
                csv_path = repo_path + csv
                csv_df = pd.read_csv(csv_path)
                csv_df["country"] = country
                df = concatenates_df(df, csv_df)
                counter += 1
    print(f"countries added: {counter}")
    df.to_csv("data/extracted/wealth_index_africa.csv", index=False)
    

if __name__ == "__main__":
    main()