# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie')
st.write('Your name on your order will be: ', name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=6
)

if ingredients_list:
    ingredients_string = ''
    for ingredient in ingredients_list:

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == ingredient, 'SEARCH_ON'].iloc[0]
        st.write('The Search Value for ', ingredient, ' is ', search_on)


        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ingredient)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


        ingredients_string += ingredient + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""


    time_to_insert = st.button('Submit Order')
    
    if time_to_insert and ingredients_string and name_on_order:
        session.sql(my_insert_stmt).collect()

        st.success('Your smoothie is ordered!')
    st.write(my_insert_stmt) 

