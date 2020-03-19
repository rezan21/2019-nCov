import schedule
import time

def repeat():
    import pandas as pd
    import pycountry
    
    confrmd_df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
    recovrd_df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")
    deaths_df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
    
    def renameCountries(confrmd_df=confrmd_df,recovrd_df=recovrd_df,deaths_df=deaths_df):
        con_rec_deaths = [confrmd_df,recovrd_df,deaths_df]
        for df in con_rec_deaths:
            df["Country/Region"].replace(
                [ 
                    "Macau",
                    "Russia",
                    "South Korea", 
                    "Taiwan", 
                    "UK",
                    "US",
                    "Vietnam",
                    "Iran",
                    " Azerbaijan",
                    "North Ireland",
                    "Czech Republic",
                    "Bolivia",
                    "Brunei",
                    "Congo (Kinshasa)",
                    "Congo (Brazzaville)",
                    "Cote d'Ivoire",
                    "Gambia, The",
                    "Korea, South",
                    "Moldova",
                    "Republic of the Congo",
                    "Taiwan*",
                    "Tanzania",
                    "The Bahamas",
                    "The Gambia",
                    "Venezuela",
                ],
                [
                    "Macao",
                    "Russian Federation",
                    "Korea, Republic of",
                    "Taiwan, Province of China",
                    "United Kingdom",
                    "United States",
                    "Viet Nam",
                    "Iran, Islamic Republic of",
                    "Azerbaijan",
                    "United Kingdom",
                    "Czechia",
                    "Bolivia, Plurinational State of",
                    "Brunei Darussalam",
                    "Congo, The Democratic Republic of the",
                    "Congo",
                    "Côte d'Ivoire",
                    "Gambia",
                    "Korea, Republic of",
                    "Moldova, Republic of",
                    "Congo",
                    "Taiwan, Province of China",
                    "Tanzania, United Republic of",
                    "Bahamas",
                    "Gambia",
                    "Venezuela, Bolivarian Republic of",
                    
                    ], inplace=True)
    renameCountries()


    def create_map_df(df):
        df = df.groupby("Country/Region").sum()
        df.reset_index(inplace=True) # get country as col

        df.drop(["Lat","Long"], axis=1, inplace=True)

        sec2_df = df.iloc[:,1:] # 2nd section containing only cases counts

        sec1_df = pd.DataFrame(df.iloc[:,0]) # 1st section containing location data
        def getCountryCode(x):
            # get alph3 encoding to match plotly standard
            try:
                c = pycountry.countries.get(name=x)
                return c.alpha_3
            except Exception as e:
                print(x)
                print(e)
                pass

        sec1_df["Country_Code"] = sec1_df["Country/Region"].apply(getCountryCode)
        sec1_df.columns = ["Country", "Country_Code"]
        df = pd.concat([sec1_df, sec2_df],axis=1) # concat back two sections

        df.dropna(axis=0, inplace=True)
        df.reset_index(inplace=True, drop=True)

        # melt (i.e: wide to long function)
        df = pd.melt(df, id_vars=["Country","Country_Code"],var_name="Time_Stamp", value_name="Cases")

        # save generated df
        df.to_csv("../app/app_data/frame_animation_df.csv",index=False)
    create_map_df(confrmd_df)

    def prepare_general_df(confrmd_df=confrmd_df, recovrd_df=recovrd_df, deaths_df=deaths_df):
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
        df.to_csv("../app/app_data/general_df.csv",index=False)
        return df
    general_df = prepare_general_df()

    def prepare_grouped_death_recov_df():
        # local processing
        df = general_df
        df = [df.groupby("Country/Region").get_group(country).sort_values("timestamp", ascending=False).\
        iloc[0] for country in df["Country/Region"].unique()]
        df = pd.DataFrame(df)
        df.to_csv("../app/app_data/df_grouped.csv",index=False) # export

        df["death_rate"] = df["death_cases"] / df["conf_cases"]
        df["recover_rate"] = df["recov_cases"] / df["conf_cases"]

        df_death  = df[df["death_rate"]>0]
        df_recov  = df[df["recover_rate"]>0]

        df_death = df_death.sort_values("death_rate",ascending=False)
        df_recov = df_recov.sort_values("recover_rate",ascending=False)


        df_death.to_csv("../app/app_data/df_death.csv",index=False) # export
        df_recov.to_csv("../app/app_data/df_recov.csv",index=False) # export
    prepare_grouped_death_recov_df()    
   
schedule.every(1).seconds.do(repeat)
while True:
    schedule.run_pending()
    time.sleep(2)


 # Cloud Implementation Note:
    # Can NOT write file to the disk on GCP-Standard enviroment.
    # The following is a solution to write files to temporary folder and create folders withing that:
    # import os
    # os.system(f"mkdir /tmp/myfolder")
    # confrmd_df.to_csv("/tmp/myfolder/frame_animation_df.csv",index=False)


