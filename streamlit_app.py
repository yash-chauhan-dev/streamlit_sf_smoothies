# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in custom Smoothie!
    """
)


name_on_order = st.text_input("Name on smoothie:")
st.write("Name on smoothie will be: ", name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
ingredients = st.multiselect(
    "choose upto 5 ingredients:",
    my_dataframe,
    max_selections =5
)

if ingredients:
    
    ingredients_str = ''
    
    for fruit in ingredients:
        ingredients_str += fruit + ' '
    
    st.write(ingredients_str)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_str + """', '""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your smoothie is ordered", icon='✅')
