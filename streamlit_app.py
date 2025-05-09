# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(f" :cup_with_straw: Customize Your Smoothie :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)
name_on_order= st.text_input("Name on Smoothie")
st.write(f"The name on your smoothie will be: {name_on_order} ")



# st.write("You selected:", option)
cnx= st.connection("snowflakes")

session = cnx.session()
# edited_dataset = session.create_dataframe(editable_df)
# og_dataset.merge(edited_dataset
#                      , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
#                      , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
#                     )
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose upto 5 ingredients:',
                                my_dataframe,max_selections=5)
if ingredients_list:
    # st.text(ingredients_list)
    ingredients_string=' '
    for fruits_chose in ingredients_list:
        ingredients_string += fruits_chose + ' '
    # st.write(ingredients_string)
    time_to_insert = st.button('Sumbit Order')

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order +"""')"""

    # st.write(my_insert_stmt)
    # st.stop( )
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")   
