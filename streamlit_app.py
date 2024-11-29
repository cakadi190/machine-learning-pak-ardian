import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

def clean_currency(x):
    """
    Clean currency columns by removing '$' and ',' and converting to numeric
    """
    if pd.isna(x) or x == 'Unknown':
        return 0
    if isinstance(x, str):
        return float(x.replace('$', '').replace(',', '')) if x.strip() else 0
    return x if pd.notnull(x) else 0

def preprocess_data(df):
    """
    Preprocess the startup funding dataset
    """
    # Columns for funding amounts
    funding_columns = [
        "No_Stage_Amount", "Seed_Amount", "Series_A_Amount", 
        "Series_B_Amount", "Series_C_Amount", "Series_D_Amount"
    ]
    
    # Clean and convert funding columns
    for col in funding_columns:
        df[col] = df[col].apply(clean_currency)
    
    # Fill NaN in string columns with 'Unknown'
    string_columns = [
        "Description", "Stage", "Market", "Names", 
        "No_Stage_Date", "Pitch", "Seed_Date",
        "Series_A_Date", "Series_B_Date", "Series_C_Date", "Series_D_Date"
    ]
    df[string_columns] = df[string_columns].fillna('Unknown')
    
    # Replace '-' in Stage with 'Not Passed'
    df['Stage'] = df['Stage'].replace('-', 'Not Passed')
    
    # Calculate total funding
    df['Total Funding'] = df[funding_columns].sum(axis=1)
    
    return df

def main():
    st.set_page_config(page_title="Startup Funding Analysis", layout="wide")
    
    # Title
    st.title("Startup Funding Analysis Dashboard")
    
    # Read the data from CSV file
    df = pd.read_csv('startup_data.csv', dtype=str)
    
    # Preprocess the data
    df = preprocess_data(df)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    analysis_type = st.sidebar.radio("Choose Analysis", [
        "Overview", 
        "Funding by Stage", 
        "Startup Total Funding", 
        "Market Analysis"
    ])
    
    if analysis_type == "Overview":
        # Display full dataset
        st.subheader("Full Startup Funding Dataset")
        st.dataframe(df)
    
    elif analysis_type == "Funding by Stage":
        # Funding distribution by stage
        st.subheader("Funding Distribution by Stage")
        
        # Aggregate funding by stage
        stage_funding = df.groupby('Stage')[
            ["Seed_Amount", "Series_A_Amount", "Series_B_Amount", "Series_C_Amount", "Series_D_Amount"]
        ].sum()
        
        # Create a stacked bar chart
        fig = px.bar(
            stage_funding.reset_index(), 
            x='Stage', 
            y=['Seed_Amount', 'Series_A_Amount', 'Series_B_Amount', 'Series_C_Amount', 'Series_D_Amount'],
            title="Funding Amount by Investment Stage",
            labels={'value': 'Funding Amount', 'variable': 'Funding Stage'},
            height=500
        )
        st.plotly_chart(fig)
    
    elif analysis_type == "Startup Total Funding":
        # Top startups by total funding
        st.subheader("Top Startups by Total Funding")
        
        # Group by startup name and sum total funding
        top_startups = df.groupby('Names')['Total Funding'].sum().nlargest(10)
        
        # Create bar chart of top startups
        fig = px.bar(
            x=top_startups.index, 
            y=top_startups.values, 
            title="Top 10 Startups by Total Funding",
            labels={'x': 'Startup Name', 'y': 'Total Funding'},
            height=500
        )
        st.plotly_chart(fig)
    
    elif analysis_type == "Market Analysis":
        # Market distribution of funding
        st.subheader("Funding Distribution Across Markets")
        
        # Group by market and sum total funding
        market_funding = df.groupby('Market')['Total Funding'].sum().nlargest(10)
        
        # Create pie chart of market funding
        fig = px.pie(
            values=market_funding.values, 
            names=market_funding.index, 
            title="Top 10 Markets by Total Funding",
            height=500
        )
        st.plotly_chart(fig)
    
    # Additional insights
    st.sidebar.header("Dataset Insights")
    st.sidebar.metric("Total Number of Startups", len(df))
    st.sidebar.metric("Total Funding", f"${df['Total Funding'].sum():,.0f}")
    st.sidebar.metric("Unique Markets", df['Market'].nunique())

def prepare_data_csv():
    """
    Prepare CSV from the original text file
    """
    import io
    
    # Baca file teks
    with open('paste.txt', 'r', encoding='utf-8') as file:
        data_text = file.read()
    
    # Konversi ke DataFrame
    df = pd.read_csv(io.StringIO(data_text), sep=',', dtype=str)
    
    # Simpan ke CSV
    df.to_csv('startup_data.csv', index=False)
    print("Konversi data selesai. File CSV telah dibuat.")

if __name__ == "__main__":
    # Uncomment the line below to prepare CSV first time
    # prepare_data_csv()
    main()