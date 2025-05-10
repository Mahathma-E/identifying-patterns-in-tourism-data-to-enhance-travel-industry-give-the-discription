!pip install streamlit pyngrok pandas spacy
!python -m spacy download en_core_web_sm


app_code = '''
import pandas as pd
import streamlit as st
import spacy
import en_core_web_sm

# Load NLP model
nlp = en_core_web_sm.load()

# Load dataset
df = pd.read_csv("/content/sample_data/large_tourism_data.csv")

# Streamlit App UI
st.title("Tourism Data NLP Analyzer")
st.write("Ask questions about tourist revenue, arrivals, seasons, climate, or popular destinations.")

query = st.text_input("Enter your question below:")

# Query Processing Function
def analyze_query(query):
    query = query.lower()
    doc = nlp(query)

    # Revenue & Arrivals Queries
    if ("highest" in query or "most" in query) and "revenue" in query:
        country = df.loc[df["tourism_receipts"].idxmax()]
        return f"Country with highest tourism revenue: {country['country']} (${country['tourism_receipts']:,})"

    elif "lowest" in query and "revenue" in query:
        country = df.loc[df["tourism_receipts"].idxmin()]
        return f"Country with lowest tourism revenue: {country['country']} (${country['tourism_receipts']:,})"

    elif "highest" in query or "most" in query and "arrivals" in query:
        country = df.loc[df["tourism_arrivals"].idxmax()]
        return f"Country with highest tourist arrivals: {country['country']} ({country['tourism_arrivals']:,} visitors)"

    elif "average" in query and "arrivals" in query:
        avg = int(df["tourism_arrivals"].mean())
        return f"Average tourist arrivals across all countries: {avg:,}"

    # Seasonal Queries
    elif "winter" in query and "countries" in query:
        countries = df[df["peak_season"].str.lower() == "winter"]["country"].tolist()
        return f"""Countries with Winter peak season:
{', '.join(countries)}"""

    elif "summer" in query and "countries" in query:
        countries = df[df["peak_season"].str.lower() == "summer"]["country"].tolist()
        return f"""Countries with Summer peak season:
{', '.join(countries)}"""

    elif "spring" in query and "countries" in query:
        countries = df[df["peak_season"].str.lower() == "spring"]["country"].tolist()
        return f"""Countries with Spring peak season:
{', '.join(countries)}"""

    # Climate Queries
    elif "cold" in query and "countries" in query:
        countries = df[df["climate"].str.lower() == "cold"]["country"].tolist()
        return f"""Countries with a Cold climate:
{', '.join(countries)}"""

    elif "tropical" in query and "beaches" in query:
        countries = df[df["climate"].str.lower() == "tropical"]["country"].tolist()
        return f"""Countries known for Tropical Beaches:
{', '.join(countries)}"""

    elif "cool" in query and "places" in query:
        countries = df[df["climate"].str.lower() == "cool"]["country"].tolist()
        return f"""Countries with Cool climate:
{', '.join(countries)}"""

    elif "mediterranean" in query and "coasts" in query:
        countries = df[df["climate"].str.lower() == "mediterranean"]["country"].tolist()
        return f"""Countries with Mediterranean coasts:
{', '.join(countries)}"""

    # Experience-Based Queries
    elif "sunny" in query and "beaches" in query:
        countries = df[df["description"].str.lower().str.contains("sunny")]["country"].tolist()
        return f"""Countries with Sunny Beaches:
{', '.join(countries)}"""

    elif "icy" in query and "destinations" in query:
        countries = df[df["description"].str.lower().str.contains("icy")]["country"].tolist()
        return f"""Icy Destinations perfect for snow lovers:
{', '.join(countries)}"""

    elif "balanced weather" in query and "countries" in query:
        countries = df[df["description"].str.lower().str.contains("balanced weather")]["country"].tolist()
        return f"""Countries with Balanced Weather for year-round travel:
{', '.join(countries)}"""

    # Comparison Queries
    elif "continent" in query and "revenue" in query:
        stats = df.groupby("continent")["tourism_receipts"].sum().sort_values(ascending=False)
        return f"""Total Tourism Revenue by Continent:
{stats.to_string()}"""

    elif "continent" in query and "arrivals" in query:
        stats = df.groupby("continent")["tourism_arrivals"].sum().sort_values(ascending=False)
        return f"""Total Tourist Arrivals by Continent:
{stats.to_string()}"""

    # Region-Specific Queries
    elif "europe" in query and "popular destinations" in query:
        countries = df[df["continent"] == "Europe"]["country"].tolist()
        return f"""Popular Tourism Destinations in Europe:
{', '.join(countries)}"""

    elif "asia" in query and "popular destinations" in query:
        countries = df[df["continent"] == "Asia"]["country"].tolist()
        return f"""Popular Tourism Destinations in Asia:
{', '.join(countries)}"""

    elif "north america" in query and "tourist arrivals" in query:
        total_arrivals = df[df["continent"] == "North America"]["tourism_arrivals"].sum()
        return f"""Total Tourist Arrivals in North America: {total_arrivals:,}"""

    elif "south america" in query and "tourist revenue" in query:
        total_revenue = df[df["continent"] == "South America"]["tourism_receipts"].sum()
        return f"""Total Tourism Revenue in South America: ${total_revenue:,}"""

    else:
        return "Sorry, I couldn't understand the query."

# Run analysis if query is entered
if query:
    result = analyze_query(query)
    st.markdown(result)'''

with open("app.py", "w") as f:
    f.write(app_code)




import subprocess
import time
from pyngrok import ngrok, conf

# Kill previous tunnels
ngrok.kill()

# Set your ngrok auth token
conf.get_default().auth_token = "YOUR_AUTH_TOKEN"

# Run Streamlit in background
streamlit_process = subprocess.Popen(["streamlit", "run", "app.py"])

# Wait for Streamlit to be ready
time.sleep(10)

# Connect to ngrok
public_url = ngrok.connect(8501)
print(f"Your app is live at: {public_url}")