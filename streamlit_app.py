# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie')
st.write('Your name on your order will be: ', name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=6
)

if ingredients_list:
    ingredients_string = ''
    for ingredient in ingredients_list:
        ingredients_string += ingredient + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""


    time_to_insert = st.button('Submit Order')
    
    if time_to_insert and ingredients_string and name_on_order:
        session.sql(my_insert_stmt).collect()

        st.success('Your smoothie is ordered!')
    st.write(my_insert_stmt) 

