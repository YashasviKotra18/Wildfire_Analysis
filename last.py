import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import base64

# Helper function for creating a downloadable link for images
def get_image_download_link(figure, filename):
    encoded_fig = base64.b64encode(figure.to_image(format="png")).decode()
    href = f'<a href="data:image/png;base64,{encoded_fig}" download="{filename}.png">Download Image</a>'
    return href

# Load the dataset
df = pd.read_csv("wildlife_fire_project.csv")

# Sidebar with radio buttons and year slider
selected_chart = st.sidebar.radio("Select Visualization", ["All", "Chart 1", "Chart 2", "Chart 3", "Chart 4", "Chart 5", "Linear Regression"])
selected_year = st.sidebar.slider("Select Year", min_value=df['discovery_year'].min(), max_value=df['discovery_year'].max(), value=df['discovery_year'].min())

# Main content
st.title("Wildlife Fire Project Dashboard")

# Filter data based on selection
df_filtered = df[df['discovery_year'] == selected_year]

# Visualization 1: Bar Chart
if selected_chart == "Chart 1" or selected_chart == "All":
    st.subheader("Bar Chart")
    fig1 = px.bar(df_filtered, x="state", y="fire_size", title=f"Fire Size by State in {selected_year}")
    st.plotly_chart(fig1)

    # Download link
    st.markdown(get_image_download_link(fig1, "bar_chart"), unsafe_allow_html=True)


# Visualization 2: Scatter Plot
if selected_chart == "Chart 2" or selected_chart == "All":
    st.subheader("Scatter Plot")
    fig2 = px.scatter(df_filtered, x="longitude", y="latitude", color="fire_size_class", size="fire_size", title=f"Scatter Plot in {selected_year}")
    st.plotly_chart(fig2)

    # Download link
    st.markdown(get_image_download_link(fig2, "scatter_plot"), unsafe_allow_html=True)

 

# Visualization 3: Violin Plot
if selected_chart == "Chart 3" or selected_chart == "All":
    st.subheader("Violin Plot")
    fig3 = px.violin(df_filtered, y="fire_size", box=True, points="all", title=f"Violin Plot of Fire Size in {selected_year}")
    st.plotly_chart(fig3)

    # Download link
    st.markdown(get_image_download_link(fig3, "violin_plot"), unsafe_allow_html=True)


# Visualization 4: Heatmap
if selected_chart == "Chart 4" or selected_chart == "All":
    st.subheader("Heatmap")
    heatmap_fig = px.density_heatmap(df_filtered, x="discovery_month", y="discovery_year",
                                     marginal_x="histogram", marginal_y="histogram",
                                     title=f"Heatmap of Fire Discoveries Over Months and Years in {selected_year}")
    st.plotly_chart(heatmap_fig)

    # Download link
    st.markdown(get_image_download_link(heatmap_fig, "heatmap"), unsafe_allow_html=True)


# Visualization 5: Pie Chart
if selected_chart == "Chart 5" or selected_chart == "All":
    st.subheader("Pie Chart")
    pie_fig = px.pie(df_filtered, names="state", title=f"Distribution of Fires by State in {selected_year}")
    st.plotly_chart(pie_fig)

    # Download link
    st.markdown(get_image_download_link(pie_fig, "pie_chart"), unsafe_allow_html=True)

# Visualization 6: Linear Regression (Scatter Plot with Fitted Line - Red Color)
if selected_chart == "Linear Regression" or selected_chart == "All":
    st.subheader("Linear Regression")
    X = df_filtered[['Temp_cont', 'Wind_cont', 'Hum_cont']]
    y = df_filtered['fire_size']

    model = LinearRegression()
    model.fit(X, y)

    scatter_fig = px.scatter(df_filtered, x='Temp_cont', y='fire_size', title=f'Linear Regression in {selected_year}', trendline='ols')
    scatter_fig.update_traces(line=dict(color='red'))  # Set trendline color to red
    scatter_fig.update_layout(xaxis_title='Temperature (Cont.)', yaxis_title='Fire Size')
    st.plotly_chart(scatter_fig)

    # Download link
    st.markdown(get_image_download_link(scatter_fig, "linear_regression"), unsafe_allow_html=True)

# Data Summary/Insights
st.subheader("Data Summary/Insights")
st.write(df_filtered.describe())
