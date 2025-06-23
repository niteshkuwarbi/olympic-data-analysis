import pandas as pd
import streamlit as st
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Olympics Dashboard",
                   layout="wide",
                   page_icon="🏅")

# Load Data
bios = pd.read_csv('bios.csv')
results = pd.read_csv('results.csv')
final2024 = pd.read_csv('final2024.csv')

df = preprocessor.preprocess(bios, results, final2024)

# Sidebar
with st.sidebar:
    st.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg', width=200)
    st.title("128 Years of Olympic\n1896 - 2024")
    user_menu = st.radio(
        'Navigate',
        ('📊 Medal Tally', '📈 Overall Analysis', '🌍 Country-Wise Analysis')
    )

# Medal Tally
if user_menu == '📊 Medal Tally':
    st.sidebar.header("🏅 Medal Tally")
    years, country = helper.country_wise(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    title_text = {
        ('Overall', 'Overall'): 'Overall Medal Tally',
        ('Overall', selected_country): f"{selected_country}'s Overall Performance",
        (selected_year, 'Overall'): f"Medal Tally in {selected_year} Olympics",
        (selected_year, selected_country): f"{selected_country}'s Performance in {selected_year} Olympics"
    }
    st.markdown(f"### {title_text.get((selected_year, selected_country), 'Medal Tally')}")
    st.table(medal_tally)

# Overall Analysis
if user_menu == '📈 Overall Analysis':
    st.markdown("## 📈 Overall Olympic Statistics")
    editions = df['Year'].nunique() - 1
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['name'].nunique()
    nations = df['Region'].nunique()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Editions", editions)
    col2.metric("Sports", sports)
    col3.metric("Events", events)
    col4.metric("Nations", nations)
    col5.metric("Athletes", athletes)

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["Participating Nations", "Events Over Time", "Athletes Over Time"])

    with tab1:
        nations_over_time = helper.data_over_time(df, 'Region')
        fig = px.line(nations_over_time, x='Edition', y='Region', title="Participating Nations Over Years")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        events_over_time = helper.data_over_time(df, 'Event')
        fig = px.line(events_over_time, x='Edition', y='Event', title="Events Over Years")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        athletes_over_time = helper.data_over_time(df, 'name')
        fig = px.line(athletes_over_time, x='Edition', y='name', title="Athletes Over Years")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Number of Events Over Time (per Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    event_data = df.drop_duplicates(['Year', 'Sport', 'Event'])
    heatmap_data = event_data.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    sns.heatmap(heatmap_data, annot=True, ax=ax)
    st.pyplot(fig)

    st.markdown("### Most Successful Athletes")
    sport_list = sorted(df['Sport'].dropna().unique().tolist())
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select Sport', sport_list)
    result = helper.most_successful(df, selected_sport)
    st.table(result)

# Country-wise Analysis
if user_menu == '🌍 Country-Wise Analysis':
    st.sidebar.header("🌍 Country-wise Analysis")
    country_list = sorted(df['Region'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    st.markdown(f"## {selected_country}'s Olympic Performance")

    # Line plot for medals over time
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal', title=f"{selected_country} - Medal Tally Over the Years")
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap of sports
    st.markdown(f"### {selected_country} - Strongest Sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True, ax=ax)
    st.pyplot(fig)

    # Top athletes
    st.markdown(f"### Top 10 Athletes from {selected_country}")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)
