import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')

st.title('Class17')

st.header('Data')
st.write('this section is for showing data structure')

df = pd.read_excel('./sample_-_superstore.xls')
cond = df['Country/Region']=='United States'
df = df[cond]

# st.write(df.head(3))
all_states = df['State/Province'].unique()
target_states = st.multiselect('Choose States', options=all_states, 
                               default=['North Carolina','South Carolina'])

df = df[df['State/Province'].isin(target_states)]
#connecting target states with later visualizations
# by slicing df based on target states

st.header('Visualizations')

col1, col2 = st.columns([7,3])
with col1:
    profit_sums_state = df.groupby('State/Province')['Profit'].sum()
    sales_sums_state = df.groupby('State/Province')['Sales'].sum()
    profit_margin_state = profit_sums_state/sales_sums_state
    profit_margin_state = profit_margin_state.reset_index(name='Profit Margin')
    fig1 = px.choropleth(
        locations = profit_margin_state['State/Province'],
        locationmode='USA-states',
        scope='usa',
        color=profit_margin_state["Profit Margin"]
    )
    st.plotly_chart(fig1, width='stretch')

with col2:
    sales_sums_cat = df.groupby('Category')['Sales'].sum()

    profit_sums_cat = df.groupby('Category')['Profit'].sum()

    profit_margin_cat = profit_sums_cat / sales_sums_cat



    fig2 = px.bar(
        x=profit_margin_cat.index,
        y=profit_margin_cat.values,
        color=profit_margin_cat.index,
        labels={'x': 'Category', 'y': 'Profit Margin'}
    )
    st.plotly_chart(fig2, width='stretch')
col3, col4 = st.columns([5,5])
with col3:
    df['YM'] = pd.to_datetime(df['Order Date']).dt.strftime('%Y-%m')
    a = df.groupby(['Category', 'YM'])['Profit'].sum()
    b = df.groupby(['Category', 'YM'])['Sales'].sum()
    profit_margin_cat_ym = a/b
    profit_margin_cat_ym = profit_margin_cat_ym.reset_index(name='Profit Margin')

    fig3 = px.line(
    profit_margin_cat_ym,
    x='YM',
    y='Profit Margin',
    color='Category')
    st.plotly_chart(fig3, width='stretch')
with col4:
    fig4 = px.treemap(
    df,
    path=['Category', 'Sub-Category'],
    values='Sales',
    color='Category')

    st.plotly_chart(fig4, width='stretch')
