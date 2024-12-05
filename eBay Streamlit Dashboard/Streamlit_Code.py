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

    col1, col2 = st.columns(2, gap="large")
    with col1:
        # Price filter
        price_filter = st.slider(
            'Select Price Range', 
            min_value=float(df['Price'].min()), 
            max_value=float(df['Price'].max()), 
            value=(float(df['Price'].min()), float(df['Price'].max()))
        )
    with col2:
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
        height=500,
        column_config={
            "Price": st.column_config.NumberColumn(
                'Price (in USD)', 
                format="$ %.2f", 
                step=0.01
            ),
            "Item Number": st.column_config.TextColumn("Item Number")
        }
    )

    

def visualizations():
    st.title('Visualizations')

    # Create a bar chart for RAM size distribution
    fig = px.bar(
        x=df['Ram Size'].value_counts().index,
        y=df['Ram Size'].value_counts().values,
        title="RAM Size Distribution",
        labels={"x": "RAM Size", "y": "Count"},
    )
    # Customize the layout for better visualization
    fig.update_layout(
        xaxis_title="RAM Size",
        yaxis_title="Count",
        template="plotly_white",
        xaxis=dict(categoryorder="total descending")  # Order by count
    )
    st.plotly_chart(fig)

    st.divider()

    # Create a histogram for Price distribution
    fig = px.histogram(
        df,
        x="Price",
        nbins=6,  # Number of bins for better granularity
        title="Price Distribution of Laptops",
        labels={"Price": "Price (in USD)"}
    )
    # Customize the layout for better visualization
    fig.update_layout(
        xaxis_title="Price (in USD)",
        yaxis_title="Count",
        template="plotly_white"
    )
    st.plotly_chart(fig)
    st.caption("Price distribution of laptops in the dataset")

    st.divider()

    new_condition_df = df[df['Condition'].str.lower() == 'new']
    # Define the desired order of "Ram Size"
    #ram_order = ['4 MB','2 GB',"4 GB", '6 GB', "8 GB", '12 GB', "16 GB", '20 GB', '24 GB', "32 GB", '64 GB', '128 GB', '512 GB']
    ram_order = ["4 GB", '6 GB', "8 GB", '12 GB', "16 GB", '20 GB', "32 GB", '64 GB']
    # Convert the "Ram Size" column to a categorical type with the specified order
    new_condition_df["Ram Size"] = pd.Categorical(new_condition_df["Ram Size"], categories=ram_order, ordered=True)
    # Calculate the average price for each RAM size
    avg_price_per_ram = new_condition_df.groupby("Ram Size")["Price"].mean().reset_index()
    # Create a line chart to show the average price at each RAM size
    fig = px.line(
        avg_price_per_ram,
        x="Ram Size",
        y="Price",
        title="Average New Laptop Price by RAM Size",
        labels={"Ram Size": "RAM Size", "Price": "Average Price (in USD)"},
    )
    # Customize the layout for better visualization
    fig.update_layout(
        xaxis_title="RAM Size",
        yaxis_title="Average Price (in USD)",
        template="plotly_white"
    )
    st.plotly_chart(fig)



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