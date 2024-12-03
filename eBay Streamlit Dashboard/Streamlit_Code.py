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

    # brand_filter = st.multiselect('Select Brand', options=['ALL'] + df['Brand'].unique().tolist(), default='ALL')
    # price_filter = st.slider('Select Price Range', min(df['Price']), max(df['Price']), (min(df['Price']), max(df['Price'])))
    # screen_size_filter = st.segmented_control('Select Screen Size', options=['ALL', 'Under 14"', '14" - 16"', 'Over 16"'], default='ALL')


    # filtered_df = df.copy()
    # if brand_filter != 'ALL':
    #     filtered_df = filtered_df[filtered_df['Brand'].isin(brand_filter)]

    # filtered_df = filtered_df[(filtered_df['Price'] >= price_filter[0]) & (filtered_df['Price'] <= price_filter[1])]
    
    # if screen_size_filter == 'Under 14"':
    #     filtered_df = filtered_df[filtered_df['Screen Size'] < 14]
    # elif screen_size_filter == '14" - 16"':
    #     filtered_df = filtered_df[(filtered_df['Screen Size'] >= 14) & (filtered_df['Screen Size'] <= 16)]
    # elif screen_size_filter == 'Over 16"':
    #     filtered_df = filtered_df[filtered_df['Screen Size'] > 16]


    # st.dataframe(filtered_df, use_container_width=True, 
    #     column_config={"Price":st.column_config.NumberColumn('Price (in USD)', format="$ %.2f", step=0.01),
    #                     "Item Number":st.column_config.TextColumn("Item Number")})   
    # 

    # Brand filter
    brand_filter = st.multiselect(
        'Select Brand', 
        options=['ALL'] + df['Brand'].unique().tolist(), 
        default=['ALL']
    )

    # Price filter
    price_filter = st.slider(
        'Select Price Range', 
        min_value=float(df['Price'].min()), 
        max_value=float(df['Price'].max()), 
        value=(float(df['Price'].min()), float(df['Price'].max()))
    )

    # Screen size filter
    screen_size_filter = st.segmented_control(
        'Select Screen Size', 
        options=['ALL', 'Under 14"', '14" - 16"', 'Over 16"']
    )

    # Create a copy of the DataFrame for filtering
    filtered_df = df.copy()

    # Apply brand filter
    if 'ALL' not in brand_filter:
        filtered_df = filtered_df[filtered_df['Brand'].isin(brand_filter)]

    # Apply price filter
    filtered_df = filtered_df[
        (filtered_df['Price'] >= price_filter[0]) & 
        (filtered_df['Price'] <= price_filter[1])
    ]

    # Apply screen size filter
    if screen_size_filter == 'Under 14"':
        filtered_df = filtered_df[filtered_df['Screen Size'] < 14]
    elif screen_size_filter == '14" - 16"':
        filtered_df = filtered_df[
            (filtered_df['Screen Size'] >= 14) & 
            (filtered_df['Screen Size'] <= 16)
        ]
    elif screen_size_filter == 'Over 16"':
        filtered_df = filtered_df[filtered_df['Screen Size'] > 16]

    # Display the filtered DataFrame in Streamlit
    st.dataframe(
        filtered_df, 
        use_container_width=True, 
        column_config={
            "Price": st.column_config.NumberColumn(
                'Price (in USD)', 
                format="$ %.2f", 
                step=0.01
            ),
            "Item Number": st.column_config.TextColumn("Item Number")
        }
    )


# Filter by Brand
#     all_brands = df['Brand'].unique()
#     brands = st.multiselect(
#         'Select Brands', 
#         options=["All"] + list(all_brands),  # Add "All" to the options
#         default=["All"]  # Default to "All"
#     )
#     # Filter the DataFrame based on selection
#     if "All" in brands:
#         filtered_brands = df  # Show all brands
#     else:
#         filtered_brands = df[df["Brand"].isin(brands)]

# # Filter by Screen Size
#     sub13 = df['Screen Size'] < 13
#     tween = (df['Screen Size'] >= 13) & (df['Screen Size'] < 16)
#     over16 = df['Screen Size'] > 16
#     screens = st.segmented_control(
#         'Select Screen Size',
#         options=['All', 'Under 14"', '14" - 16"', 'Over 16"'],
#         default='All')
#     if screens == 'All':
#         filtered_sizes = df
#     elif screens == 'Under 14"':
#         filtered_sizes = df[sub13]
#     elif screens == '14" - 16"':
#         filtered_sizes = df[tween]
#     elif screens == 'Over 16"':
#         filtered_sizes = df[over16]


         

    

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