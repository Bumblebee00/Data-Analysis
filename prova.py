import streamlit as st
import numpy as np
import pandas as pd

# display a table
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

st.write(df)

# display another table
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.table(dataframe)

# display a line chart
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

# display a slider from 0 to 10
x = st.slider('x', 0, 20, 10)
st.write(x, 'squared is', x * x)

# display an area chart
map_data = pd.DataFrame(
    np.random.randn(500, 2) / [100, 100] + [45.0703, 7.67],
    columns=['lat', 'lon'])

st.map(map_data, zoom=x)

# you can gve labels to your widgets
st.text_input("Your name", key="name")
st.session_state.name

# you can also use checkboxes to show/hide elements
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.write(chart_data)

# let the user select a number from the dataframe first column
option = st.selectbox(
    f'Which number do you like best {st.session_state.name}?',
    dataframe['col 0'])

# this is analogous to st.write()
'You selected: ', option

# if instead of st.slider() you create st.sidebar.slider() the widget will be in the sidebar
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'what crypto is your favorite?',
    ('Bitcoin', 'Ethereum', 'Dogecoin')
)

if add_selectbox == 'Bitcoin':
    st.sidebar.write('yeee')
else:
    st.sidebar.write('study bitcoin....')


left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
greet = left_column.button('Press me!')
if greet:
    left_column.write('ciao %s' % np.random.choice(['Giorgio', 'Piero', 'Paolo']))


# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

# st.expander lets you conserve space by hiding away large content.
