
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Social Media & Mental Health Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("Student Social Media And Mental Health Impact.csv")

df = load_data()

st.title("📊 Student Social Media & Mental Health Dashboard")

st.sidebar.header("Filter")
gender = st.sidebar.multiselect("Gender", sorted(df["Gender"].dropna().unique()))
country = st.sidebar.multiselect("Country", sorted(df["Country"].dropna().unique()))

filtered = df.copy()
if gender:
    filtered = filtered[filtered["Gender"].isin(gender)]
if country:
    filtered = filtered[filtered["Country"].isin(country)]

c1, c2, c3 = st.columns(3)
c1.metric("Jumlah Data", len(filtered))
c2.metric("Rata-rata Mental Health Score", round(filtered["Mental_Health_Score"].mean(), 2))
c3.metric("Rata-rata Daily Usage", round(filtered["Avg_Daily_Usage_Hours"].mean(), 2))

st.subheader("Preview Data")
st.dataframe(filtered, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.scatter(
        filtered,
        x="Avg_Daily_Usage_Hours",
        y="Mental_Health_Score",
        color="Gender",
        title="Penggunaan Media Sosial vs Mental Health Score"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.box(
        filtered,
        x="Stress_Level",
        y="Mental_Health_Score",
        title="Mental Health Score berdasarkan Stress Level"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Platform yang Paling Sering Digunakan")
platform = filtered["Most_Used_Platform"].value_counts().reset_index()
platform.columns = ["Platform", "Jumlah"]
fig3 = px.bar(platform, x="Platform", y="Jumlah")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Korelasi Numerik")
numeric_df = filtered.select_dtypes(include="number")
st.dataframe(numeric_df.corr().round(2))
