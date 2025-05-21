# Import python packages
import requests
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

name_on_order = st.text_input('Name on smoothie:')
st.write(f'The name on your smoothie will be: {name_on_order}')

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert Snowpark Dataframe to Pandas Dataframe
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

incredient_list = st.multiselect(
    'Choose upto 5 ingredients:',
    my_dataframe,
    max_selections=5)

if incredient_list:
    # st.write(incredient_list)
    # st.text(incredient_list)
    
    incredient_string = ''
    for fruit_chosen in incredient_list:
        incredient_string += fruit_chosen + ' '

        # search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        # st.subheader(f"{fruit_chosen} Nutrition Information")

        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
       # smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        st.text(smoothiefroot_response.json())
        # sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        

    # st.write(incredient_string)
    
    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients, name_on_order)
                         values('{incredient_string}', '{name_on_order}')"""
    
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        
