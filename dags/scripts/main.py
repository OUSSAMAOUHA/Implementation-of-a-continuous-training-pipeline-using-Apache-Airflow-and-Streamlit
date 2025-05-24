import os

import requests
import pandas as pd
from datetime import datetime
#7c0f631168d840e542618054bb96059e
api_key = '2a258b2fa442fb8d6f8be3014c88c57a'
endpoint = 'https://api.openweathermap.org/data/2.5/forecast'

existing_data = pd.read_csv('/opt/airflow/dags/scripts/dataset/Weather_Data.csv')
existing_data['Date'] = pd.to_datetime(existing_data['Date'], errors='coerce')

cities = [
        "Tokyo", "Mexico", "Séoul", "Jakarta", "New Delhi", "Le Caire", "Moscou", "Buenos Aires",
        "Manille", "Londres", "Dhâkâ", "Paris", "Pékin", "Bangkok", "Lima", "Bogotá", "Téhéran",
        "Kinshasa", "Santiago", "Madrid", "Naypyidaw", "Damas", "Singapour", "Ankara", "Luanda",
        "Bagdad", "Riyad", "Caracas", "Athènes", "Berlin", "Accra", "Hanoï", "Kiev", "Rome",
        "Addis-Abeba", "Guatemala", "Pyongyang", "Tachkent", "Saint-Domingue", "Brasilia",
        "Nairobi", "San José", "Tunis", "Alger", "Bucarest", "Budapest", "Conakry", "La Havane",
        "Port-au-Prince", "Dakar", "Amman", "Lisbonne", "Stockholm", "Kaboul", "Bakou",
        "San Salvador", "Minsk", "Varsovie", "Vienne", "Astana", "Harare", "Katmandou",
        "Khartoum", "Montevideo", "Quito", "Rabat", "Tananarive", "Colombo", "Kuala Lumpur",
        "Erevan", "Tripoli", "Bruxelles", "Phnom Penh", "Sofia", "Belgrade", "Mogadiscio",
        "Prague", "Tegucigalpa", "Yaoundé", "Maputo", "Tbilissi", "Pretoria", "Kampala",
        "Ottawa", "Abou Dabi", "Bamako", "Beyrouth", "Lusaka", "Managua", "Ndjamena",
        "Ouagadougou", "Sanaa", "Mascate", "Lomé", "Panamá", "Brazzaville", "Islamabad",
        "Kigali", "Zagreb", "Jerusalem", "Monrovia", "Rīga", "Amsterdam", "Niamey", "Tirana",
        "Oulan-Bator", "Bangui", "Libreville", "Chişinău", "Vientiane", "Kingston", "Bichkek",
        "Achgabat", "Skopje", "Washington", "Helsinki", "Nouakchott", "Vilnius", "Freetown",
        "Asunción", "Oslo", "Douchanbé", "Copenhague", "Dublin", "Asmara", "Bratislava",
        "Koweït", "Lilongwe", "Tallinn", "Sarajevo", "Djibouti", "Doha", "Wellington",
        "Canberra", "Port Moresby", "Bujumbura", "Port-d'Espagne", "Porto-Novo",
        "Sucre (Bolivie)", "Bissau", "Ljubljana", "Georgetown", "Paramaribo", "Windhoek",
        "Nassau", "Nicosie", "Dodoma", "Gaborone", "Maseru", "Suva", "Manama", "Port-Louis",
        "Podgorica", "Berne", "Reykjavík", "Yamoussoukro", "Praia", "Abuja",
        "Bandar Seri Begawan", "Luxembourg", "Malé", "Castries", "Dili", "Mbabane",
        "Thimphou", "Malabo", "São Tomé", "Banjul", "Apia", "Nuku'alofa", "Saint-Georges",
        "Monaco", "Honiara", "Moroni", "Port-Vila", "Saint John's", "Tarawa", "Victoria",
        "Delap-Uliga-Darrit", "Andorre-la-Vieille", "Kingstown", "Roseau", "Basseterre",
        "Palikir", "Belmopan", "La Valette", "Bridgetown", "Vaduz", "Funafuti", "Saint-Marin",
        "Cité du Vatican", "Melekeok"
    ]

new_data_list = []

for city in cities:
    url = f'{endpoint}?q={city}&APPID={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
            weather_data = response.json()

            if 'list' in weather_data:
                city_forecast = weather_data['list']

                for forecast in city_forecast:
                    timestamp = forecast['dt']
                    date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

                    forecast_date = pd.to_datetime(date)

                    if forecast_date > existing_data['Date'].max():
                        city_info = {
                            'City': city,
                            'Date': date,
                            'Temperature': forecast['main']['temp'],
                            'Temp_Min': forecast['main']['temp_min'],
                            'Temp_Max': forecast['main']['temp_max'],
                            'Pressure': forecast['main']['pressure'],
                            'Sea_Level': forecast['main']['sea_level'] if 'sea_level' in forecast['main'] else None,
                            'Humidity': forecast['main']['humidity'],
                            'Description': forecast['weather'][0]['main'],
                            'Wind Speed': forecast['wind']['speed'],
                            'Country': weather_data['city']['country'],
                            'Lon': weather_data['city']['coord']['lon'],
                            'Lat': weather_data['city']['coord']['lat'],
                        }
                        new_data_list.append(city_info)
            else:
                print(f"No forecast data for {city}")
    else:
        print(f"Error {city}: {response.status_code}")

    new_data_df = pd.DataFrame(new_data_list)

    if not new_data_df.empty:
        new_data_df.to_csv(os.path.abspath('/opt/airflow/dags/scripts/dataset/Weather_Data.csv'), index=False, mode='a', header=False)
    else:
        print("No new data to add.")