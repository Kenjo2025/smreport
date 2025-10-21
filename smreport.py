import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import altair as alt
from google.cloud import bigquery
from matplotlib.colors import LinearSegmentedColormap
#import seaborn as sns

#conn = st.connection("gsheets", type=GSheetsConnection)
#df = conn.read(worksheet="data")

color1 = [ "#e6ffff", "#00cccc", "#009999"  ]
color_map1 = LinearSegmentedColormap.from_list("my_cmap", color1)

color2 = [ "#f7e6ff", "#ff99ff", "#e60099"  ]
color_map2 = LinearSegmentedColormap.from_list("my_cmap", color2)

color3 = [ "#e6ffff", "#ffffff", "#ffe6f2"  ]
color_map3 = LinearSegmentedColormap.from_list("my_cmap", color3)

client = bigquery.Client.from_service_account_json("pipeline-looker-3ccfc32b2780.json")

df = client.query("SELECT * FROM `pipeline-looker.pythonpl.sm` where Topic_Clean <> '-'").to_dataframe()
    
st.set_page_config(layout="wide")

#df=pd.read_csv("smreport.csv")

#df_combined.rename(columns= {"facebook reach":"FB Reach", "ig reach":"IG Reach"})

df["index"] = range(1,len(df) +1)
df.rename(columns= {"Date_Clean":"Date" , "Topic_Clean" : "Topic", "title":"Title"}, inplace=True)

df["FB Followers"] = df["facebook_followers"].astype(float)
df["FB Views"] = df["facebook_views"].astype(float)
df["FB Reach"] = df["facebook_reach"].astype(float)
df["FB Like"] = df["facebook_like"].astype(float)
df["FB Share"] = df["facebook_share"].astype(float)
df["FB Comments"] = df["facebook_comments"].astype(float)
df["IG Followers"] = df["ig_followers"].astype(float)
df["IG Viewers"] = df["ig_viewers"].astype(float)
df["IG Reach"] = df["ig_reach"].astype(float)
df["IG Like"] = df["ig_like"].astype(float)
df["IG Comments"] = df["ig_comments"].astype(float)
df["IG Share"] = df["ig_share"].astype(float)
df["IG Save"] = df["ig_save"].astype(float)

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df["group"] = "sm"
df.rename(columns= {"facebook reach":"FB Reach", "ig reach":"IG Reach"})

#---------------------------------------------------------------------------------

min_date = df["Date"].min()
max_date = df["Date"].max()
date_range = st.date_input("Select Date Range", [min_date, max_date])

if len(date_range) == 2:
    start_date, end_date = date_range
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
    df_f = df[mask]

    x = end_date - start_date
    prev_start = start_date - x
    prev_end = start_date
    mask3 = (df["Date"] >= prev_start) & (df["Date"] <= prev_end)
    df_f2 = df[mask3]

else:
    mask = pd.Series(True, index=df.index)
    df_f = df[mask]
    df_f2 = df[mask]

#---------------------------------------------------------------------------------

df_displayfb = df_f.groupby(["index", "Topic", "Date", "Title"]).agg(**{
    "FB Followers": ("FB Followers", "sum"),
    "FB Views": ("FB Views", "sum"),
    "FB Reach": ("FB Reach", "sum"),
    "FB Like": ("FB Like", "sum"),
    "FB Comments": ("FB Comments", "sum"),
    "FB Share": ("FB Share", "sum")
})

df_displayig = df_f.groupby(["index", "Topic", "Date", "Title"]).agg(**{
    "IG Followers": ("IG Followers", "sum"),
    "IG Viewers": ("IG Viewers", "sum"),
    "IG Reach": ("IG Reach", "sum"),
    "IG Like": ("IG Like", "sum"),
    "IG Comments": ("IG Comments", "sum"),
    "IG Share": ("IG Share", "sum"),
    "IG Save": ("IG Save", "sum")
})

df_display2 = df_f.groupby("group", as_index=False).agg(**{
    "FB Followers": ("FB Followers", "mean"),
    "FB Views": ("FB Views", "sum"),
    "FB Reach": ("FB Reach", "sum"),
    "FB Like": ("FB Like", "sum"),
    "FB Comments": ("FB Comments", "sum"),
    "FB Share": ("FB Share", "sum")
})


df_display3 = df_f.groupby("group", as_index=False).agg(**{
    "IG Followers": ("IG Followers", "mean"),
    "IG Viewers": ("IG Viewers", "sum"),
    "IG Reach": ("IG Reach", "sum"),
    "IG Like": ("IG Like", "sum"),
    "IG Comments": ("IG Comments", "sum"),
    "IG Share": ("IG Share", "sum"),
    "IG Save": ("IG Save", "sum")
})

df_display4 = df_f2.groupby("group", as_index=False).agg(**{
    "FB Followers": ("FB Followers", "mean"),
    "FB Views": ("FB Views", "sum"),
    "FB Reach": ("FB Reach", "sum"),
    "FB Like": ("FB Like", "sum"),
    "FB Comments": ("FB Comments", "sum"),
    "FB Share": ("FB Share", "sum")
})


df_display5 = df_f2.groupby("group", as_index=False).agg(**{
    "IG Followers": ("IG Followers", "mean"),
    "IG Viewers": ("IG Viewers", "sum"),
    "IG Reach": ("IG Reach", "sum"),
    "IG Like": ("IG Like", "sum"),
    "IG Comments": ("IG Comments", "sum"),
    "IG Share": ("IG Share", "sum"),
    "IG Save": ("IG Save", "sum")
})

df_displaya= pd.concat([df_display2, df_display4], axis=0)
df_displayb= pd.concat([df_display3, df_display5], axis=0)

df_displaya["group"] = range(1,len(df_displaya) +1)
df_displayb["group"] = range(1,len(df_displayb) +1)

df_displaya=df_displaya.set_index("group")
df_displayb=df_displayb.set_index("group")

#readjust date#-------------------------
#df_displayfb["Date"]=pd.to_datetime(df_displayfb["Date"]).dt.strftime("%d %B %Y")

#---------------------------------------

col1,col2 = st.columns(2)
with col1:
    st.subheader("Facebook Metrics")
    st.dataframe(df_displayfb.style.background_gradient(cmap=color_map1).format({    
    "FB Followers": "{:,.0f}",
    "FB Views": "{:,.0f}",
    "FB Reach": "{:,.0f}",
    "FB Like": "{:,.0f}",
    "FB Comments": "{:,.0f}",
    "FB Share": "{:,.0f}"   
    }))
    st.dataframe(df_displaya.style.background_gradient(cmap=color_map1).format({    
    "FB Followers": "{:,.2f}",
    "FB Views": "{:,.0f}",
    "FB Reach": "{:,.0f}",
    "FB Like": "{:,.0f}",
    "FB Comments": "{:,.0f}",
    "FB Share": "{:,.0f}"   
    }))
with col2:
    st.subheader("Instagram Metrics")
    st.dataframe(df_displayig.style.background_gradient(cmap=color_map2).format({    
    "IG Followers": "{:,.0f}",
    "IG Viewers": "{:,.0f}",
    "IG Reach": "{:,.0f}",
    "IG Like": "{:,.0f}",
    "IG Comments": "{:,.0f}",
    "IG Share": "{:,.0f}",
    "IG Save" : "{:,.0f}"
    }))
    st.dataframe(df_displayb.style.background_gradient(cmap=color_map2).format({    
    "IG Followers": "{:,.2f}",
    "IG Viewers": "{:,.0f}",
    "IG Reach": "{:,.0f}",
    "IG Like": "{:,.0f}",
    "IG Comments": "{:,.0f}",
    "IG Share": "{:,.0f}",
    "IG Save" : "{:,.0f}"
    }))

#---------------------------------------------------------------------------------
#ttest topic

df_topic = pd.get_dummies(df_f["Topic"], prefix="Topic")

df_combined = pd.concat([df_topic, df_f[[
    "FB Reach", "IG Reach"
]].astype(float)], axis=1)

#---compared----------------------------------------

df_topic_compare = pd.get_dummies(df_f2["Topic"], prefix="Topic")

df_combined_compare = pd.concat([df_topic_compare, df_f2[[
    "FB Reach", "IG Reach"
]].astype(float)], axis=1)

#---------------------------------------------------

fb=[]
for col in df_combined.columns:
    if df_combined[col].dtype == bool:
        t1 = df_combined.loc[df_combined[col], "FB Reach"]
        t2 = df_combined.loc[~df_combined[col], "FB Reach"]
        t, p = stats.ttest_ind(t1, t2, equal_var=False, nan_policy="omit")
        fb.append({"Topic": col, "T-test" : t , "P-Value" : p})

df_fb = pd.DataFrame(fb)


df_fb["Topic"]=df_fb["Topic"].str.replace("Topic_","")
df_fb["Topic"]=df_fb["Topic"].str.title()
df_fb["Significant"]= df_fb["P-Value"] < 0.05

#-day-significant-compare

fb_compare=[]
for col in df_combined_compare.columns:
    if df_combined_compare[col].dtype == bool:
        t1 = df_combined_compare.loc[df_combined_compare[col], "FB Reach"]
        t2 = df_combined_compare.loc[~df_combined_compare[col], "FB Reach"]
        t, p = stats.ttest_ind(t1, t2, equal_var=False, nan_policy="omit")
        fb_compare.append({"Topic": col, "T-test Previous" : t , "P-Value Previous" : p})

df_fb_comp = pd.DataFrame(fb_compare)
df_fb_comp["Topic"]=df_fb_comp["Topic"].str.replace("Topic_","")
df_fb_comp["Topic"]=df_fb_comp["Topic"].str.title()
df_fb_comp["Significant Previous"]= df_fb_comp["P-Value Previous"] < 0.05

df_day_fb = pd.merge(df_fb, df_fb_comp, on="Topic", how="left")

#-ig---------------------------------------------------------

ig=[]
for col in df_combined.columns:
    if df_combined[col].dtype == bool:
        t1 = df_combined.loc[df_combined[col], "IG Reach"]
        t2 = df_combined.loc[~df_combined[col], "IG Reach"]
        t, p = stats.ttest_ind(t1, t2, equal_var=False, nan_policy="omit")
        ig.append({"Topic": col, "T-test" : t , "P-Value" : p})

df_ig = pd.DataFrame(ig)
df_ig["Topic"]=df_ig["Topic"].str.replace("Topic_","")
df_ig["Topic"]=df_ig["Topic"].str.title()
df_ig["Significant"]= df_ig["P-Value"] < 0.05

ig_compare=[]
for col in df_combined_compare.columns:
    if df_combined_compare[col].dtype == bool:
        t1 = df_combined_compare.loc[df_combined_compare[col], "IG Reach"]
        t2 = df_combined_compare.loc[~df_combined_compare[col], "IG Reach"]
        t, p = stats.ttest_ind(t1, t2, equal_var=False, nan_policy="omit")
        ig_compare.append({"Topic": col, "T-test Previous" : t , "P-Value Previous" : p})

df_ig_comp = pd.DataFrame(ig_compare)
df_ig_comp["Topic"]=df_ig_comp["Topic"].str.replace("Topic_","")
df_ig_comp["Topic"]=df_ig_comp["Topic"].str.title()
df_ig_comp["Significant Previous"]= df_ig_comp["P-Value Previous"] < 0.05

df_day_ig = pd.merge(df_ig, df_ig_comp, on="Topic", how="left")

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#place table day significant

col1,col2 = st.columns(2)
with col1:
    st.subheader("Facebook Significant Topic")
    st.dataframe(df_day_fb.style.background_gradient(cmap=color_map1).format({
        "T-test":"{:.3f}",
        "P-Value":"{:.3f}",
        "T-test Previous":"{:.3f}",
        "P-Value Previous":"{:.3f}"
    }))
with col2:
    st.subheader("Instagram Significant Topic")
    st.dataframe(df_day_ig.style.background_gradient(cmap=color_map2).format({
        "T-test":"{:.3f}",
        "P-Value":"{:.3f}",
        "T-test Previous":"{:.3f}",
        "P-Value Previous":"{:.3f}"
    }))


#---------------------------------------------------------------------------------

df_day = pd.get_dummies(df_f["day"], prefix="day")

df_combined2 = pd.concat([df_day, df_f[[
    "FB Reach", "IG Reach"
]].astype(float)], axis=1)

df_day_comp = pd.get_dummies(df_f2["day"], prefix="day")

df_combined2_comp = pd.concat([df_day_comp, df_f2[[
    "FB Reach", "IG Reach"
]].astype(float)], axis=1)

#---------------------------------------------------------------------------------------------------------------------

#ttest day

fb2=[]
for col in df_combined2.columns:
    if df_combined2[col].dtype == bool:
        t1 = df_combined2.loc[df_combined2[col], "FB Reach"]
        t2 = df_combined2.loc[~df_combined2[col], "FB Reach"]
        t, p = stats.ttest_ind(t1, t2, equal_var=False, nan_policy="omit")
        fb2.append({"Topic": col, "T-test" : t , "P-Value" : p})

df_fb2 = pd.DataFrame(fb2)
df_fb2["Topic"]=df_fb2["Topic"].str.replace("day_","")
df_fb2["Significant"]= df_fb2["P-Value"] < 0.05

fb2_comp=[]
for col in df_combined2_comp.columns:
    if df_combined2_comp[col].dtype == bool:
        t1 = df_combined2_comp.loc[df_combined2_comp[col], "FB Reach"]
        t2 = df_combined2_comp.loc[~df_combined2_comp[col], "FB Reach"]
        t, p = stats.ttest_ind(t1, t2, equal_var=False, nan_policy="omit")
        fb2_comp.append({"Topic": col, "T-test Previous" : t , "P-Value Previous" : p})

df_fb2_comp = pd.DataFrame(fb2_comp)
df_fb2_comp["Topic"]=df_fb2_comp["Topic"].str.replace("day_","")
df_fb2_comp["Significant Previous"]= df_fb2_comp["P-Value Previous"] < 0.05

df_day_fb = pd.merge(df_fb2, df_fb2_comp, on="Topic", how="left")

ig2=[]
for col in df_combined2.columns:
    if df_combined2[col].dtype == bool:
        t1 = df_combined2.loc[df_combined2[col], "IG Reach"]
        t2 = df_combined2.loc[~df_combined2[col], "IG Reach"]
        t, p = stats.ttest_ind(t1, t2, equal_var=False, nan_policy="omit")
        ig2.append({"Topic": col, "T-test" : t , "P-Value" : p})

df_ig2 = pd.DataFrame(ig2)
df_ig2["Topic"]=df_ig2["Topic"].str.replace("day_","")
df_ig2["Significant"]= df_ig2["P-Value"] < 0.05

ig2_comp=[]
for col in df_combined2_comp.columns:
    if df_combined2_comp[col].dtype == bool:
        t1 = df_combined2_comp.loc[df_combined2_comp[col], "IG Reach"]
        t2 = df_combined2_comp.loc[~df_combined2_comp[col], "IG Reach"]
        t, p = stats.ttest_ind(t1, t2, equal_var=False, nan_policy="omit")
        ig2_comp.append({"Topic": col, "T-test Previous" : t , "P-Value Previous" : p})

df_ig2_comp = pd.DataFrame(ig2_comp)
df_ig2_comp["Topic"]=df_ig2_comp["Topic"].str.replace("day_","")
df_ig2_comp["Significant Previous"]= df_ig2_comp["P-Value Previous"] < 0.05

df_day_ig = pd.merge(df_ig2, df_ig2_comp, on="Topic", how="left")

#---------------------------------------------------------------------------------
#place table

col1,col2 = st.columns(2)
with col1:
    st.subheader("Facebook Significant Day")
    st.dataframe(df_day_fb.style.background_gradient(cmap=color_map1).format({
        "T-test":"{:.3f}",
        "P-Value":"{:.3f}",
        "T-test Previous":"{:.3f}",
        "P-Value Previous":"{:.3f}"
    }))
with col2:
    st.subheader("Instagram Significant Day")
    st.dataframe(df_day_ig.style.background_gradient(cmap=color_map2).format({
        "T-test":"{:.3f}",
        "P-Value":"{:.3f}",
        "T-test Previous":"{:.3f}",
        "P-Value Previous":"{:.3f}"
    }))

#------------------------------------------------------------------------------------

corr = df_combined.corr()
corr2 = df_combined2.corr()

#-----------------------------------------------------------------------------------

expected_topics = [
    "Topic_baby tips", "Topic_husband & wife", "Topic_others",
    "Topic_parenting tips", "Topic_pregnancy tips"
]
expected_days = [
    "day_Monday", "day_Tuesday", "day_Wednesday", "day_Thursday",
    "day_Friday", "day_Saturday", "day_Sunday"
]

for col in expected_topics:
    if col not in corr.columns:
        corr[col] = 0

for col in expected_days:
    if col not in corr2.columns:
        corr2[col] = 0

#corellation-topic----------------------------------------------------------------


corr.rename(columns= {"Topic_baby tips":"Baby Tips", 
                      "Topic_husband & wife":"Husband & Wife", 
                      "Topic_others":"Others", 
                      "Topic_parenting tips":"Parenting Tips", 
                      "Topic_pregnancy tips":"Pregnancy Tips" }, inplace=True)

#mask = (corr["index"] >= 6 )

#plt.figure(figsize=(12,8))
#sns.heatmap(corr, cmap="coolwarm", annot=True, fmt=".2f")
#plt.title("Topic vs Engagement Correlation Heatmap")
#plt.show()


#corellation-day------------------------------------------------------------------


corr2.rename(columns= {"day_Friday":"Friday", 
                      "day_Monday":"Monday", 
                      "day_Saturday":"Saturday", 
                      "day_Sunday":"Sunday", 
                      "day_Thursday":"Thursday",
                      "day_Tuesday":"Tuesday",
                      "day_Wednesday":"Wednesday"}, inplace=True)

#mask2 = (corr2["index"] >= 8 )

#plt.figure(figsize=(12,8))
#sns.heatmap(corr, cmap="coolwarm", annot=True, fmt=".2f")
#plt.title("Topic vs Engagement Correlation Heatmap")
#plt.show()

#corr_a = corr[mask]
#corr_b = corr2[mask2] 
#df_corr = corr_a.merge(corr_b, on="index")
#df_corr = pd.concat([corr_a, corr_b[["Monday","Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]] ], axis=1)
#df_corr = pd.concat([corr, corr2[["Monday","Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]] ], axis=1)

#-corellation-compare---------

df_combined_compare.rename(columns= {"FB Reach":"FB Reach Previous", "IG Reach":"IG Reach Previous"}, inplace=True)
df_combined2_comp.rename(columns= {"FB Reach":"FB Reach Previous", "IG Reach":"IG Reach Previous"}, inplace=True)

#corellation topic
corr_comp = df_combined_compare.corr()

corr_comp.rename(columns= {"Topic_baby tips":"Baby Tips", 
                      "Topic_husband & wife":"Husband & Wife", 
                      "Topic_others":"Others", 
                      "Topic_parenting tips":"Parenting Tips", 
                      "Topic_pregnancy tips":"Pregnancy Tips" }, inplace=True)

#mask = (corr_comp["index"] >= 6 )

#plt.figure(figsize=(12,8))
#sns.heatmap(corr_comp, cmap="coolwarm", annot=True, fmt=".2f")
#plt.title("Topic vs Engagement Correlation Heatmap")
#plt.show()


#corellation topic
corr2_comp = df_combined2_comp.corr()

corr2_comp.rename(columns= {"day_Friday":"Friday", 
                      "day_Monday":"Monday", 
                      "day_Saturday":"Saturday", 
                      "day_Sunday":"Sunday", 
                      "day_Thursday":"Thursday",
                      "day_Tuesday":"Tuesday",
                      "day_Wednesday":"Wednesday"}, inplace=True)

#mask2 = (corr2["index"] >= 8 )

#plt.figure(figsize=(12,8))
#sns.heatmap(corr, cmap="coolwarm", annot=True, fmt=".2f")
#plt.title("Topic vs Engagement Correlation Heatmap")
#plt.show()

#corr_a_comp = corr_comp[mask]
#corr_b_comp = corr2_comp[mask2]
#df_corr = corr_a.merge(corr_b, on="index")
#df_corr_comp = pd.concat([corr_a_comp, corr_b_comp[["Monday","Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]], axis=1)
df_corr_comp = pd.concat([corr_comp, corr2_comp[["Monday","Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]], axis=1)

#corr_a = corr_a_comp.drop("index", axis=1)
#corr_a_comp = corr_a_comp.drop("index", axis=1)
#corr_b = corr_a_comp.drop("index", axis=1)
#corr_b_comp = corr_a_comp.drop("index", axis=1)

#-start-filtering-removing-columns/rows--------------

#-corr
#-corr_comp
#-corr2
#-corr2_comp

corr = corr.loc[["FB Reach", "IG Reach"]]
corr_comp = corr_comp.loc[["FB Reach Previous", "IG Reach Previous"]]
corr2 = corr2.loc[["FB Reach", "IG Reach"]]
corr2_comp = corr2_comp.loc[["FB Reach Previous", "IG Reach Previous"]]

#df_big = pd.concat([table_a, table_b], axis=0, ignore_index=True)
corr_a = pd.concat([corr, corr_comp], axis=0, ignore_index=False)
corr_b = pd.concat([corr2, corr2_comp], axis=0, ignore_index=False)

#df_new = df.drop(['col2', 'col4'], axis=1)
corr_a = corr_a.drop(["FB Reach", "IG Reach", "FB Reach Previous", "IG Reach Previous"], axis=1)
corr_b = corr_b.drop(["FB Reach", "IG Reach", "FB Reach Previous", "IG Reach Previous"], axis=1)

#-start-placing-table--------------------------------

#st.subheader(f"Corellation: {min_date.strftime("%#d %B %Y")} to {max_date.strftime("%#d %B %Y")} vs {prev_start.strftime("%#d %B %Y")} to {prev_end.strftime("%#d %B %Y")}")
#st.dataframe(corr.style.background_gradient(cmap=color_map3))
#st.dataframe(corr_comp.style.background_gradient(cmap=color_map3))

#st.subheader(f"Corellation from {prev_start.strftime("%#d %B %Y")} to {prev_end.strftime("%#d %B %Y")}")
#st.dataframe(corr2.style.background_gradient(cmap=color_map3))
#st.dataframe(corr2_comp.style.background_gradient(cmap=color_map3))

st.subheader(f"Corellation: {start_date.strftime("%#d %B %Y")} to {end_date.strftime("%#d %B %Y")} vs {prev_start.strftime("%#d %B %Y")} to {prev_end.strftime("%#d %B %Y")}")

st.dataframe(corr_a.style.background_gradient(cmap=color_map3).format({
        "Baby Tips":"{:.3f}",
        "Husband & Wife":"{:.3f}",
        "Others":"{:.3f}",
        "Parenting Tips":"{:.3f}",
        "Pregnancy Tips":"{:.3f}"
    }))
st.dataframe(corr_b.style.background_gradient(cmap=color_map3).format({
        "Friday":"{:.3f}",
        "Monday":"{:.3f}",
        "Saturday":"{:.3f}",
        "Sunday":"{:.3f}",
        "Thursday":"{:.3f}",
        "Tuesday":"{:.3f}",
        "Wednesday":"{:.3f}"
    }))

#-try-chart-scatter/whatever-graph------------------------------------------------------------------------------------

topic_select = df_f["Topic"].unique()
topic_selected = st.multiselect("Select Topic(s)", topic_select, default=topic_select)

topic_graphfb = df_f[df_f["Topic"].isin(topic_selected)].groupby(["Topic","Date", "Title"], as_index=False).agg(**{
    "FB Reach": ("FB Reach", "sum")})

chart =alt.Chart(topic_graphfb).mark_circle(size=60).encode(
    x="Date",
    y="FB Reach",
    color="Topic",
    tooltip=["Date", "FB Reach", "Topic", "Title"]
).interactive()

st.subheader("Facebook Topic Distribution by Date")
st.altair_chart(chart, use_container_width=True)

#-----------------------------------------------------------
#-section-FB------------------------------------------------
#-----------------------------------------------------------

with st.expander("FB Section"):
    col1,col2 = st.columns(2)
    with col1:
        topic_graphig = df_f[df_f["Topic"]=="baby tips"].groupby(["Topic","Date", "Title"], as_index=False).agg(**{
            "FB Reach": ("FB Reach", "sum")})
        
        chart =alt.Chart(topic_graphig).mark_circle(size=60).encode(
            x="Date", y="FB Reach", color=alt.Color("Topic",legend=None), tooltip=["Date", "FB Reach", "Topic", "Title"])
        
        st.write("Baby Tips Scatter Plot")
        st.altair_chart(chart, use_container_width=True)

        topic_graphig = df_f[df_f["Topic"]=="parenting tips"].groupby(["Topic","Date", "Title"], as_index=False).agg(**{
            "FB Reach": ("FB Reach", "sum")})
        
        chart =alt.Chart(topic_graphig).mark_circle(size=60).encode(
            x="Date", y="FB Reach", color=alt.Color("Topic",legend=None), tooltip=["Date", "FB Reach", "Topic", "Title"])
        
        st.write("Parenting Tips Scatter Plot")
        st.altair_chart(chart, use_container_width=True)

    with col2:
        topic_graphig = df_f[df_f["Topic"]=="husband & wife"].groupby(["Topic","Date", "Title"], as_index=False).agg(**{
            "FB Reach": ("FB Reach", "sum")})
        
        chart =alt.Chart(topic_graphig).mark_circle(size=60).encode(
            x="Date", y="FB Reach", color=alt.Color("Topic",legend=None), tooltip=["Date", "FB Reach", "Topic", "Title"])
        
        st.write("Husband & Wife Scatter Plot")
        st.altair_chart(chart, use_container_width=True)

        topic_graphig = df_f[df_f["Topic"]=="pregnancy tips"].groupby(["Topic","Date", "Title"], as_index=False).agg(**{
            "FB Reach": ("FB Reach", "sum")})
        
        chart =alt.Chart(topic_graphig).mark_circle(size=60).encode(
            x="Date", y="FB Reach", color=alt.Color("Topic",legend=None), tooltip=["Date", "FB Reach", "Topic", "Title"])
        
        st.write("Pregnancy Tips Scatter Plot")
        st.altair_chart(chart, use_container_width=True)


#-igscatter--bozo---------------------------------------

topic_graphig = df_f[df_f["Topic"].isin(topic_selected)].groupby(["Topic","Date", "Title"], as_index=False).agg(**{
    "IG Reach": ("IG Reach", "sum")})

chart =alt.Chart(topic_graphig).mark_circle(size=60).encode(
    x="Date",
    y="IG Reach",
    color="Topic",
    tooltip=["Date", "IG Reach", "Topic", "Title"]
).interactive()

st.subheader("Instagram Topic Distribution by Date")
st.altair_chart(chart, use_container_width=True)

#-----------------------------------------------------------
#-section-IG------------------------------------------------
#-----------------------------------------------------------

with st.expander("IG Section"):
    col1,col2 = st.columns(2)
    with col1:
        topic_graphig = df_f[df_f["Topic"]=="baby tips"].groupby(["Topic","Date", "Title"], as_index=False).agg(**{
            "IG Followers": ("IG Followers", "sum"),
            "IG Viewers": ("IG Viewers", "sum"),
            "IG Reach": ("IG Reach", "sum"),
            "IG Like": ("IG Like", "sum"),
            "IG Comments": ("IG Comments", "sum"),
            "IG Share": ("IG Share", "sum"),
            "IG Save": ("IG Save", "sum")})
        
        chart =alt.Chart(topic_graphig).mark_circle(size=60).encode(
            x="Date", y="IG Reach", color=alt.Color("Topic",legend=None), tooltip=["Date", "IG Reach", "Topic","Title"])
        
        st.write("Baby Tips Scatter Plot")
        st.altair_chart(chart, use_container_width=True)

        topic_graphig = df_f[df_f["Topic"]=="parenting tips"].groupby(["Topic","Date","Title"], as_index=False).agg(**{
            "IG Followers": ("IG Followers", "sum"),
            "IG Viewers": ("IG Viewers", "sum"),
            "IG Reach": ("IG Reach", "sum"),
            "IG Like": ("IG Like", "sum"),
            "IG Comments": ("IG Comments", "sum"),
            "IG Share": ("IG Share", "sum"),
            "IG Save": ("IG Save", "sum")})
        
        chart =alt.Chart(topic_graphig).mark_circle(size=60).encode(
            x="Date", y="IG Reach", color=alt.Color("Topic",legend=None), tooltip=["Date", "IG Reach", "Topic", "Title"])
        
        st.write("Parenting Tips Scatter Plot")
        st.altair_chart(chart, use_container_width=True)

    with col2:
        topic_graphig = df_f[df_f["Topic"]=="husband & wife"].groupby(["Topic","Date" ,"Title" ], as_index=False).agg(**{
            "IG Followers": ("IG Followers", "sum"),
            "IG Viewers": ("IG Viewers", "sum"),
            "IG Reach": ("IG Reach", "sum"),
            "IG Like": ("IG Like", "sum"),
            "IG Comments": ("IG Comments", "sum"),
            "IG Share": ("IG Share", "sum"),
            "IG Save": ("IG Save", "sum")})
        
        chart =alt.Chart(topic_graphig).mark_circle(size=60).encode(
            x="Date", y="IG Reach", color=alt.Color("Topic",legend=None), tooltip=["Date", "IG Reach", "Topic", "Title"])
        
        st.write("Husband & Wife Scatter Plot")
        st.altair_chart(chart, use_container_width=True)

        topic_graphig = df_f[df_f["Topic"]=="pregnancy tips"].groupby(["Topic","Date", "Title"], as_index=False).agg(**{
            "IG Followers": ("IG Followers", "sum"),
            "IG Viewers": ("IG Viewers", "sum"),
            "IG Reach": ("IG Reach", "sum"),
            "IG Like": ("IG Like", "sum"),
            "IG Comments": ("IG Comments", "sum"),
            "IG Share": ("IG Share", "sum"),
            "IG Save": ("IG Save", "sum")})
        
        chart =alt.Chart(topic_graphig).mark_circle(size=60).encode(
            x="Date", y="IG Reach", color=alt.Color("Topic",legend=None), tooltip=["Date", "IG Reach", "Topic", "Title"])
        
        st.write("Pregnancy Tips Scatter Plot")
        st.altair_chart(chart, use_container_width=True)

#------------------------------------------------------------------------------------

df_followers1 = df_f.groupby("Date", as_index = False).agg(**{
    "Reach" : ("FB Reach", "mean"),
    "Followers" : ("FB Followers", "mean"),
    "Views" : ("FB Views", "mean")
})

df_followers2 = df_f2.groupby("Date", as_index = False).agg(**{
    "Reach" : ("FB Reach", "mean"),
    "Followers" : ("FB Followers", "mean"),
    "Views" : ("FB Views", "mean")
})

df_followers1["Date"]= pd.to_datetime(df_followers1["Date"], dayfirst=True)
df_followers2["Date"]= pd.to_datetime(df_followers2["Date"], dayfirst=True)

period_length = (end_date - start_date).days

df_followers2_aligned = df_followers2.copy()
df_followers2_aligned["Date"] = pd.to_datetime(df_followers2_aligned["Date"]) + pd.Timedelta(days=period_length)

chart1 = (
    alt.Chart(df_followers1)
    .mark_line(interpolate='monotone', color="#0072B2", strokeWidth=2)
    .encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Followers:Q", title="Average Followers"),
        tooltip=["Date", "Followers"]
    )
    .properties(title="Current Period")
)

chart2 = (
    alt.Chart(df_followers2_aligned)
    .mark_line(interpolate='monotone', color="#E69F00", strokeDash=[5, 5], strokeWidth=2, opacity=0.8)
    .encode(
        x="Date:T",
        y="Followers:Q",
        tooltip=["Date", "Followers"]
    )
    .properties(title="Previous Period (Shifted & Aligned)")
)

chart = alt.layer(chart1, chart2).properties(
    width=700,
    height=400,
    title="Reach Comparison: Current vs Previous Period (Overlayed)"
).interactive()

st.altair_chart(chart, use_container_width=True)

#-------------------------------------------------------------------------------------------

df_followers3 = df_f.groupby("Date", as_index = False).agg(**{
    "Reach" : ("IG Reach", "mean"),
    "Followers" : ("IG Followers", "mean"),
    "Views" : ("IG Viewers", "mean")
})

df_followers4 = df_f2.groupby("Date", as_index = False).agg(**{
    "Reach" : ("IG Reach", "mean"),
    "Followers" : ("IG Followers", "mean"),
    "Views" : ("IG Viewers", "mean")
})

df_followers3["Date"]= pd.to_datetime(df_followers1["Date"], dayfirst=True)
df_followers4["Date"]= pd.to_datetime(df_followers2["Date"], dayfirst=True)

period_length = (end_date - start_date).days

df_followers4_aligned = df_followers4.copy()
df_followers4_aligned["Date"] = pd.to_datetime(df_followers4_aligned["Date"]) + pd.Timedelta(days=period_length)

chart3 = (
    alt.Chart(df_followers3)
    .mark_line(interpolate='monotone', color="#0072B2", strokeWidth=2)
    .encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Followers:Q", title="Average Followers"),
        tooltip=["Date", "Followers"]
    )
    .properties(title="Current Period")
)

chart4 = (
    alt.Chart(df_followers4_aligned)
    .mark_line(interpolate='monotone', color="#E69F00", strokeDash=[5, 5], strokeWidth=2, opacity=0.8)
    .encode(
        x="Date:T",
        y="Followers:Q",
        tooltip=["Date", "Followers"]
    )
    .properties(title="Previous Period (Shifted & Aligned)")
)

charts = alt.layer(chart3, chart4).properties(
    width=700,
    height=400,
    title="Reach Comparison: Current vs Previous Period (Overlayed)"
).interactive()

st.altair_chart(charts, use_container_width=True)
