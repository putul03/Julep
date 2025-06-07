# Foodie Tour Planner

## Description
This project is an AI-powered foodie tour planning assistant that creates personalized culinary adventures around the world. The system combines real-time weather data, local cuisine expertise, and restaurant recommendations to generate comprehensive food tours tailored to user preferences and dietary requirements.

## Features
* **Intelligent Cuisine Discovery:** Identifies iconic local dishes for any city using AI agents
* **Restaurant Recommendations:** Finds top-rated restaurants for each local dish
* **Weather-Aware Planning:** Integrates real-time weather to suggest indoor/outdoor dining
* **Dietary Preferences:** Supports various dietary restrictions (vegetarian, vegan, gluten-free, halal, kosher, dairy-free)
* **Personalized Tour Narratives:** Creates engaging day-long food tour stories with breakfast, lunch, and dinner recommendations
* **Web Interface:** User-friendly Streamlit web application for easy tour planning
* **Global Coverage:** Works with cities worldwide using Open-Meteo weather API

## Prerequisites
* Python 3.8+
* pip (Python package installer)
* Julep API key (for AI agents)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/putul03/Julep.git
   cd foodie-tour-planner
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   * On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   * On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

This project uses a `.env` file for managing environment variables.

1. Create a file named `.env` in the root directory of the project.
2. Add your Julep API key:
   ```env
   JULEP_API_KEY="your_julep_api_key_here"
   ```

## Usage

### Web Application (Recommended)

Launch the Streamlit web interface for an interactive experience:

```bash
streamlit run app.py
```

#### Web Interface Features:
* Enter multiple cities (comma-separated)
* Select dining preferences: Weather-based (Auto), Indoor, Outdoor, Vegetarian, Non-vegetarian, Mixed
* Choose dietary restrictions from multiple options
* View comprehensive tour results with weather, dishes, restaurants, and full narratives

### Command Line Interface

Run the core workflow directly:

```bash
python main.py
```

This will generate foodie tours for the default cities (Paris, Tokyo, New York).

### Individual Components

Test individual components:

```bash
# Test weather service
python weather_service.py

# Test cuisine agent
python cuisine_agent.py

# Test tour planner
python tour_planner.py
```

## Project Structure

```
foodie-tour-planner/
├── app.py                 # Streamlit web interface
├── main.py               # Main workflow orchestrator
├── cuisine_agent.py      # AI agent for finding local dishes and restaurants
├── tour_planner.py       # AI agent for creating tour narratives
├── weather_service.py    # Weather data service using Open-Meteo API
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
└── README.md            # This file
```
