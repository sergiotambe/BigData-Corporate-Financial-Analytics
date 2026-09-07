import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.express import colors
from utils.data_load import load_data, filter_quarter
import os


st.set_page_config(
    page_title="Sergio Tambè Homework #3",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("""
<div style='text-align: center;'>
    <h2 style='color: black;'>Data Science - BigData Analytics<br>Sergio Tambè 1000084729</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center'>
    <img src='https://images.squarespace-cdn.com/content/v1/60056c48dfad4a3649200fc0/1613294634908-3HTA3TR74HYYSNEIZSIJ/UniCT-Logo.jpg' width=500>
    <h3 style='color: black;'>Department of Mathematics and Computer Science</h3>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data2():
    df = load_data()
    df['Quarter'] = df['year'].astype(str) + ' Q' + df['quarter'].astype(str)
    return df

df = load_data2()
quarters_2024 = [f"2024 Q{q}" for q in range(1, 5)]

def filter_by_quarter(df, start_q_label, end_q_label):
    start_q = int(start_q_label.split('Q')[1])
    end_q = int(end_q_label.split('Q')[1])
    return df[(df['year'] == 2024) & (df['quarter'] >= start_q) & (df['quarter'] <= end_q)].copy()


def classify_manual_question(question):
    q = question.lower()
    if "symbol" in q or "compan" in q:
        return "symbols"
    elif "sector" in q:
        return "sectors"
    elif "industry" in q or "industries" in q:
        return "industries"
    else:
        return "unknown"



################### PAGE 1 - TIME ANALYSIS ###################
def time_analysis(df):
    st.title("🕒 Time Analysis")
    st.subheader("Time Analysis with Interactive Filters")

    ### LINE CHART ###
    st.subheader("Transaction Trends (quarter)")
    start_q_line, end_q_line = filter_quarter(key_prefix="line")

    df_line = filter_by_quarter(df, start_q_line, end_q_line)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("N. Transactions", f"{len(df_line):,}")
    with col2:
        st.metric("🛒 Purchases", f"{len(df_line[df_line['transactiontype'] == 'BUY']):,}")
    with col3:
        st.metric("💸 Sales", f"{len(df_line[df_line['transactiontype'] == 'SELL']):,}")
    with col4:
        st.metric("📦 Total Units", f"{df_line['units'].sum():,}")

    qt = df_line.groupby(['year', 'quarter']).size().reset_index(name='Number of Transactions')
    qt['Quarter'] = qt['year'].astype(str) + ' Q' + qt['quarter'].astype(str)
    fig_line = px.line(qt, x='Quarter',
                       y='Number of Transactions',
                       title='Quarterly Number of Transactions',
                       markers=True
                       )
    fig_line.update_traces(
        line=dict(width=8, color = '#5ec962'),
        marker=dict(size=15, color='#d43e4e')
        )
    fig_line.update_traces(line=dict(width=8))
    fig_line.update_layout(hovermode='x unified')
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    
    col_manual, col_predef = st.columns(2)

    with col_predef:
        st.subheader("📌 Example of Questions")
        example_question = st.selectbox("Example of questions:", [
            "What are the top symbols for transactions volume?",
            "What are the top sectors by transaction volume?",
            "What are the top industries by transaction volume?",
            "Top company",
            "Top companies",
            "Tell me the top sectors by transaction",
            "Tell me what are the top industries"
        ], key="example_question_box")

    with col_manual:
        st.subheader("🧠 Ask a Question")
        user_question = st.text_input(
            "Write your question:",
            value=example_question,
            key="manual_question_input"
        )


    # 🔍 Domanda manuale
    if user_question:
        category = classify_manual_question(user_question)

        start_q_nl, end_q_nl = filter_quarter(key_prefix="nl")

        df_nl = filter_by_quarter(df, start_q_nl, end_q_nl)

        if category == "symbols":
            available = df_nl['symbol'].nunique()
            num = st.slider("Select number of top symbols", 1, available, 3, key="nl_slider_symbols")
            top_data = df_nl['symbol'].value_counts().head(num)
            st.subheader(f"Top {num} Companies (symbols)")
            fig = px.bar(
                x=top_data.index,
                y=top_data.values,
                title="Top Symbols by Number of Transactions",
                labels={'x': 'Symbols', 'y': 'Number of Transactions'},
                color=top_data.values,
                color_continuous_scale="Cividis", text_auto=True
            )
            fig.update_traces(marker_line_color='black', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True)

        elif category == "sectors":
            available = df_nl['sector'].nunique()
            num = st.slider("Select number of top sectors", 1, available, 5, key="nl_slider_sectors")
            top_data = df_nl['sector'].value_counts().head(num)
            st.subheader(f"Top {num} Sectors")
            fig = px.bar(
                x=top_data.index,
                y=top_data.values,
                title="Top Sectors by Number of Transactions",
                labels={'x': 'Sectors', 'y': 'Number of Transactions'},
                color=top_data.values,
                color_continuous_scale="Cividis", text_auto=True
            )
            fig.update_traces(marker_line_color='black', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True)

        elif category == "industries":
            available = df_nl['industry'].nunique()
            num = st.slider("Select number of top industries", 1, available, 5, key="nl_slider_industries")
            top_data = df_nl['industry'].value_counts().head(num)
            st.subheader(f"Top {num} Indutries")
            fig = px.bar(
                x=top_data.index,
                y=top_data.values,
                title="Top Industries by Number of Transactions",
                labels={'x': 'Industries', 'y': 'Number of Transactions'},
                color=top_data.values,
                color_continuous_scale="Cividis", text_auto=True
            )
            fig.update_traces(marker_line_color='black', marker_line_width=2)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("❓ I couldn't understand your question. Try using keywords like 'symbols', 'sectors', or 'industries'.")


################### PAGE 2 - COUNTRY ANALYSIS ###################
def country_analysis(df):
    st.title("🌍 Country Analysis")
    st.subheader("Transaction Analysis by Country of Origin")

    countries = sorted(df['name'].dropna().unique())
    selected_country = st.selectbox("Select Country", countries, index=countries.index('United States of America') if 'United States of America' in countries else 0)

    st.subheader(f"Quarterly Trends in {selected_country}")
    start_q_line2, end_q_line2 = filter_quarter(key_prefix="line2")

    df_country = df[(df['name'] == selected_country) & (df['year'] == 2024)]
    df_line = filter_by_quarter(df_country, start_q_line2, end_q_line2)

    qt = df_line.groupby(['year', 'quarter']).size().reset_index(name='Number of Transactions')
    qt['Quarter'] = qt['year'].astype(str) + ' Q' + qt['quarter'].astype(str)
    fig_line = px.line(qt,
                       x='Quarter',
                       y='Number of Transactions',
                       title=f'Quarterly Transactions in {selected_country}',
                       markers=True
                       )
    fig_line.update_traces(
        line=dict(width=8, color = '#5ec962'),
        marker=dict(size=15, color='#d43e4e')
        )
    fig_line.update_traces(line=dict(width=8))
    fig_line.update_layout(hovermode='x unified')
    st.plotly_chart(fig_line, use_container_width=True)

    # BUY CHART
    note_text = "*Note: The color gradient represents the number of transactions (lighter for lower values, darker for higher values).*"

    st.subheader(f"BUY Transactions in {selected_country}")
    start_q_buy, end_q_buy = filter_quarter(key_prefix="buy")

    df_buy = filter_by_quarter(df_country, start_q_buy, end_q_buy)
    buy_df = df_buy[df_buy['transactiontype'] == 'BUY']
    available_ind_buy = buy_df['industry'].nunique()
    num_ind_buy = st.slider(f"Select Number of Top Industries", min_value=1, max_value=available_ind_buy,
                            value=5 if available_ind_buy >5 else available_ind_buy,
                            key='ind_buy')
    top_ind_buy = buy_df.groupby('industry').size().sort_values(ascending=False).head(num_ind_buy)  
    less5_buy = f'⚠️ There are only {available_ind_buy} Industries that have bought something in {selected_country}' if available_ind_buy < 5 else f'📈 There are {available_ind_buy} Industries that have bought something in {selected_country}'
    st.subheader(f"Top {num_ind_buy} Industries between {start_q_buy} and {end_q_buy}")
    st.markdown(less5_buy)

    fig_buy = px.bar(x=top_ind_buy.index,
                     y=top_ind_buy.values,
                     title=f"Top {num_ind_buy} Industries (BUY) in {selected_country}",
                     labels={'x': 'Industry', 'y': 'Number of BUY Transactions'},
                     color=top_ind_buy.values,
                     color_continuous_scale="Cividis", text_auto=True
                     )
    fig_buy.update_layout(height=600) 
    fig_buy.update_traces(marker_line_color='black', marker_line_width=2) 
    st.plotly_chart(fig_buy, use_container_width=True)

    # SELL CHART
    st.subheader(f"SELL Transactions in {selected_country}")

    start_q_sell, end_q_sell = filter_quarter(key_prefix="sell")

    df_sell = filter_by_quarter(df_country, start_q_sell, end_q_sell)
    sell_df = df_sell[df_sell['transactiontype'] == 'SELL']
    available_ind_sell = sell_df['industry'].nunique()
    num_ind_sell = st.slider(f"Select Number of Top Industries", min_value=1, max_value=available_ind_sell,
                             value=5 if available_ind_sell >5 else available_ind_sell,
                             key='ind_sell')
    top_ind_sell = sell_df.groupby('industry').size().sort_values(ascending=False).head(num_ind_sell)  
    less5_sell = f'⚠️ There are only {available_ind_sell} Industries that have sold something in {selected_country}' if available_ind_sell < 5 else f'📈 There are {available_ind_sell} Industries that have sold something in {selected_country}'
    st.subheader(f"Top {num_ind_sell} Industries between {start_q_sell} and {end_q_sell}")    
    st.markdown(less5_sell)


    fig_sell = px.bar(x=top_ind_sell.index,
                      y=top_ind_sell.values,
                      orientation='v', 
                      title=f"Top {num_ind_sell} Industries (SELL) in {selected_country}",
                      labels={'x': 'Industry', 'y': 'Number of SELL Transactions'},
                      color=top_ind_sell.values,
                      color_continuous_scale="Plasma", text_auto=True
                      )
    fig_sell.update_layout(height=600) # Altezza aggiornata a 600 per coerenza
    fig_sell.update_traces(marker_line_color='black', marker_line_width=2) 
    st.plotly_chart(fig_sell, use_container_width=True)
    st.markdown(note_text)



################### APP NAVIGATION ###################
def main():
    df = load_data2()

    st.sidebar.title("🔍 Select Page")

    page_selection = st.sidebar.selectbox('Selected Page:', ["Time Analysis", "Country Analysis"])

    if page_selection == "Time Analysis":
        time_analysis(df)
    elif page_selection == "Country Analysis":
        country_analysis(df)

    # Download merged_df.csv
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Download DataFrame")

    merged_file_path = os.path.join("data", "merged_df.csv")

    @st.cache_data
    def load_merged_csv(path):
        with open(path, "rb") as f:
            return f.read()

    merged_csv_bytes = load_merged_csv(merged_file_path)

    st.sidebar.download_button(
        label="📥 Download DataFrame (.csv)",
        data=merged_csv_bytes,
        file_name="merged_df.csv",
        mime="text/csv"
    )

    # Download Report
    st.sidebar.subheader("📄 Download Report")

    report_path = os.path.join("Sergio Tambè - Report.docx")

    @st.cache_data
    def load_report_file(path):
        with open(path, "rb") as f:
            return f.read()

    report_bytes = load_report_file(report_path)

    st.sidebar.download_button(
        label="📥 Download Report (.docx)",
        data=report_bytes,
        file_name="Report_Tambe.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    st.sidebar.info("📘 Use the selectors to explore transaction trends across sectors, industries, and countries.")


if __name__ == "__main__":
    main()
