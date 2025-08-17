import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Israeli-Palestinian Fatalities Dashboard", layout="wide")
st.title("📈 Dashboard: Fatalities in the Israeli–Palestinian Conflict")

@st.cache_data
def load():
    return pd.read_csv("cleaned_fatalities.csv")

df = load()

########################################
############## Filters ###################
st.sidebar.header("Filters")
st.sidebar.markdown("Select filters to customize the dashboard")

# --- Year filter ---
year = sorted(df["year"].dropna().unique())
year_selected = st.sidebar.selectbox(
    "Choose the time period:",
    year
)

# --- Side filter ---
sides = df["citizenship"].dropna().unique().tolist()
side_selected = st.sidebar._multiselect(
    "Choose side",
    sides
)

# --- Gender filter ---
gender = df["gender"].dropna().unique().tolist()
gender_selected = st.sidebar.radio(
    "Choose gender",
    options=gender,
    index=0
)
if st.sidebar.button("❌ Reset Filters"):
    year_selected = "All"
    side_selected = "All"
    gender_selected = "All"
# --- Apply filters ---
filtered_df = df.copy()

if year_selected:
    filtered_df = filtered_df[filtered_df["year"] == year_selected]

if side_selected:
    filtered_df = filtered_df[filtered_df["citizenship"] == side_selected]

if gender_selected:
    filtered_df = filtered_df[filtered_df["gender"] == gender_selected]

#############################################
# KPIs
total_fatalities = filtered_df.shape[0]
avrg_age = filtered_df["age"].mean() if "age" in filtered_df.columns else 0

col1, col2 = st.columns(2)
col1.metric("Total Fatalities", total_fatalities)
col2.metric("Average Age", f"{avrg_age:.1f}")

############################################
################# Tabs #####################
tab1, tab2, tab3, tab4 = st.tabs(
    ["Fatalities per Year", "Fatalities per Side", "Age & Gender", "Data Table"]
)

# ----- Tab 1 -----
with tab1:
    st.subheader("📈 Deaths by Year")
    if 'year' in filtered_df.columns:
        fatalities_per_year = filtered_df.groupby('year').size().reset_index(name='count')
        fig = px.line(fatalities_per_year, x='year', y='count', markers=True,
                      labels={'year': 'السنة', 'count': 'عدد الوفيات'})
        st.plotly_chart(fig, use_container_width=True)

# ----- Tab 2 -----
with tab2:
    st.subheader("⚔️ الوفيات حسب الطرف")
    if 'citizenship' in filtered_df.columns:
        fatalities_per_side = filtered_df['citizenship'].value_counts().reset_index()
        fatalities_per_side.columns = ['citizenship', 'count']

        fig = px.bar(fatalities_per_side, x='citizenship', y='count',
                     color='citizenship', labels={'citizenship': 'الطرف', 'count': 'عدد الوفيات'})
        st.plotly_chart(fig, use_container_width=True)

        fig_pie = px.pie(fatalities_per_side, names='citizenship', values='count',
                         title='نسبة الوفيات حسب الطرف')
        st.plotly_chart(fig_pie, use_container_width=True)

# ----- Tab 3 -----
with tab3:
    st.subheader("🧑‍🤝‍🧑 توزيع الأعمار والنوع")
    if 'age' in filtered_df.columns:
        fig = px.histogram(filtered_df, x='age', nbins=20, title="توزيع الأعمار")
        st.plotly_chart(fig, use_container_width=True)

    if 'gender' in filtered_df.columns:
        gender_count = filtered_df['gender'].value_counts().reset_index()
        gender_count.columns = ['gender', 'count']
        fig = px.pie(gender_count, names='gender', values='count', title="توزيع النوع")
        st.plotly_chart(fig, use_container_width=True)

# ----- Tab 4 -----
with tab4:
    st.subheader("🗂️ الجدول الكامل")
    columns_to_show = ['name', 'age', 'gender', 'citizenship', 'date_of_death', 'notes']
    st.dataframe(filtered_df[columns_to_show])