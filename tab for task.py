import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap\
import seaborn as sns
from scipy.stats import f_oneway

st.markdown(
    "<h1 style='text-align: center;'>August, September, October 2025 Analysis</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align: center;'>prepared by: Izzat</h3>",
    unsafe_allow_html=True
)

df=pd.read_csv("task1-clean csv.csv")

color1 = [ "#ffffff", "#ffffff", "#66ffb3"  ]
color_map1 = LinearSegmentedColormap.from_list("my_cmap", color1)

df["date time"] = pd.to_datetime(df["date time"], dayfirst=True)
df["date"] = pd.to_datetime(df["date time"], dayfirst=True).dt.date
df["time"] = pd.to_datetime(df["date time"], dayfirst=True).dt.time
df["DOM"] = df["date time"].dt.day
df = df.set_index("date time")

df = df.rename(columns={"Total":"Sales", 
                        "transaction":"Transaction", 
                        "date time":"Date Time",
                        "slot": "Slot",
                        "holiday":"Holiday",
                        "Qty":"Quantity"})


tab1, tab2, tab3 = st.tabs(["Task 1", "Task 2", "Others"])

with tab1:
    st.header("Task 1")
    f1 = (df.groupby(["DOM", "Month"], as_index=False).agg({
        "Sales": "sum",
        "Transaction": "sum",}))
    df_pivot = df1.pivot(index="DOM", columns="Month", values=["Sales","Transaction"])
    st.subheader("Sum Sales and Transaction by DOM for Month August, September, October.")
    st.dataframe(df_pivot.style.background_gradient(cmap=color_map1).format({
    ("Sales", "August"): "{:,.2f}",
    ("Transaction", "August"): "{:,.0f}",
    ("Sales", "September"): "{:,.2f}",
    ("Transaction", "September"): "{:,.0f}",
    ("Sales", "October"): "{:,.2f}",
    ("Transaction", "October"): "{:,.0f}",
    }))

    august_sales = df[df["Month"] == "August"].groupby("DOM", as_index = True ).agg(
    {"Sales":"sum"})
    august_sales = august_sales.rename(columns = {"Sales":"August Sales"})
    #+
    september_sales = df[df["Month"] == "September"].groupby("DOM", as_index = True ).agg(
    {"Sales":"sum"})
    september_sales = september_sales.rename(columns = {"Sales":"September Sales"})
    #+
    october_sales = df[df["Month"] == "October"].groupby("DOM", as_index = True ).agg(
    {"Sales":"sum"})
    october_sales = october_sales.rename(columns = {"Sales":"October Sales"})
    #for transaction
    august_tranc = df[df["Month"] == "August"].groupby("DOM", as_index = True ).agg(
    {"Transaction" : "sum"})
    august_tranc = august_tranc.rename(columns = {"Transaction":"August Transaction"})
    #+
    september_tranc = df[df["Month"] == "September"].groupby("DOM", as_index = True ).agg(
    {"Transaction" : "sum"})
    september_tranc = september_tranc.rename(columns = {"Transaction":"September Transaction"})
    #+
    october_tranc = df[df["Month"] == "October"].groupby("DOM", as_index = True ).agg(
    {"Transaction" : "sum"})
    october_tranc = october_tranc.rename(columns = {"Transaction":"October Transaction"})
    #concat it ------------------- #= # all month_sales has index, so concat join on index! wowwerz!
    df_sales = pd.concat([august_sales, september_sales, october_sales], axis=1)
    df_sales = df_sales.reset_index()
    df_tranc = pd.concat([august_tranc, september_tranc, october_tranc], axis=1)
    df_tranc = df_tranc.reset_index()
    #plot
    df_long = df_sales.melt(id_vars="DOM", var_name="Month", value_name="Sales")
    df_long["Month"] = df_long["Month"].str.replace(" Sales", "")
    sales = alt.Chart(df_long).mark_line(point=True, interpolate="monotone").encode(
        x="DOM:Q",
        y="Sales:Q",
        color=alt.Color("Month:N", scale=alt.Scale(domain=["August", "September", "October"],
                                                   range=["#0099ff", "#4dffa6", "#ff471a"]), legend= None),
        tooltip=["DOM", "Month", "Sales"])
    st.caption("Sales of DOM per Month :🟦 August 🟩 September 🟥 October")
    st.altair_chart(sales, use_container_width=True)
    
    df_long2 = df_tranc.melt(id_vars="DOM", var_name="Month", value_name="Transaction")
    df_long2["Month"] = df_long2["Month"].str.replace(" Transaction", "")
    
    tranc = alt.Chart(df_long2).mark_line(point=True, interpolate="monotone").encode(x="DOM:Q", y="Transaction:Q",
                                                                                     color=alt.Color("Month:N", 
                                                                                                     scale=alt.Scale(domain=["August", "September", "October"],
                                                                                                                     range=["#0099ff", "#4dffa6", "#ff471a"]), legend= None),
                                                                                     tooltip=["DOM", "Month", "Transaction"])
    st.caption("Transaction of DOM per Month :🟦 August 🟩 September 🟥 October")
    st.altair_chart(tranc, use_container_width=True)
    st.subheader("What does it tells.")
    st.write("Both of them (Sales and Transaction) seems identical, we say H1 : sales trend by month = transactions trend by month. Thats interesting topic but we'll discuss H1 further in topic 'things or two regarding sales and transaction'. But right now, we need to know.")
    st.write("(1) August and September peak in early day of month (DOM). And then after second quarter, its a stage for August and September.")
    st.write("(2) September is the worst series out of three. It has (a) the lowest point of collected sales (b) the smallest peak out of three series. (c) almost constant / decreases trendline if we draw one.")
    st.write("This section is not about taking away our 'assumed hypothesis', when we first click the report, we want to see one thing and everyone has different idea, so this section is about presenting an open picture of sales per day for each month without explaining any factors or reasoning etc. Everyone free to make assumption, and then pleased to scroll down and see whats more to come.")
    #twin, this is slot groupby twin
    #twin can i borrow 20 buck
    df2 = (df.groupby(["Slot", "Month"], as_index=False).agg({
        "Sales": "sum",
        "Transaction": "sum",})
    )
    df2_pivot = df2.pivot(index="Slot", columns="Month", values=["Sales","Transaction"])
    st.subheader("Sum Sales and Transaction by Slot for Month August, September, October.")
    st.dataframe(df2_pivot.style.background_gradient(cmap=color_map1).format({
        ("Sales", "August"): "{:,.2f}",
        ("Transaction", "August"): "{:,.0f}",
        ("Sales", "September"): "{:,.2f}",
        ("Transaction", "September"): "{:,.0f}",
        ("Sales", "October"): "{:,.2f}",
        ("Transaction", "October"): "{:,.0f}",
    }))
    
    august_slot = df[df["Month"] == "August"].groupby("Slot", as_index = True ).agg({"Sales":"sum"})
    september_slot = df[df["Month"] == "September"].groupby("Slot", as_index = True ).agg({"Sales":"sum"})
    october_slot = df[df["Month"] == "October"].groupby("Slot", as_index = True ).agg({"Sales":"sum"})
    august_slot = august_slot.rename(columns = {"Sales":"August Sales"})
    september_slot = september_slot.rename(columns = {"Sales":"September Sales"})
    october_slot = october_slot.rename(columns = {"Sales":"October Sales"})
    august_slot1 = df[df["Month"] == "August"].groupby("Slot", as_index = True ).agg({"Transaction":"sum"})
    september_slot1 = df[df["Month"] == "September"].groupby("Slot", as_index = True ).agg({"Transaction":"sum"})
    october_slot1 = df[df["Month"] == "October"].groupby("Slot", as_index = True ).agg({"Transaction":"sum"})
    august_slot1 = august_slot1.rename(columns = {"Transaction":"August Transaction"})
    september_slot1 = september_slot1.rename(columns = {"Transaction":"September Transaction"})
    october_slot1 = october_slot1.rename(columns = {"Transaction":"October Transaction"})
    df_slot = pd.concat([august_slot, september_slot, october_slot], axis=1)
    df_slot = df_slot.reset_index()
    df_slot1 = pd.concat([august_slot1, september_slot1, october_slot1], axis=1)
    df_slot1 = df_slot1.reset_index()
    #plot this twin, plot for groupby slot
    df_long3 = df_slot.melt(id_vars="Slot", var_name="Month", value_name="Sales")
    df_long3["Month"] = df_long3["Month"].str.replace(" Sales", "")
    sales1 = alt.Chart(df_long3).mark_line(point=True, interpolate="monotone").encode(
        x=alt.X("Slot:O" , axis=alt.Axis(labelAngle=0)),y="Sales:Q",color=alt.Color("Month:N", 
                                                                                    scale=alt.Scale(domain=["August", "September", "October"],
                                                                                                    range=["#0099ff", "#4dffa6", "#ff471a"]), legend= None),
        tooltip=["Slot", "Month", "Sales"])
    st.caption("Sales of Slot per Month : 🟦 August 🟩 September 🟥 October")
    st.altair_chart(sales1, use_container_width=True)
    df_long4 = df_slot1.melt(id_vars="Slot", var_name="Month", value_name="Transaction")
    df_long4["Month"] = df_long4["Month"].str.replace(" Transaction", "")
    tranc1 = alt.Chart(df_long4).mark_line(point=True, interpolate="monotone").encode(
        x=alt.X("Slot:O" , axis=alt.Axis(labelAngle=0)),
        y="Transaction:Q",
        color=alt.Color("Month:N", 
                        scale=alt.Scale(domain=["August", "September", "October"],
                                        range=["#0099ff", "#4dffa6", "#ff471a"]), legend= None),
        tooltip=["Slot", "Month", "Transaction"])
    st.caption("Transaction of Slot per Month :🟦 August 🟩 September 🟥 October")
    st.altair_chart(tranc1, use_container_width=True)
    st.subheader("Slot Analysis")
    st.write ( "We purposely dont continous the time becasue we can transforms it into an obvious analysis. A single peak and shape like probability distribution 😌. How to understand this? ok here it goes. Imagine probability, if 'its happening!' then y = 1 (becasuse whatever happen already happen so is true for probability = 1/1). If probability = 0.9 we dont say 'its happening!' instead we say 'almost happen 🤏' so as we go further to probability = 0.00, untill we say 'ok not happening'. as number decreases , y will follow on smooth curved line. This is whats happening with our graph, assume the axis for x=0 and y = 1, is at 3pm to 6pm, so to the right (9am - 12pm) y ~ 0.25 and to the left (12am to 9am) y ~ 0.000999, This is very interesting.")
    st.write("Lets put it into the statement game:")
    st.write("(1) If 3 pm to 6 pm -> confirm sales probability (1 to 0.8 +/-).")
    st.write("(2) If 12 pm to 3 pm @ 6 pm to 9 pm -> maybe-lah sales probability (0.8 to 0.6 +/-).")
    st.write("(3) If 12 am pm to 9 am -> no work so no sales.")
    st.write("(4) Night shift -> has lowest sales point for three months *iff* we based on shift availability.")
    dfc = df
    dfc["time"] = dfc["time"].astype("string")
    dfc["Hour"]=dfc["time"].str[:2]
    dfc["Hour"] = dfc["Hour"].astype(int)
    cont = dfc.groupby(["Hour", "Month"], as_index = False ).agg({"Sales":"sum"}).sort_values(by="Hour", ascending=True)
    plot = alt.Chart(cont).mark_area(opacity=0.3, #interpolate="monotone"
                                    ).encode(x=alt.X("Hour:Q" , axis=alt.Axis(labelAngle=0)),y="Sales:Q",color=alt.Color("Month:N", 
                                                                                                                         scale=alt.Scale(domain=["August", "September", "October"],
                                                                                                                                         range=["#0099ff", "#4dffa6", "#ff471a"]), legend= None), tooltip=["Hour", "Month", "Sales"])
    aug_both = df[df["Month"] == "August"].groupby("DOM", as_index = False ).agg({"Sales":"sum","Transaction":"sum"})
    line = (alt.Chart(aug_both).mark_line(interpolate = "monotone").encode(
        x=alt.X("DOM:Q", scale=alt.Scale(domain=[aug_both["DOM"].min(), aug_both["DOM"].max()])),
        y=alt.Y("Sales:Q", title="Sales"), color=alt.value("#1a75ff"), tooltip=["DOM", "Sales"],))
    bar = (alt.Chart(aug_both).mark_bar().encode(
        x=alt.X("DOM:Q" ,scale=alt.Scale(domain=[aug_both["DOM"].min(), aug_both["DOM"].max()])),
        y=alt.Y("Transaction:Q", title="Transactions"), color=alt.value("#ff4d4d"), tooltip=["DOM", "Transaction", "Sales"],))
    linebar = (line + bar).resolve_scale(y="independent")        
    sep_both = df[df["Month"] == "September"].groupby("DOM", as_index = False ).agg(
        {"Sales":"sum","Transaction":"sum"})
    line1 = (
        alt.Chart(sep_both).mark_line(interpolate = "monotone").encode(
            x=alt.X("DOM:Q", scale=alt.Scale(domain=[sep_both["DOM"].min(), sep_both["DOM"].max()])),
            y=alt.Y("Sales:Q", title="Sales"), color=alt.value("#1a75ff"), tooltip=["DOM", alt.Tooltip("Sales:Q", title="Sales")],))
    bar1 = (alt.Chart(sep_both).mark_bar().encode(
        x=alt.X("DOM:Q" ,scale=alt.Scale(domain=[sep_both["DOM"].min(), sep_both["DOM"].max()])),
        y=alt.Y("Transaction:Q", title="Transactions"), color=alt.value("#ff4d4d"), tooltip=["DOM", "Transaction", "Sales"],))
    linebar1 = (line1 + bar1).resolve_scale(y="independent")        
    oct_both = df[df["Month"] == "October"].groupby("DOM", as_index = False ).agg(
        {"Sales":"sum", "Transaction":"sum"})
    line2 = (
        alt.Chart(oct_both).mark_line(interpolate = "monotone").encode(
            x=alt.X("DOM:Q", scale=alt.Scale(domain=[oct_both["DOM"].min(), oct_both["DOM"].max()])),
            y=alt.Y("Sales:Q", title="Sales"), color=alt.value("#1a75ff"), tooltip=["DOM", alt.Tooltip("Sales:Q", title="Sales")],))
    bar2 = (
        alt.Chart(oct_both).mark_bar().encode(
            x=alt.X("DOM:Q" ,scale=alt.Scale(domain=[oct_both["DOM"].min(), oct_both["DOM"].max()])),
            y=alt.Y("Transaction:Q", title="Transactions"), color=alt.value("#ff4d4d"), tooltip=["DOM", "Transaction", "Sales"],))
    linebar2 = (line2 + bar2).resolve_scale(y="independent")        
    df_corr = pd.concat([august_sales, august_tranc, september_sales, september_tranc, october_sales, october_tranc], axis=1)
    corr_matrix = df_corr.corr()
    aug_ = corr_matrix.loc["August Sales", "August Transaction"]
    sep_ = corr_matrix.loc["September Sales", "September Transaction"]
    oct_ = corr_matrix.loc["October Sales", "October Transaction"]
    df_corr = df_corr.corr().stack().reset_index()
    df_corr.columns = ["variable1", "variable2", "correlation"]
    month_sns = alt.Chart(df_corr).mark_rect().encode(
        x=alt.X("variable1:O", title=None), y=alt.Y("variable2:O", title=None),
        color=alt.Color("correlation:Q", title="Correlation", scale=alt.Scale(range="heatmap")),
        tooltip=["variable1", "variable2", "correlation"]).properties(title="Correlation Heatmap",width=400,height=400)
    month_text = (
        alt.Chart(df_corr)
            .mark_text(size=12, fontWeight="bold", color="black").encode(x="variable1:O", y="variable2:O", text=alt.Text("correlation:Q", format=".2f")))
    
with tab2:
    st.header("Task 2")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
with tab3:
    st.header("Others")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)