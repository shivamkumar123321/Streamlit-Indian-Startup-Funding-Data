import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit import columns, pyplot
import seaborn as sns

st.set_page_config(layout='wide',page_title='StartUp Analysis',page_icon="❤️",initial_sidebar_state="expanded")

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


def load_overall_analysis():
    st.title('Overall Analysis')

    # Total money invested in Indian Startup
    Total = round(df['amount'].sum())

    # Maximum amount infused in Startup
    Max_amount = round(df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).iloc[0])

    # Total funded startup
    Total_startups = df['startup'].nunique()

    # Avg Ticket size
    Avg_ticket = round(Total / Total_startups)

    col1, col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(Total) + "cr")

    with col2:
        st.metric('Max Amount',str(Max_amount) + "cr")

    with col3:
        st.metric('Total Funded Startup', str(Total_startups) + "cr")

    with col4:
        st.metric('Average Fund',str(Avg_ticket) + "cr")

    st.header('MOM Graph')
    option = st.selectbox('Select Type',['Total','Count'])
    if option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig3)

    st.header('Sector Analysis Pie')

    options = st.selectbox('Select one',['Count','Sum'])
    if options == 'Count':
        sector_data = df.groupby('vertical')['amount'].count().sort_values(ascending=False).head(5)
    else:
        sector_data = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(5)

    fig, ax = plt.subplots()
    ax.pie(sector_data,labels=sector_data.index, autopct='%1.1f%%',explode=[0.1,0,0,0,0],shadow = True)
    st.pyplot(fig)

# Type of Funding and City wise Funding
    df['round'] = df['round'].str.lower()
    df['round'] = df['round'].str.replace('seed funding', 'seed')
    df['round'] = df['round'].str.replace('seed/ angel funding', 'seed')
    df['round'] = df['round'].str.replace('seed / angel funding', 'seed')
    df['round'] = df['round'].str.replace('seed/angel funding', 'seed')
    df['round'] = df['round'].str.replace('seed / angle funding', 'seed')
    df['round'] = df['round'].str.replace('angel / seed funding', 'seed')
    df['round'] = df['round'].str.replace('angel round', 'angel')
    df['round'] = df['round'].str.replace('angel funding', 'angel')
    df['round'] = df['round'].str.replace('angel round', 'angel')
    df['round'] = df['round'].str.replace('angel / seed', 'angel')
    df['round'] = df['round'].str.replace('structured debt', 'debt funding')
    df['round'] = df['round'].str.replace('term loan', 'debt funding')
    df['round'] = df['round'].str.replace('debt-funding', 'debt funding')
    df['round'] = df['round'].str.replace('debt and preference capital', 'debt funding')

    types_of_funding = df['round'].unique()

    city_wise_funding = sorted(df['city'].unique())

    # Top year wise funded startup
    year_wise = (df.loc[df.groupby('year')['amount'].idxmax(), ['year', 'startup', 'amount']]
                 .sort_values(by='year').reset_index(drop=True).set_index('year'))

    # Overall top funded startup
    overall = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(6)

    fund,year ,city,over = columns([1,3,1,2])

    with fund:
        st.markdown('**Funding Types**')
        st.dataframe(types_of_funding)

    with year:
        st.markdown('**Top year wise funded Startup**')
        st.dataframe(year_wise)

    with city:
        st.markdown('**City wise funding**')
        st.dataframe(city_wise_funding)

    with over:
        st.markdown('**Top funded Startup**')
        st.dataframe(overall)

# Investor and heatmap
    invest,heat = columns([1,2])

    with invest:
        st.subheader('Top Investor Chart')
        x = df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(16)
        st.dataframe(x)

    with heat:
        # Aggregate data: total funding amount by city and round type
        funding_heatmap_data = df.pivot_table(
            index='city',
            columns='round',
            values='amount',
            aggfunc='sum'
        ).fillna(0)

        # Streamlit application
        st.subheader('Funding Heatmap')
        # Plotting the heatmap
        fig, ax = plt.subplots()
        sns.heatmap(funding_heatmap_data, cmap='YlGnBu', annot=False, cbar=True, ax=ax)

        # Customize the heatmap
        ax.set_title('Funding Heatmap by City and Round Type', fontsize=16)
        ax.set_xlabel('Funding Round', fontsize=12)
        ax.set_ylabel('City', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Display the heatmap in Streamlit
        st.pyplot(fig)

def load_investor_analysis():
    st.title('Investor analysis')
    if investor:
        st.subheader(investor)

    # Top 5 Recent investment
    last5_df = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1,col2 = columns([1,2])

    with col1:
        # Top 5 Biggest investment
        top_5 = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('TOP 5 investment')
        st.dataframe(top_5)

    with col2:
        pie_graph = st.selectbox('Select one PIE chart', ['Sector', 'Stage', 'City'])

        if pie_graph == 'Sector':

            sector_pie = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)

            fig, ax = plt.subplots()
            ax.pie(sector_pie, labels=sector_pie.index, autopct='%1.1f%%')
            ax.set_title('Investment in top sector ')
            st.pyplot(fig)

        elif pie_graph == 'Stage':

            round_pie = df[df['investors'].str.contains(investor, na=False)].groupby('round')[
                'amount'].sum().sort_values(ascending=False).head(10)

            fig, ax = plt.subplots()
            ax.pie(round_pie, labels=round_pie.index, autopct='%1.1f%%')
            ax.set_title('Investment in top stages ')
            st.pyplot(fig)

        else:
            city_pie = df[df['investors'].str.contains(investor, na=False)].groupby('city')[
                'amount'].sum().sort_values(ascending=False).head(10)

            fig, ax = plt.subplots()
            ax.pie(city_pie, labels=city_pie.index, autopct='%1.1f%%')
            ax.set_title('Investment in top stages ')
            st.pyplot(fig)

    st.subheader('YOY Invesment Report')

    df['year'] = df['date'].dt.year
    yoy_graph = df.groupby('year')['amount'].sum()

    fig1,ax1 = plt.subplots()
    ax1.plot(yoy_graph.index,yoy_graph.values)
    ax1.set_title('Year on year Investment in India')
    ax1.set_xlabel("years")
    ax1.set_ylabel("amount in CR")
    st.pyplot(fig1)

def load_startup_analysis():

    st.title('Startup analysis')
    st.subheader('Startup Information')
    colX,colY = st.columns(2)

    with colX:
        if name:
            location = df[df['startup'] == name]['city'].tolist()
            st.metric('name',str(name))

    with colY:
        st.metric('location',str(location))

    colA, colB = st.columns(2)

    with colA:
        if name:
            verticle = df[df['startup'] == name]['vertical'].tolist()
            st.metric('Verticle', str(verticle))

    with colB:
        subverticle = df[df['startup'] == name]['subvertical'].tolist()
        st.metric('Subverticle', str(subverticle))

    st.subheader('Funding Round')
    com_detail = df[df['startup'] == name][['date', 'round', 'investors', 'amount']].set_index('date').sort_index()
    st.dataframe(com_detail)

    # st.subheader('Competitor')
    # verticle = df[df['startup'] == name]['vertical'].tolist()
    # xx = df[df['vertical'] == verticle]['startup'].unique().tolist()
    # st.metric('Competitor',str(xx))



st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select one',['Overall Analysis','Investor','StartUp'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Investor':
    investor = st.sidebar.selectbox('Select Investor name', df['investors'])
    load_investor_analysis()
else:
    name = st.sidebar.selectbox('Select StartUp name', df['startup'].unique())
    load_startup_analysis()





















































































































































