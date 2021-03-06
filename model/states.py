# Dependencies
import pandas as pd
import streamlit as st
import model_dependencies.segmentation_dependecy as segmentRevolver

from inform import Descriptions

def display_customer_segmentation():

    """
    display_customer_segmentation() brings every
    function together such that the code is 
    cleaner.
    """

    st.title("States")
    st.markdown('---')

    data = select_user_journey()

    if (data is not None):

        # Display Data
        display_data_being_used(data)

        # CART Targets
        target_dict = define_cart_targets(data)

        if (target_dict is not None):
            # Running CART
            apply_cart(data, target_dict)
            # st.write(snippet)
        
        else:
            st.warning('Waiting to press the Submit Button!')

    else: 
        st.markdown('---')
        st.warning('Before we start, you need to feed the algorithm some data!')

def select_user_journey():

    """
    select_user_journey() responsable for defining if the user 
    wants to drag and drop his data or if he wants to use data collected
    by the authors.
    """

    c1, c2 = st.columns((2, 1))
    c1.header('Input')

    c2.header('Description')
    c2.info(Descriptions.CART_ABOUT)

    c2.error(Descriptions.CART_INPUT)
    c2.success(Descriptions.CART_OUTPUT)

    # Option to decide whether or not to use data generated by us
    data_options = ['Import own data', 'Use data collected by authors']
    data = c1.radio('Which data would you like the model to consider?', data_options)

    if (data == data_options[0]):

        # Own Data
        upload = c1.file_uploader("Upload Dataframe", type=["csv"], key='competitor_data')
        #data = pd.read_csv("data/datasets/dummy/cart/weatherAUS 3.csv")

        if (upload is not None):
            data = pd.read_csv(upload).iloc[: , 1:]
            return data

    else:
        # Input Data
        data = pd.read_csv('data/datasets/official/customer_segmentation/segments.csv').iloc[: , 1:]
        return data

def define_cart_targets(data):

    """
    define_cart_targets() get input from user. The input here
    are the parameters for the CART Algorithm.
    """
    st.markdown('---')
    st.markdown('## Define CART Targets')

    target_columns = st.multiselect("Pick which Columns should be used to create the segmentations", data.columns, help = Descriptions.SOLVERS, key = "target_cart_columns")
    target_y = st.selectbox("Pick the target variable", data.columns)

    if st.button("Apply CART"):
        target_dict = dict()
        target_dict['target_columns'] = target_columns
        target_dict['target_y'] = target_y
        return target_dict

def apply_cart(data, target_dictionary):
    """Calls CART Implementation"""
    snippet = segmentRevolver.segment_customer_using(data, target_dictionary.get('target_columns'), target_dictionary.get('target_y'))
    st.success('CART was succesful!')
    return snippet

def display_data_being_used(data):
    st.markdown('---')
    st.write('## Data Overview')
    st.write(data)