import streamlit as st
import pickle
import pandas as pd
import numpy as np
import joblib

# Load the saved model
loaded_pipe = joblib.load('pipe.pkl')
pipe = loaded_pipe
loaded_df = joblib.load('df.pkl')
df = loaded_df


# Create a function for prediction
def predict_price(name, os, processor, generation, ram, ssd, hdd, display):
    input_data = pd.DataFrame([[name, os, processor, generation, ram, ssd, hdd, display]],
                              columns=['name', 'os', 'processor', 'generation', 'ram', 'ssd', 'hdd', 'display'])
    log_price = pipe.predict(input_data)[0]
    price = round(np.exp(log_price))
    return price


# Streamlit app
def main():
    st.title('Laptop Price Prediction')

    # Input form
    st.sidebar.header('Input details')

    name = st.sidebar.selectbox('Brand Name', df['name'].unique(), index=None)

    # Update options based on the selected brand
    processor_options = df['processor'].unique()
    os_options = df['os'].unique()

    if name == 'apple':
        apple_processors = ['apple m1 processor', 'apple m2 processor', 'apple m1 max', 'apple m1 pro', 'apple m2 pro']
        processor_options = apple_processors
        os_options = ['mac']
        generation = [None]
    else:
        processor_options = df['processor'].unique()
        os_options = df['os'].unique()
        # Exclude specific options
        exclude_processors = ['apple m1 processor', 'apple m2 processor', 'apple m1 max', 'apple m1 pro',
                              'apple m2 pro']

        df_filtered = df[~df['processor'].isin(exclude_processors)]
        processor_options = df_filtered['processor'].unique()

        os_options = os_options[os_options != 'mac']

        # os_options = df['os'].unique()

    os = st.sidebar.selectbox('Operating System', os_options, index=None)
    processor = st.sidebar.selectbox('Processor', processor_options, index=None)
    generation = st.sidebar.selectbox('Generation', [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], index=None)
    ram = st.sidebar.selectbox('RAM', [2, 4, 6, 8, 12, 16, 24, 32, 64], index=None)
    hdd = st.sidebar.selectbox('HDD', [0, 128, 256, 512, 1024, 2048], index=None)
    ssd = st.sidebar.selectbox('SSD', [0, 8, 128, 256, 512, 1024, 2048, 4096], index=None)
    display = st.sidebar.number_input('Display size')

    # Prediction
    if st.sidebar.button('Predict'):
        price = predict_price(name, os, processor, generation, ram, ssd, hdd, display)
        st.success(f'Predicted Price: {price} INR')


if __name__ == '__main__':
    main()
