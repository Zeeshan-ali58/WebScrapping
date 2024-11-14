import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def scrap_news_date():
    url = "https://tribune.com.pk/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    st.write(f"Status Code for request is: {response.status_code}")
    newsData = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate the main news section
        news_section = soup.find('div', class_='horizontal-news1')
        if news_section:
            # Find all list items within this section
            for article in news_section.find_all('li'):
                caption = article.find('div', class_='horiz-news1-caption')
                
                if caption:
                    title_tag = caption.find('h3')
                    date_tag = caption.find('span')
                    
                    # Extract and clean title and date
                    title = title_tag.text.strip() if title_tag else "No title available"
                    last_updated_date = date_tag.text.strip() if date_tag else "No date available"

                    newsData.append({
                        "Title": title,
                        "Last Updated Date": last_updated_date
                    })
    else:
        st.write(f"Failed to retrieve the page, status code: {response.status_code}")

    return newsData

# Streamlit app interface
st.title("News Scraping from Tribune - Prepared by Zeeshan Ali Ludhianvi")

# Scrape and display the news data
news_data = scrap_news_date()

# Convert news data to DataFrame for tabular display
if news_data:
    news_df = pd.DataFrame(news_data)
    st.write("### Latest News Articles")
    st.table(news_df)  # Display data in a table format
else:
    st.write("No news data available.")

st.markdown(
    """
    <div style="text-align: right; font-size: 12px; color: grey; font-style:italic">
        Data collected by Zeeshan Ali
    </div>
    """,
    unsafe_allow_html=True
)
