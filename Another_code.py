import streamlit as st
from datetime import date,datetime
import webbrowser
import pandas as pd
import requests
from bs4 import BeautifulSoup
import wikipediaapi


wiki = wikipediaapi.Wikipedia(
    user_agent="MyWikipediaApp/1.0 (contact@example.com)",
    language="en"
)


API_KEY="310ad18b56d29bdc3d75f18493bcc69b"
url="https://api.openweathermap.org/data/2.5/weather"




st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;">
        🌈 — Feel Free To Ask Anything 
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='color: blue;'>WELCOME TO CHATBOT 💬</h1>",
    unsafe_allow_html=True
)

st.markdown("### Hello Friends :smile:")

# Initialize page in session state
if "page" not in st.session_state:
    st.session_state.page = "Ask_anything"

# Page buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Ask anything", key="Ask anything"):
        st.session_state.page = 'Ask_anything'
with col2:
    if st.button("Today weather report", key="today_weather_report"):
        st.session_state.page = 'weather_report'
with col3:
    if st.button("Sports info", key="sports_info"):
        st.session_state.page = 'sports_info'
with col4:    
    if st.button("What's going around world", key="whats_going_around_world"):
        st.session_state.page = 'whats_going_around_world'


# Page functions
def page_Ask_anything():
    
    st.subheader("Ask anything")
    
    with st.form("Taking input"):
        ask1 = st.text_input("What's in your mood")
        submitted = st.form_submit_button("Ask")  

        if submitted:
            page = wiki.page(ask1)
            if page.exists():
                st.write(f"\n🔹 Title: {page.title}")
                st.write(f"\n🔹 Summary:\n{page.summary[:500]}...")  # Print first 500 characters
                st.write(f"\n🔹 Full article: {page.fullurl}")
            else:
                st.write("\n❌ Sorry, the page was not found on Wikipedia.")

           

def page_weather_report():
    st.subheader("Weather report")
    a=datetime.today()
    st.text(f" The report is generated at Time {a}")

    


    with st.form("weather form"):
        whet=st.text_input("Enter Location Name ")
        submitted= st.form_submit_button("get weather report")

        if submitted:
            params = {
    "q": whet,          
    "appid": API_KEY,   
    "units": "metric"   
}

            # Make the GET request
            response = requests.get(url, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                city = data["name"]
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"].capitalize()
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]



                st.success(f"✅ Weather report for **{city}**:")
                st.write(f"🌡️ **Temperature:** {temp} °C")
                st.write(f"☁️ **Condition:** {desc}")
                st.write(f"💧 **Humidity:** {humidity}%")
                st.write(f"💨 **Wind speed:** {wind_speed} m/s")
                
            else:
                st.error(f"❌ Error {response.status_code}: Could not fetch weather data.")
                st.text(response.text)
                

    
    
def page_sports_info():
    st.subheader("Cric news")
    
    sports = st.selectbox("Choose sports", ["select sports",
        "Football info",
        "Cricket info",
        "Olympics info",
        "Hockey info"
    ])
    if sports=="select sports":
        st.write("choose options")
    if sports == "Football info":
        st.write("Football info will appear here")
        webbrowser.open("https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026")
    elif sports == "Cricket info":
        cricket_type = st.selectbox("Choose cricket type", ["Select option",
            "Test",
            "ODI",
            "T20",
            "IPL"
        ])
        if cricket_type=="Select option":
            st.text("")
        elif cricket_type=="Test":
            st.write(f"You selected: {cricket_type}")
            webbrowser.open("https://www.cricbuzz.com/cricket-stats/points-table/test/icc-world-test-championship")

        elif cricket_type=="ODI":
             st.write(f"You selected: {cricket_type}")
             webbrowser.open("https://www.cricbuzz.com/live-cricket-scores/121681/indw-vs-rsaw-final-icc-womens-world-cup-2025")
            
        elif cricket_type=="T20":
             st.write(f"You selected: {cricket_type}")
             webbrowser.open("https://www.cricbuzz.com/live-cricket-scores/116957/aus-vs-ind-4th-t20i-india-tour-of-australia-2025")
            
        elif cricket_type=="IPL":
             st.write(f"You selected: {cricket_type}")
             webbrowser.open("https://www.cricbuzz.com/cricket-series/9241/indian-premier-league-2026/matches")
        
    elif sports == "Olympics info":
        st.write("Olympics info will appear here")
        webbrowser.open("https://www.olympics.com/en/olympic-games/paris-2024")
    elif sports == "Hockey info":
        st.write("Hockey info will appear here")
        webbrowser.open("https://www.hockeyindia.org/")



def page_whats_going_around_world():
    st.subheader("News across the world")
    url = "https://timesofindia.indiatimes.com/"
    headers = {"User-Agent": "Mozilla/5.0"}  # To avoid being blocked
    response = requests.get(url, headers=headers)

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    links = []

    # Extract links that lead to articles (pattern: /articleshow/)
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]
        if text and "/articleshow/" in href:
            # Convert relative URLs to absolute
            if href.startswith("/"):
                href = "https://timesofindia.indiatimes.com" + href
            headlines.append(text)
            links.append(href)

    # Store in DataFrame
    if headlines:
        df = pd.DataFrame({
            "Headline": headlines[:20],  # Top 20 headlines
            "Link": links[:20]
        })
        # Display clickable links
        st.markdown("### 🗞️ Top Headlines")
        for i, row in df.iterrows():
            st.markdown(f"**{i+1}. [{row['Headline']}]({row['Link']})**")
    else:
        st.warning("⚠️ No headlines found — the website layout might have changed.")




# Navigation logic
if st.session_state.page == "Ask_anything":
    page_Ask_anything()
elif st.session_state.page == "weather_report":
    page_weather_report()
elif st.session_state.page == "sports_info":
    page_sports_info()
elif st.session_state.page == "whats_going_around_world":
    page_whats_going_around_world()




