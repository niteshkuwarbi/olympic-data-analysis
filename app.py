import pandas as pd
import streamlit as st
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

bios = pd.read_csv('bios.csv')
results = pd.read_csv('results.csv')
final2024 = pd.read_csv('final2024.csv')

df = preprocessor.preprocess(bios, results, final2024)

st.sidebar.title("128 Years of Olympic \n 1896 - 2024")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_wise(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' overall performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' performance in ' + str(selected_year) + ' Olympics')
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    sports = df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    athletes = df['name'].unique().shape[0]
    nations = df['Region'].unique().shape[0]

    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Sports')
        st.title(sports)
    with col3:
        st.header('Events')
        st.title(event)

    col1, col2 = st.columns(2)
 
    with col1:
        st.header('Nations')
        st.title(nations)
    with col2:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'Region')
    fig = px.line(nations_over_time, x='Edition', y='Region')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'name')
    fig = px.line(athletes_over_time, x='Edition', y='name')
    st.title('Athletes over the years')
    st.plotly_chart(fig)

    st.title('No. of Events over time(every sport)')
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select any Sport', sport_list)
    result = helper.most_successful(df, selected_sport)
    st.table(result)


if user_menu == 'Country-Wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['Region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title('The Medal Tally of ' + selected_country + ', over the years')
    st.plotly_chart(fig) 

    st.title(selected_country + ' excels in the following sports')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title('Top 10 Athletes of ' + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

