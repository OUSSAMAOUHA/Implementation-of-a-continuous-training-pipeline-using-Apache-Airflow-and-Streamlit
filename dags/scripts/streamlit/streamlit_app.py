import streamlit as st
import pickle
import pandas as pd
from sklearn import preprocessing
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib.ticker import MaxNLocator
import filter
import visualization as viz

# Load the pre-trained model
with open('/opt/airflow/dags/scripts/pickle_files/modele_classification13.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

label_encoder = preprocessing.LabelEncoder()

# num_samples = 400
# nouvelles_donnees1 = pd.DataFrame({
#     'Temperature': np.random.uniform(270, 300, num_samples),
#     'Temp_Min': np.random.uniform(270, 300, num_samples),
#     'Temp_Max': np.random.uniform(270, 300, num_samples),
#     'Pressure': np.random.uniform(990, 1020, num_samples),
#     'Sea_Level': np.random.uniform(990, 1020, num_samples),
#     'Humidity': np.random.uniform(20, 100, num_samples),
#     'Wind Speed': np.random.uniform(0, 10, num_samples),
#     'Lon': np.random.uniform(-180, 180, num_samples),
#     'Lat': np.random.uniform(-90, 90, num_samples),
# })



# Main Streamlit app
def main():
    st.title("Weather Prediction App")

    # Sidebar navigation
    page = st.sidebar.selectbox("Choose a page", ["Home", "Prediction"])

    if page == "Home":
       
        data = pd.read_csv("/opt/airflow/dags/scripts/Weather_Data.csv")
       
        cities = filter.get_unique_cities_and_countries(data)
        city_selected = filter.create_city_country_dropdown(cities)

        # Call the function to get filtered records
        filtered_records = filter.filter_records_by_city(data, city_selected)

        # Display the selected city in the map
        viz.map(filtered_records)

        # Dataset features
        all_features = ['Temperature', 'Temp_Min', 'Temp_Max', 'Pressure', 'Humidity', 'Wind Speed']

        viz.create_viz(filtered_records,all_features)


    elif page == "Prediction":

        st.write("Make a weather prediction:")
        # User input for each feature
        temperature = st.slider("Temperature", min_value=0.0, max_value=400.0)
        temp_min = st.slider("Minimum Temperature", min_value=0.0, max_value=400.0)
        temp_max = st.slider("Maximum Temperature", min_value=0.0, max_value=400.0)
        pressure = st.slider("Pressure", min_value=900, max_value=1100)
        sea_level = st.slider("Sea Level", min_value=900, max_value=1100)
        humidity = st.slider("Humidity", min_value=0, max_value=100)
        wind_speed = st.slider("Wind Speed", min_value=0.0, max_value=20.0)
        lon = st.number_input("Longitude")
        lat = st.number_input("Latitude")
        # Create a DataFrame with user input
        user_data = pd.DataFrame({
            'Temperature': [temperature],
            'Temp_Min': [temp_min],
            'Temp_Max': [temp_max],
            'Pressure': [pressure],
            'Sea_Level': [sea_level],
            'Humidity': [humidity],
            'Wind Speed': [wind_speed],
            'Lon': [lon],
            'Lat': [lat]
        })
        # Load the label_encoder
        with open('/opt/airflow/dags/pickle_files/label_encoder.pkl', 'rb') as label_encoder_file:
            label_encoder1 = pickle.load(label_encoder_file)
        # Make a prediction
        if st.button("Predict"):
            # scaler = preprocessing.StandardScaler()
            # processed_data = scaler.fit_transform(nouvelles_donnees1)
            print(user_data)
            prediction = model.predict(user_data)
            print("Raw predictions:",prediction)
            st.success(f"Prediction: {prediction[0]}")

if __name__ == "__main__":
    main()
