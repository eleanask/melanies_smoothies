# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f"Customise your smoothie ")
st.write(
  """Choose your fruits
  """
)



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

name_on_order = st.text_input('name')

ingredients_list = st.multiselect(
    'choose 5', my_dataframe, max_selections = 5
)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
            ingredients_string +=fruit_chosen

            search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER )
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('submit')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


