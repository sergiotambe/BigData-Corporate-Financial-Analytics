import pandas as pd
import streamlit as st


# Load and cache data
@st.cache_data
def load_data():
    # Load the dataframe already created
    merged_df = pd.read_csv('data/merged_df.csv')

    return merged_df

def filter_quarter(key_prefix="q"):
    quarters_2024 = [f"2024 Q{q}" for q in range(1, 5)]
    import streamlit as st  # necessario se usi la funzione all'interno di un modulo esterno

    col1, col2 = st.columns(2)
    with col1:
        start_quarter = st.selectbox("Start Quarter", quarters_2024, index=0, key=f'{key_prefix}_start')
    with col2:
        end_quarter = st.selectbox("End Quarter", quarters_2024, index=3, key=f'{key_prefix}_end')

    return start_quarter, end_quarter
