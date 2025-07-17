# AI-Powered-Crop-Recommendation-System


A smart, lightweight web application that recommends region-specific crops based on historical weather data and soil type using a local LLM (phi3 via Ollama). Built with **Streamlit**, **OpenStreetMap**, **Open-Meteo**, and **Ollama** to support sustainable agriculture.

---

## 🔍 Overview

Many farmers face reduced crop yields due to generic farming advice and lack of access to localized resources. This AI-powered tool provides personalized crop recommendations by:

- 🌍 Taking location input (e.g., city/district)
- ☁️ Fetching real historical climate data (temperature & rainfall)
- 🧠 Using a local LLM (phi3) to analyze the inputs and suggest suitable crops
- 💻 Displaying results in a user-friendly Streamlit interface

---

## 🎯 Key Features

- 📍 Location-to-coordinates conversion using OpenStreetMap (Nominatim)
- 📊 Weather data via Open-Meteo Archive API
- 🧠 AI crop advisor powered by **phi3 LLM** running locally with **Ollama**
- 🌱 Inputs include soil type and region
- 📈 Real-time climate metrics & interactive UI
- ✅ Fully offline AI processing (no cloud LLMs required)

---

## 🛠 Tech Stack

| Component         | Description                           |
|------------------|---------------------------------------|
| Streamlit        | Interactive frontend                   |
| Ollama (phi3)    | Local LLM for crop suggestions         |
| Open-Meteo API   | Historical weather data (free)         |
| OpenStreetMap    | Geo-coordinates lookup for location    |
| Python 3.13      | Backend & data handling                |

---

