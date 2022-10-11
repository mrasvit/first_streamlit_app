import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected=streamlit.multiselect('Pick some fruits":',list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(user_fruit_choice):
    #import requests
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+user_fruit_choice)
    #just writes the data on the screen
    #streamlit.text(fruityvice_response.json())

    #to display json data in the tabular format
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header('Fruityvice fruit Advice')
try:
    fruit_choice = streamlit.text_input('what fruit would you like information about?','Kiwi')
    if fruit_choice:
        streamlit.write('The user entered',fruit_choice)
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
    else:
        streamlit.error('Please select a fruit to get information.')
        
except URLError as e:
    streamlit.error()

#streamlit.stop()

#import snowflake.connector
streamlit.header('From Snowflake')

streamlit.header('View Our Fruit List - Add Your Favorites!')

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

#streamlit.stop()

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
        return 'Thanks for adding '+ new_fruit

add_fruit = streamlit.text_input('Please type the fruit name you like to add?')
if streamlit.button('Add Fruit'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
