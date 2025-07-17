import streamlit as st
import requests
from langchain.llms import Ollama
from datetime import datetime

# Configuration
HEADERS = {
    'User-Agent': 'AI-Crop-Advisor-App/1.0 (contact@example.com)'
}

# Initialize LLM (cached) - Using a smaller model for faster responses
@st.cache_resource
def load_llm():
    return Ollama(model="phi3")  # Alternatives: "gemma:2b", "tinyllama"

# Cached functions for API calls
@st.cache_data(ttl=3600)
def get_geo_data(location):
    geo_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    try:
        response = requests.get(geo_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError("Location not found")
        return data[0]  # Return first result
    except Exception as e:
        st.error(f"Error fetching location data: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_climate_data(lat, lon):
    current_year = datetime.now().year
    climate_url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={current_year-1}-01-01&end_date={current_year-1}-12-31"
        f"&daily=temperature_2m_max,precipitation_sum&timezone=auto"
    )
    try:
        response = requests.get(climate_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching climate data: {str(e)}")
        return None

# Main App
def main():
    llm = load_llm()
    
    st.set_page_config(page_title="AI Crop Advisor", layout="centered")
    st.title("🌾 AI-Powered Crop Recommendation System")
    
    with st.sidebar:
        st.markdown("### 🌍 Example Locations")
        st.markdown("- Pune, Maharashtra")
        st.markdown("- Bengaluru, Karnataka")
        st.markdown("- Ludhiana, Punjab")
        st.markdown("---")
        st.markdown("ℹ️ Uses real weather data from Open-Meteo")
        st.markdown("⚡ Using fast lightweight AI model")
    
    st.markdown("""
    Get personalized crop recommendations based on:
    - Local climate conditions
    - Soil characteristics
    - Regional farming patterns
    """)

    # Location input
    location = st.text_input(
        "📍 Enter your location (city/district/region)", 
        placeholder="e.g., Nashik, Maharashtra",
        key="location_input"
    )

    if location:
        with st.spinner("Fetching location data..."):
            geo_data = get_geo_data(location)
        
        if geo_data:
            lat = geo_data.get("lat")
            lon = geo_data.get("lon")
            display_name = geo_data.get("display_name", location)
            region = display_name.split(',')[-2].strip() if len(display_name.split(',')) > 1 else display_name
            
            with st.spinner(f"Fetching climate data for {display_name}..."):
                climate_data = get_climate_data(lat, lon)
            
            if climate_data and "daily" in climate_data:
                try:
                    # Calculate averages for the whole year
                    temp_data = climate_data["daily"]["temperature_2m_max"]
                    rain_data = climate_data["daily"]["precipitation_sum"]
                    
                    avg_temp = round(sum(temp_data) / len(temp_data), 1)
                    avg_rain = round(sum(rain_data) / len(rain_data), 1)
                    
                    # Display climate info
                    st.success(f"Climate data for {display_name}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Average Temperature", f"{avg_temp} °C")
                    with col2:
                        st.metric("Average Rainfall", f"{avg_rain} mm/year")
                    
                    # User inputs
                    st.subheader("🌱 Farming Parameters")
                    soil_type = st.selectbox(
                        "Soil Type",
                        ["Loamy", "Sandy", "Clay", "Silty", "Peaty", "Chalky"],
                        index=0
                    )
                    
                    if st.button("Get Most Common Crops", type="primary"):
                        with st.spinner("Analyzing regional farming patterns..."):
                            # Prompt focused on regional crops
                            prompt = f"""Provide a list of the most commonly grown crops in {region} based on:
- Region: {region}
- Average Temperature: {avg_temp}°C
- Average Rainfall: {avg_rain} mm/year
- Typical Soil: {soil_type}

For each crop, include:
1. Local name and scientific name
2. Typical growing season
3. Percentage of farmland dedicated to this crop in the region
4. Brief description of why it's commonly grown here
5. Any special cultural or economic significance

Format as a numbered list with bold crop names and bullet points for details."""

                            try:
                                response = llm(prompt)
                                st.subheader(f"🌱 Most Common Crops in {region}")
                                st.markdown(response)
                                
                                # Additional context about regional agriculture
                                with st.expander("ℹ️ About Regional Agriculture"):
                                    context_prompt = f"""Provide a brief overview of agriculture in {region}, including:
- Main agricultural products
- Typical farming methods
- Important festivals or traditions related to farming
- Major challenges faced by farmers
- Recent trends in agriculture"""
                                    context_response = llm(context_prompt)
                                    st.markdown(context_response)
                                
                            except Exception as e:
                                st.error(f"Error generating recommendations: {str(e)}")
                
                except KeyError:
                    st.error("Incomplete climate data received. Please try another location.")
            else:
                st.error("Climate data unavailable for this location.")
        else:
            st.error("Could not find geographic data for this location. Please try a different name.")

if __name__ == "__main__":
    main()
