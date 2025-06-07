# app.py - Fixed version

import streamlit as st
from main import FoodieTourWorkflow

st.set_page_config(
    page_title="Foodie Tour Planner",
    layout="wide"
)

st.title("🌍 Foodie Tour Planner")
st.markdown("Plan culinary adventures around the world — based on local dishes, weather, and top-rated restaurants.")

# Sidebar
st.sidebar.header("Plan Your Tour")
city_input = st.sidebar.text_area(
    "Enter city names (comma-separated):",
    value="Paris, Tokyo, New York"
)

# Add dining preference selection
dining_preference = st.sidebar.selectbox(
    "Select your dining preference:",
    ["Weather-based (Auto)", "Indoor", "Outdoor"]
)

# Add dietary restrictions
dietary_restrictions = st.sidebar.multiselect(
    "Dietary restrictions (optional):",
    ["Non Vegetarian", "Vegetarian", "Vegan", "Gluten-free", "Dairy-free"]
)

run_button = st.sidebar.button("Create Foodie Tour")

# Instantiate workflow
workflow = FoodieTourWorkflow()

if run_button:
    cities = [c.strip() for c in city_input.split(",") if c.strip()]

    if not cities:
        st.warning("Please enter at least one valid city name.")
    else:
        st.info("Running foodie tour workflow...")
        with st.spinner("Generating tours..."):
            # Pass dining preferences to workflow
            results = workflow.run_workflow(cities, dining_preference, dietary_restrictions)

        for result in results:
            st.markdown(f"## 📍 {result['city']}")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🌤️ Weather")
                st.write(f"**Description:** {result['weather']['description']}")
                st.write(f"**Temperature:** {result['weather']['temperature']}°C")
                st.write(f"**Humidity:** {result['weather']['humidity']}%")
                st.write(f"**Dining Preference:** {result['dining_type'].capitalize()}")

            with col2:
                st.subheader("🍽️ Iconic Dishes")
                for dish in result['dishes']:
                    st.write(f"- {dish}")

                st.subheader("🏪 Restaurants")
                for restaurant in result['restaurants']:
                    st.write(f"- {restaurant}")

            with st.expander("📖 Full Tour Narrative"):
                st.markdown(result['tour_narrative'])

            st.markdown("---")