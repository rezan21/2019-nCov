import pandas as pd
import numpy as np
import pycountry

confrmd_df = pd.read_csv("./data/time_series_2019_ncov_confirmed.csv")
recovrd_df = pd.read_csv("./data/time_series_2019_ncov_recovered.csv")
deaths_df = pd.read_csv("./data/time_series_2019_ncov_deaths.csv")

def prepare_dfCnfrmd(confrmd_df=confrmd_df):
    confrmd_df = confrmd_df.groupby("Country/Region").sum()
    confrmd_df.reset_index(inplace=True) # get country as col
    confrmd_df["Country/Region"].replace([ # rename to match pycountry standard
                                        "Macau",
                                        "Russia",
                                        "South Korea", 
                                        "Taiwan", 
                                        "UK",
                                        "US",
                                        "Vietnam"
                                        ],
                                        [
                                        "Macao",
                                        "Russian Federation",
                                        "Korea, Republic of",
                                        "Taiwan, Province of China",
                                        "United Kingdom",
                                        "United States",
                                        "Viet Nam"
                                        
                                        ], inplace=True)

    confrmd_df.drop(["Lat","Long"], axis=1, inplace=True)

    sec2_confrmd_df = confrmd_df.iloc[:,1:] # 2nd section containing only confirmed counts

    sec1_confrmd_df = pd.DataFrame(confrmd_df.iloc[:,0]) # 1st section containing location data
    def getCountryCode(x):
        # get alph3 encoding to match plotly standard
        try:
            c = pycountry.countries.get(name=x)
            return c.alpha_3
        except:
            pass
        
    sec1_confrmd_df["Country_Code"] = sec1_confrmd_df["Country/Region"].apply(getCountryCode)
    sec1_confrmd_df.columns = ["Country", "Country_Code"]
    confrmd_df = pd.concat([sec1_confrmd_df, sec2_confrmd_df],axis=1) # concat back two sections

    confrmd_df.dropna(axis=0, inplace=True)
    confrmd_df.reset_index(inplace=True, drop=True)

    # melt (i.e: wide to long function)
    import os
    confrmd_df = pd.melt(confrmd_df, id_vars=["Country","Country_Code"],var_name="Time_Stamp", value_name="Cases")
    os.system(f"mkdir /tmp/myfolder")
    confrmd_df.to_csv("/tmp/myfolder/frame_animation_df.csv",index=False)

prepare_dfCnfrmd()


def prepare_general_df(confrmd_df=confrmd_df,recovrd_df=recovrd_df,deaths_df=deaths_df):
    confrmd_df.drop(["Province/State","Lat","Long"], axis=1, inplace=True)
    recovrd_df.drop(["Province/State","Lat","Long"], axis=1, inplace=True)
    deaths_df.drop(["Province/State","Lat","Long"], axis=1, inplace=True)

    confrmd_df = confrmd_df.groupby("Country/Region").sum().reset_index()
    recovrd_df = recovrd_df.groupby("Country/Region").sum().reset_index()
    deaths_df = deaths_df.groupby("Country/Region").sum().reset_index()

    confrmd_df = confrmd_df.melt(id_vars=["Country/Region"], var_name="timestamp", value_name="cases")
    recovrd_df = recovrd_df.melt(id_vars=["Country/Region"], var_name="timestamp", value_name="cases")
    deaths_df = deaths_df.melt(id_vars=["Country/Region"], var_name="timestamp", value_name="cases")

    confrmd_df.rename(columns={"cases": "conf_cases"},inplace=True)
    recovrd_df.rename(columns={"cases": "recov_cases"},inplace=True)
    deaths_df.rename(columns={"cases": "death_cases"},inplace=True)

    df = pd.concat([confrmd_df,recovrd_df.iloc[:,2],deaths_df.iloc[:,2]], axis=1)

    df["timestamp"] = pd.to_datetime(df["timestamp"])


prepare_general_df()