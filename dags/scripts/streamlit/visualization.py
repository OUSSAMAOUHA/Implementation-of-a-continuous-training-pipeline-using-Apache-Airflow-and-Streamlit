import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib.ticker import MaxNLocator

def create_viz_type_dropdown():
    viz_types = ['Line Chart', 'Bar Chart', 'Scatter Plot', 'Histogram', 'Box Plot']
    
    # Create the dropdown widget
    selected_viz_type = st.selectbox("Select Visualization Type:", options=viz_types)

    return selected_viz_type


def create_feature_dropdowns(viz_type, all_features):
    if viz_type in ['Scatter Plot', 'Box Plot']:
        # Create the first feature dropdown
        feature1 = st.selectbox("Select the first feature:", options=all_features)

        # Create the second feature dropdown
        feature2 = st.selectbox("Select the second feature:", options=all_features)

        return feature1, feature2
    
    elif viz_type in ['Bar Chart', 'Line Chart','Histogram']:
        # Create the feature dropdown
        feature = st.selectbox("Select the feature:", options=all_features)

        return feature
    else:
        return None

def scatter_box_plot(x_feature, y_feature, data, type, num_ticks=8):
    if type == 'Scatter Plot':
        # Scatter Plot
        st.subheader(f'Scatter Plot for {x_feature} vs. {y_feature}')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x=x_feature, y=y_feature, data=data, ax=ax)
        st.pyplot(fig)
    elif type == 'Box Plot':
        # Box Plot
        st.subheader('Box Plot')
        fig_box, ax_box = plt.subplots(figsize=(10, 6))
        sns.boxplot(x=x_feature, y=y_feature, data=data, ax=ax_box)
        set_selected_ticks(ax_box, num_ticks)
        st.pyplot(fig_box)


def histogram_line_bar_plot(feature, data,type):
    if type == 'Line Chart':
        # Line Chart
        st.subheader(f'Time Series Plot for {feature}')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.lineplot(x='Date', y=feature, data=data, ax=ax)
        
        # Set a maximum number of x-axis ticks
        max_ticks = 8
        ax.xaxis.set_major_locator(MaxNLocator(max_ticks))
        
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif type == 'Bar Chart':
        st.subheader(f'Bar Chart for {feature}')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x=feature, data=data, ax=ax)
        # Set a maximum number of x-axis ticks
        max_ticks = 16
        ax.xaxis.set_major_locator(MaxNLocator(max_ticks))
        plt.xticks(rotation=45)
        st.pyplot(fig)
    elif type == 'Histogram':
        st.subheader(f'Histogram for {feature}')
        fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
        sns.histplot(data[feature], bins=20, kde=True, ax=ax_hist)
        st.pyplot(fig_hist)


def set_selected_ticks(axis, num_ticks):
    # Distribute ticks evenly across the x-axis
    x_ticks = [i * (len(axis.get_xticks()) - 1) // (num_ticks - 1) for i in range(num_ticks)]
    axis.set_xticks(x_ticks)    



def map(data):
    fig_map = px.scatter_mapbox(data, lat="Lat", lon="Lon", hover_name="City",
                                color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig_map)

def create_viz(data, features):
    
        viz_type = create_viz_type_dropdown()  # Assuming you have a function to get the visualization type

        selected_features = create_feature_dropdowns(viz_type, features)

        if viz_type in ['Scatter Plot', 'Box Plot']:

            scatter_box_plot(selected_features[0], selected_features[1], data,viz_type)

        elif viz_type in ['Bar Chart', 'Line Chart','Histogram']:
          
            histogram_line_bar_plot(selected_features, data,viz_type)

        else:

            st.write(f"Selected visualization type: {viz_type}")