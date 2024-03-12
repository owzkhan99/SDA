import pandas as pd
import streamlit as st

import plotly.express as px



df = pd.read_csv('vehicles_us.csv')

#drop the column containing 'date posted'
df = df.drop(df.columns[11], axis=1)

#dropping rows where the model_year is older than 1950
# Identifying the index of rows where model_year is older than 1950
index_to_drop = df[df['model_year'] < 1950].index
# Dropping these rows
df.drop(index_to_drop, axis='rows', inplace=True)

#separate the make and model strings into new columns
df[['make','model']] = df['model'].str.split(" ", n=1, expand=True)


#visualization starts here

st.header('Analysis of Vehicle Markets')
st.write('Filter by vehicle make in the drop down below')

#create a dropdown selection filtered by vehicle make/brand
make_options = df['make'].unique()

selected_make = st.selectbox('Select a make', make_options)


#create a slider to filter year range
min_year, max_year = int(df['model_year'].min()), int(df['model_year'].max())

year_range = st.slider("Choose Year Range", value=(min_year, max_year), min_value = min_year, max_value = max_year)

actual_range = list(range(year_range[0], year_range[1]+1))

#specify the range of vehicles to be shown after filtering
df_filtered = df[ (df.make == selected_make) & (df.model_year.isin(list(actual_range)) )]

st.dataframe(df_filtered)




#moving on to price analysis
st.header('Price Analysis')
st.write('Here is a look at how different variables impact the price of the vehicle')

list_for_hist = ['condition', 'transmission', 'type']

selected_variable = st.selectbox('Select a variable', list_for_hist)


check = st.checkbox('Exclude cars over $50,000')
# Conditional to filter the dataframe based on the checkbox.
if check:
    df_filtered = df[df['price'] <= 50000]
else:
    df_filtered = df

fig1 = px.histogram(df_filtered, x="price", color=selected_variable)
fig1.update_layout(title="<b> Visual of price by {}</b>".format(selected_variable))
st.plotly_chart(fig1)




#moving on to scatterplot analysis of different variables

#adding a column that calculates age of vehicle from the max value of the model_year
df['age'] = 2019 - df['model_year']

#creating a function that separates vehicles into ranges by their age in years
def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'


st.write('Visualizing price with scatterplots from various parameters')

df['age_category'] = df['age'].apply(age_category)

list_for_scatter = ['odometer', 'cylinders', 'days_listed']

choice_for_scatter = st.selectbox('Select a variable', list_for_scatter)

fig2 = px.scatter(df, x= "price", y= choice_for_scatter, color= "age_category", hover_data=['model_year'], range_x=[0, 100000])
fig2.update_layout(title= "<b> Visual of price by {}</b>".format(choice_for_scatter))

st.plotly_chart(fig2)





#This next histogram will visualize odometer vs. various conditions

st.header('Analysis of Listings by odometer values')
st.write('Select a variable to compare vehicle mileage')

check = st.checkbox('Exclude cars over 300k miles')
# Conditional to filter the dataframe based on the checkbox.
if check:
    df_filtered = df[df['odometer'] <= 300000]
else:
    df_filtered = df


list_for_hist2 = ['condition', 'transmission', 'type']

selected_variable2 = st.selectbox('Vehicle Characteristic', list_for_hist2)

fig3 = px.histogram(df_filtered, x="odometer", color= selected_variable2)
fig3.update_layout(title= "<b> Visual of odometer by {}</b>".format(selected_variable2))

st.plotly_chart(fig3)





#This visual will compare average price by 'type' and 'make'

st.header('How does the vehicle type and make affect the average list price?')

avg_price_type = df.groupby('type')['price'].mean().reset_index()
avg_price_make = df.groupby('make')['price'].mean().reset_index() 

data_for_barplot = {
    "type": avg_price_type, 
    "make": avg_price_make
}

list_for_barplot = ['type', 'make']

selected_variable3 = st.selectbox('Vehicle Characteristic', list_for_barplot)

fig4 = px.bar(data_for_barplot[selected_variable3], x="price", color=selected_variable3)
fig4.update_layout(title= "<b> Visual of average price by {}</b>".format(selected_variable3))

st.plotly_chart(fig4)





