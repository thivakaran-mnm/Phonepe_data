import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

#CREATE DATAFRAMES FROM SQL
mycon=mysql.connector.connect(host="localhost",user="root",password="Thiva@1999",database="phonepe",auth_plugin='mysql_native_password')
mycursor=mycon.cursor()

#1
mycursor.execute("SELECT * FROM Agg_insurance")
table1 = mycursor.fetchall()
Agg_Insurance = pd.DataFrame(table1, columns=('States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount'))
mycon.commit()
#2
mycursor.execute("SELECT * FROM Agg_Trans")
table1 = mycursor.fetchall()
Agg_Transaction = pd.DataFrame(table1, columns=('States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount'))
mycon.commit()
#3
mycursor.execute("SELECT * FROM Agg_User")
table1 = mycursor.fetchall()
Agg_Users = pd.DataFrame(table1, columns=('States', 'Years', 'Quarter', 'Brand_Name', 'Transaction_Count','Percentage'))
mycon.commit()
#4
mycursor.execute("SELECT * FROM Map_Insur")
table4 = mycursor.fetchall()
Map_Insurance = pd.DataFrame(table4, columns=('States', 'Years', 'Quarter', 'District', 'Transaction_count','Transaction_amount'))
mycon.commit()
#5
mycursor.execute("SELECT * FROM Map_Trans")
table5 = mycursor.fetchall()
Map_Transaction = pd.DataFrame(table5, columns=('States', 'Years', 'Quarter', 'District', 'Transaction_count','Transaction_amount'))
mycon.commit()
#6
mycursor.execute("SELECT * FROM Map_User")
table6 = mycursor.fetchall()
Map_Users = pd.DataFrame(table6, columns=('States', 'Years', 'Quarter', 'District', 'Registered_Users', 'App_Opens'))
mycon.commit()
#7
mycursor.execute("SELECT * FROM Top_Insur")
table7 = mycursor.fetchall()
Top_Insurance = pd.DataFrame(table7, columns=('States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count','Transaction_amount'))
mycon.commit()
#8
mycursor.execute("SELECT * FROM Top_Trans")
table8 = mycursor.fetchall()
Top_Transaction = pd.DataFrame(table8, columns=('States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count','Transaction_amount'))
mycon.commit()
#9
mycursor.execute("SELECT * FROM Top_User")
table9 = mycursor.fetchall()
Top_Users = pd.DataFrame(table9, columns=('States', 'Years', 'Quarter', 'Pincodes', 'Registered_Users'))
mycon.commit()


def Agg_insurance_year(df,year):
    aiy= df[df["Years"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="States", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                           width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(aiyg, x="States", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                          width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        

        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_amount"].min(),aiyg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_count"].min(),aiyg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)

    return aiy


def Aggre_insurance_quarter(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "States", y= "Transaction_amount", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(aiyqg, x= "States", y= "Transaction_count", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_amount"].min(),aiyqg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_count"].min(),aiyqg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)
    
    return aiyq

def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)
        
def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_count", hover_data= "Percentage",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def map_insure_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "District", values= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "District", values= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

def map_user_plot_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUser", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["RegisteredUser"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "RegisteredUser",barmode= "group",
                           width=1000, height= 800,color= "RegisteredUser",hover_data="Pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

def ques1():
    brand= Agg_Users[["Brand_Name","Transaction_Count"]]
    brand1= brand.groupby("Brand_Name")["Transaction_Count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_Count", names= "Brand_Name", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    ht= Agg_Transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(5)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    lt= Agg_Transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(5)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques4():
    stc= Agg_Transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques5():
    stc= Agg_Transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques6():
    dt= Map_Transaction[["District", "Transaction_amount"]]
    dt1= dt.groupby("District")["Transaction_amount"].sum().sort_values(ascending=False)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "District", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)

def ques7():
    dt= Map_Transaction[["District", "Transaction_amount"]]
    dt1= dt.groupby("District")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "District", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)

def ques8():
    dtc= Agg_Transaction[["District", "Transaction_Count"]]
    dtc1= dtc.groupby("States")["Transaction_Count"].sum().sort_values(ascending=False)
    dtc2= pd.DataFrame(dtc1).reset_index()

    fig_dtc= px.bar(dtc2, x= "States", y= "Transaction_Count", title= "DISTRICTS WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_dtc)

def ques9():
    dtcl= Agg_Transaction[["District", "Transaction_Count"]]
    dtcl1= dtcl.groupby("States")["Transaction_Count"].sum().sort_values(ascending=True)
    dtcl2= pd.DataFrame(dtcl1).reset_index()

    fig_dtcl= px.bar(dtcl2, x= "States", y= "Transaction_Count", title= "DISTRICTS WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_dtcl)


def ques10():
    sa= Map_Users[["States", "App_Opens"]]
    sa1= sa.groupby("States")["App_Opens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "App_Opens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques11():
    sa= Map_Users[["States", "App_Opens"]]
    sa1= sa.groupby("States")["App_Opens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "App_Opens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)




#Streamlit part

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])


if select == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("Simple, Fast & Secure")
        st.write("One app for all things money.")
        st.write("Pay whenever you like, wherever you like")
    with col2:
        st.video("E:\GUVI\DATASCIENCE\phonepevid.mp4")


if select == "Data Exploration":
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("**Select the Analysis Method**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.selectbox("Select the Year", Agg_Insurance["Years"].unique())

            df_agg_insur_Y= Agg_insurance_year(Agg_Insurance,years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.selectbox("Select the Quarter", df_agg_insur_Y["Quarter"].unique())
                
            Aggre_insurance_quarter(df_agg_insur_Y, quarters)

            
        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_at= st.selectbox("**Select the Year**", Agg_Transaction["Years"].unique())

            df_agg_tran_Y= Agg_insurance_year(Agg_Transaction,years_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.selectbox("Select the Quarter", df_agg_tran_Y["Quarter"].unique())

            df_agg_tran_Y_Q= Aggre_insurance_quarter(df_agg_tran_Y, quarters_at)
            
            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("Select the State",df_agg_tran_Y_Q["States"].unique())

            Aggre_Transaction_type(df_agg_tran_Y_Q,state_Y_Q)


        elif method == "User Analysis":
            year_au= st.selectbox("Select the Year_AU",Agg_Users["Years"].unique())
            agg_user_Y= Aggre_user_plot_1(Agg_Users,year_au)

            quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quarter"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State_AU**",agg_user_Y["States"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)

    with tab2:
        method_map = st.radio("Select the Analysis Method(MAP)",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        if method_map == "Map Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m1= st.selectbox("Select the Year_mi", Map_Insurance["Years"].unique())

            df_map_insur_Y= Agg_insurance_year(Map_Insurance,years_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State_mi", df_map_insur_Y["States"].unique())

            map_insure_plot_1(df_map_insur_Y,state_m1)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m1= st.selectbox("**Select the Quarter_mi**", df_map_insur_Y["Quarter"].unique())

            df_map_insur_Y_Q= Aggre_insurance_quarter(df_map_insur_Y, quarters_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m2= st.selectbox("Select the State_miy", df_map_insur_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_insur_Y_Q, state_m2)

        elif method_map == "Map Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m2= st.selectbox("**Select the Year_mi**", Map_Transaction["Years"].unique())

            df_map_tran_Y= Agg_insurance_year(Map_Transaction, years_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m3= st.selectbox("Select the State_mi", df_map_tran_Y["States"].unique())

            map_insure_plot_1(df_map_tran_Y,state_m3)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.selectbox("**Select the Quarter_mi**", df_map_tran_Y["Quarter"].unique())

            df_map_tran_Y_Q= Aggre_insurance_quarter(df_map_tran_Y, quarters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State_miy", df_map_tran_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_tran_Y_Q, state_m4)

        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("Select the Year_mu",Map_Users["Years"].unique())
            map_user_Y= map_user_plot_1(Map_Users, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("Select the Quarter_mu",map_user_Y["Quarter"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarter_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("Select the State_mu",map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu1)

    with tab3:
        method_top = st.radio("Select the Analysis Method(TOP)",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_top == "Top Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.selectbox("Select the Year_ti", Top_Insurance["Years"].unique())
 
            df_top_insur_Y= Agg_insurance_year(Top_Insurance,years_t1)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t1= st.selectbox("Select the Quarter_ti", df_top_insur_Y["Quarter"].unique())

            df_top_insur_Y_Q= Aggre_insurance_quarter(df_top_insur_Y, quarters_t1)

        
        elif method_top == "Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t2= st.selectbox("Select the Year_tt", Top_Transaction["Years"].unique())
 
            df_top_tran_Y= Agg_insurance_year(Top_Transaction,years_t2)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t2= st.selectbox("Select the Quarter_tt", df_top_tran_Y["Quarter"].unique())

            df_top_tran_Y_Q= Aggre_insurance_quarter(df_top_tran_Y, quarters_t2)

        elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t3= st.selectbox("Select the Year_tu", Top_Users["Years"].unique())

            df_top_user_Y= top_user_plot_1(Top_Users,years_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State_tu**", df_top_user_Y["States"].unique())

            df_top_user_Y_S= top_user_plot_2(df_top_user_Y,state_t3)


if select == "Top Charts":

    ques= st.selectbox("Select the Question",('Top Brands Of Mobiles Used','States With Highest Trasaction Amount',
                                                  'States With Lowest Trasaction Amount','States With Highest Trasaction Count',
                                                 'States With Lowest Trasaction Count','Districts With Highest Transaction Amount',
                                                 'Districts With Lowest Transaction Amount','Districts With Highest Transaction Count',
                                                 'Districts With Lowest Transaction Count','Top 10 States With AppOpens','Least 10 States With AppOpens'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()
        
    elif ques=="States With Highest Trasaction Amount":
        ques2()

    elif ques=="States With Lowest Trasaction Amount":
        ques3()
        
    elif ques=="States With Highest Trasaction Count":
        ques4()
        
    elif ques=="States With Lowest Trasaction Count":
        ques5()

    elif ques=="Districts With Highest Transaction Amount":
        ques6()

    elif ques=="Districts With Lowest Transaction Amount":
        ques7()
        
    elif ques=="Districts With Highest Transaction Count":
        ques8()
        
    elif ques=="Districts With Lowest Transaction Count":
        ques9()

    elif ques=="Top 10 States With AppOpens":
        ques10()

    elif ques=="Least 10 States With AppOpens":
        ques11()
