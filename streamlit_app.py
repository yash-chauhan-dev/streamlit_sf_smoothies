# Import python packages
import streamlit as st
import requests
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on'))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients = st.multiselect(
    "choose upto 5 ingredients:",
    my_dataframe,
    max_selections =5
)

if ingredients:
    
    ingredients_str = ''
    
    for fruit in ingredients:
        ingredients_str += fruit + ' '
        search_on=pd_df.loc[pd_df['fruit_name']==fruit, 'search_on'].iloc[0]
        st.subheader(fruit + "Nutrition Information")
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)
    
    st.write(ingredients_str)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_str + """', '""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your smoothie is ordered", icon='✅')


smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)
