import streamlit as st



def get_unique_cities_and_countries(dataframe):
        # Ensure that the dataframe contains the required columns
        required_columns = ['City', 'Country']
        if not all(col in dataframe.columns for col in required_columns):
            raise ValueError("The dataframe must contain 'City' and 'Country' columns.")

        # Extract unique city-country pairs
        unique_city_country_pairs = dataframe[['City', 'Country']].drop_duplicates()

        # Convert the pairs to a dictionary
        city_country_dict = dict(zip(unique_city_country_pairs['City'], unique_city_country_pairs['Country']))

        return city_country_dict


def create_city_country_dropdown(city_country_dict):
    # Convert the dictionary to a list of tuples for the dropdown
    options = [(f"{city} - {country}", city) for city, country in city_country_dict.items()]

    # Create the search box
    search_text = st.text_input("Search:", "")

    # Filter options based on search
    filtered_options = [(label, value) for label, value in options if search_text.lower() in label.lower()]

    # Create the dropdown widget
    selected_city = st.selectbox("Select a City:", options=filtered_options, format_func=lambda x: x[0] if x else None)

    return selected_city[1] if selected_city else None
    

def filter_records_by_city(dataframe, city):
    # Ensure the 'City' column is in string format
    dataframe['City'] = dataframe['City'].astype(str)

    # Filter records based on the provided city
    filtered_records = dataframe[dataframe['City'].str.lower() == city.lower()]

    return filtered_records
