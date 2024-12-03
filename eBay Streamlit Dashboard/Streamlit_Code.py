import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(layout='wide',initial_sidebar_state="collapsed")

# Add a logo in the top left corner
logo_url = "https://upload.wikimedia.org/wikipedia/commons/4/48/EBay_logo.png"
st.logo(logo_url, size="large")

# Custom HTML for logo and title
html_header = f"""
    <div style="display: flex; align-items: center; justify-content: center;">
        <img src="{logo_url}" alt="Logo" style="width: 100px; margin-right: 20px;">
        <h1 style="flex-grow: 1; text-align: center;">Data Dashboard</h1>
    </div>
"""
st.markdown(html_header, unsafe_allow_html=True)

df = pd.read_csv('Cleaned_Ebay_Data.csv')


def data():
    st.title('Explore the Data')

    all_brands = df['Brand'].unique()
    brands = st.multiselect(
        'Select Brands', 
        options=["*All Brands*"] + list(all_brands),  # Add "All" to the options
        default=["*All Brands*"]  # Default to "All"
    )
    # Filter the DataFrame based on selection
    if "*All Brands*" in brands:
        filtered_brands = df  # Show all brands
    else:
        filtered_brands = df[df["Brand"].isin(brands)]

    st.dataframe(filtered_brands, use_container_width=True, 
        column_config={"Price":st.column_config.NumberColumn('Price (in USD)', format="$ %.2f", step=0.01),
                        "Item Number":st.column_config.TextColumn("Item Number")})         

    

def visualizations():
    st.title('Visualizations')





def streamlit_menu():
    selected = option_menu(
            menu_title=None,  # required
            options=["Explore Data", "Visualizations"],  # required
            icons=["database", "bar-chart"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#727372"},
                "icon": {"color": "orange", "font-size": "30px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#6fa3f7",
                },
                "nav-link-selected": {"background-color": "#045fba"},
            },
        )
    return selected

selected = streamlit_menu()

if selected == "Explore Data":
    data()
if selected == "Visualizations":
    visualizations()