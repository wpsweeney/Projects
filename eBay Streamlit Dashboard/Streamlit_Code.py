import pandas as pd
import streamlit as st
import plotly.express as px
import subprocess
from streamlit_option_menu import option_menu
import numpy as np

st.set_page_config(layout='wide',
                    initial_sidebar_state="collapsed",
                    page_title="eBay Dashboard",
                    page_icon=":bar_chart:")

# Add a logo in the top left corner
ebay_url = "https://upload.wikimedia.org/wikipedia/commons/4/48/EBay_logo.png"
wfu_url = "https://seeklogo.com/images/W/wake-forest-university-athletic-logo-3CDC546B33-seeklogo.com.png"
st.logo(wfu_url, size="large")

# Custom HTML for logo and title
html_header = f"""
    <div style="display: flex; align-items: center; justify-content: center;">
        <img src="{ebay_url}" alt="Logo" style="width: 100px; margin-right: 20px;">
        <h1 style="flex-grow: 1; text-align: center;">Data Dashboard</h1>
    </div>
"""
st.markdown(html_header, unsafe_allow_html=True)

df = pd.read_csv('Cleaned_Ebay_Data.csv')


def data():
    st.title('Explore the Data')

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
            options=['ALL', 'Under 14"', '14" - 16"', 'Over 16"'],
            default='ALL'
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
    col1, col2 = st.columns(2)
    # Create a bar chart for RAM size distribution
    with col1:
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
        st.text("Most laptops for sale on eBay use the four main RAM sizes: 4GB, 8GB, 16GB, and 32GB. These RAM sizes make up the majority of the consumer market laptops. Many laptops also offer multiple RAM sizes to choose from.")

    #st.divider()

    # Create a histogram for Price distribution
    with col2:
        fig = px.histogram(
            df,
            x="Price",
            nbins=6,  # Number of bins for better granularity
            title="Price Distribution",
            labels={"Price": "Price (in USD)"}
        )
        # Customize the layout for better visualization
        fig.update_layout(
            xaxis_title="Price (in USD)",
            yaxis_title="Count",
            template="plotly_white"
        )
        st.plotly_chart(fig)
        st.text("The price distribution shows that most laptops are priced below $500, followed by laptops in the $500-1000 range. The high-end laptops are few and far between. This makes sense considering that eBay is a marketplace for primarily used and refurbished items at lower price points.")

    st.divider()

    new_condition_df = df[df['Condition'].str.lower() == 'new']
    # screen size filter
    screen_filter = st.slider(
        'Select Screen Size Range', 
        min_value=float(df['Screen Size'].min()), 
        max_value=float(df['Screen Size'].max()), 
        value=(float(df['Screen Size'].min()), float(df['Screen Size'].max()))
    )
    # Apply screen filter
    new_condition_df = new_condition_df[
        (new_condition_df['Screen Size'] >= screen_filter[0]) & 
        (new_condition_df['Screen Size'] <= screen_filter[1])
    ]

    # Define the desired order of "Ram Size"
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
    st.text("The average price of new laptops increases with the RAM size. The price difference between RAM sizes is more pronounced for higher RAM sizes, such as 32GB and 64GB. This trend is expected as higher RAM sizes are associated with more powerful laptops that are typically more expensive.")

    st.divider()

    # Filter data for valid 4-digit years
    df["Release Year"] = pd.to_numeric(df["Release Year"], errors="coerce")
    valid_data = df[(df["Release Year"] >= 2010) & (df["Release Year"] <= 9999)]

    # Subset the data to calculate average price by release year
    avg_price_by_year = (
        valid_data.groupby("Release Year")["Price"]
        .mean()
        .reset_index()
        .sort_values("Release Year")
    )
    avg_price_by_year["Release Year"] = avg_price_by_year["Release Year"].astype(int)
    avg_price_by_year["Release Year"] = avg_price_by_year["Release Year"].astype(str)
    
    st.markdown("##### Average Laptop Price by Release Year")
    st.line_chart(avg_price_by_year.set_index("Release Year"), x_label="Release Year", y_label="Average Price (in USD)")
    st.text("The average price of laptops is highest for the most recent years, indicating that older technology has become outdated and less expensive. The decreasing trend in average price over the years is consistent with the rapid advancements in technology and the decreasing cost of older models.")



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