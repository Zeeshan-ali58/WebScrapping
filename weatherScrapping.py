import requests
from bs4 import BeautifulSoup
import streamlit as st

def scrape_weather_data():
    url = "https://nwfc.pmd.gov.pk/new/daily-forecast-en.php" #National Weather Forecasting Center
    # setting headers for targeted url. Sometimes the browser does not support scrapping or its blocked on the site so headers help to get the data
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    st.write(f"Status Code: {response.status_code}") 
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        #Punjab's data is in 3rd tab and the id of that tab is tab3 so we are targeting that
        tab3 = soup.find('div', {'id': 'tab3'})
        
        if tab3:
            # Extract forecast date (assuming the date is inside 'h5' or 'span' tag)
            forecast_date = tab3.find('h5') or tab3.find('span')
            if forecast_date:
                forecast_date = forecast_date.text.strip()
            else:
                forecast_date = "Date not found"
        else:
            forecast_date = "tab3 not found"
        
        # Find the table with the class 'table-bordered' for weather data
        table = tab3.find('table', {'class': 'table-bordered'})
        
        if table:
            weather_data = []
            rows = table.find_all('tr')[1:]  # Skip the header row

            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 6:  # Ensure that the row has the expected columns because columns are 6 in the targeted url
                    city = columns[0].text.strip()
                    max_temp = columns[1].text.strip()
                    min_temp = columns[2].text.strip()
                    weather = columns[3].text.strip()
                    wind = columns[4].text.strip()
                    humidity = columns[5].text.strip()

                    weather_data.append({
                        "City": city,
                        "Max Temp": max_temp,
                        "Min Temp": min_temp,
                        "Weather": weather,
                        "Wind": wind,
                        "Humidity": humidity
                    })
            return forecast_date, weather_data
    else:
        st.write(f"Failed to retrieve the page, status code: {response.status_code}")
        return None, []

# Streamlit app interface
st.title("Punjab Weather Forecast Prepared by Zeeshan Ali Ludhianvi")
st.write("Select a city to view the weather forecast.")

# Scrape and display the weather data and forecast date
forecast_date, weather_data = scrape_weather_data()
if forecast_date:
    st.write(f"### Forecast Date: {forecast_date}")
else:
    st.write("### Forecast Date: Not available")

# Check if data is available
if weather_data:
    # Get unique city names for filtering
    cities = sorted(set(item["City"] for item in weather_data))
    
    # Filter for city selection of punjab
    selected_city = st.selectbox("Choose a City", ["All"] + cities)
    
    # Apply city filter if one is selected
    if selected_city != "All":
        weather_data = [item for item in weather_data if item["City"] == selected_city]
    
    # Display filtered data in a table format
    st.write("### Weather Data")
    st.table(weather_data)
else:
    st.warning("Failed to retrieve weather data.")

st.write("Data collected by Zeeshan Ali")