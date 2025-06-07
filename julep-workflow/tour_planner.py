# tour_planner.py - Fixed version

from julep import Julep
import yaml
import time
import os
from typing import Dict, Any, List


class TourPlanner:
    def __init__(self):
        self.client = Julep(api_key=os.getenv('JULEP_API_KEY'))
        self.agent = self._create_agent()
        self.tour_task = self._create_tour_task()

    def _create_agent(self):
        """Create the tour planning agent"""
        try:
            agent = self.client.agents.create(
                name="Foodie Tour Planner",
                model="gpt-4o",
                about="A creative tour planner that crafts delightful foodie experiences based on specific city information."
            )
            print(f"Agent created successfully with ID: {agent.id}")
            return agent
        except Exception as e:
            print(f"Failed to create agent: {e}")
            raise

    def _create_tour_task(self):
        """Create task to plan a foodie tour"""
        task_definition = {
            "name": "Create Foodie Tour",
            "description": "Create a delightful one-day foodie tour narrative for a specific city",
            "main": [
                {
                    "prompt": [
                        {
                            "role": "system",
                            "content": """You are a creative foodie tour planner. Create a one-day foodie tour plan for the EXACT city provided in the user message. 

IMPORTANT: 
- Use ONLY the city name provided in the user message
- Reference the specific weather conditions provided
- Use the exact restaurants listed
- Consider dietary restrictions if mentioned
- Format with clear headers: ## Breakfast, ## Lunch, ## Dinner
- Keep descriptions engaging but concise
- Ensure all information matches the provided city

Do not use examples from other cities or generic templates."""
                        },
                        {
                            "role": "user",
                            "content": "{{user_message}}"
                        }
                    ]
                }
            ]
        }

        try:
            task = self.client.tasks.create(
                agent_id=self.agent.id,
                **task_definition
            )
            print(f"Task created successfully with ID: {task.id}")
            return task
        except Exception as e:
            print(f"Failed to create task: {e}")
            raise

    def create_tour(self, city: str, weather_data: Dict[str, Any],
                    dining_type: str, restaurants: List[str],
                    dietary_restrictions: List[str] = None) -> str:
        """Create a foodie tour narrative"""
        try:
            # Prepare dietary restrictions text
            dietary_text = ""
            if dietary_restrictions and dietary_restrictions != ["None"]:
                dietary_text = f"\n- Dietary restrictions: {', '.join(dietary_restrictions)}"

            user_message = f"""Create a delightful one-day foodie tour for {city}, India.

CITY: {city}
WEATHER: {weather_data['description']} ({weather_data['temperature']}°C)
DINING PREFERENCE: {dining_type}
RESTAURANTS: {', '.join(restaurants)}{dietary_text}

Create a tour narrative with:
- ## Breakfast
- ## Lunch  
- ## Dinner

Important: Use ONLY {city} as the location. Reference the {weather_data['temperature']}°C temperature and {weather_data['description']} weather. Use the provided restaurants in your recommendations."""

            execution = self.client.executions.create(
                task_id=self.tour_task.id,
                input={
                    "user_message": user_message
                }
            )

            print(f"Execution created with ID: {execution.id}")
            result = self._wait_for_completion(execution.id)

            if result.status == "succeeded" and hasattr(result, 'output') and result.output:
                # Extract the content from the response
                if isinstance(result.output, dict) and 'choices' in result.output:
                    content = result.output['choices'][0]['message']['content']
                    # Verify the response contains our city name
                    if city.lower() in content.lower():
                        return content
                    else:
                        print(f"Response doesn't contain {city}. Using fallback.")
                        return self._create_fallback_tour(city, weather_data, dining_type, restaurants,
                                                          dietary_restrictions)
                else:
                    print("Unexpected output structure. Using fallback.")
                    return self._create_fallback_tour(city, weather_data, dining_type, restaurants,
                                                      dietary_restrictions)
            else:
                print(f"Execution failed. Status: {result.status}")
                return self._create_fallback_tour(city, weather_data, dining_type, restaurants, dietary_restrictions)

        except Exception as e:
            print(f"Exception occurred: {e}")
            return self._create_fallback_tour(city, weather_data, dining_type, restaurants, dietary_restrictions)

    def _create_fallback_tour(self, city: str, weather_data: Dict[str, Any],
                              dining_type: str, restaurants: List[str],
                              dietary_restrictions: List[str] = None) -> str:
        """Create a fallback tour when API fails"""
        weather_desc = weather_data['description']
        temp = weather_data['temperature']

        # Handle dietary restrictions
        dietary_note = ""
        if dietary_restrictions and dietary_restrictions != ["None"]:
            dietary_note = f" (accommodating {', '.join(dietary_restrictions)} preferences)"

        # Weather-appropriate dining suggestion
        weather_note = ""
        if temp > 30:
            weather_note = "Stay cool with refreshing beverages and light meals. "
        elif temp < 15:
            weather_note = "Warm up with hearty, comforting dishes. "

        # Dining type context
        dining_context = ""
        if dining_type == "indoor":
            dining_context = "enjoying air-conditioned comfort"
        elif dining_type == "outdoor":
            dining_context = "taking advantage of the pleasant weather"
        else:
            dining_context = f"experiencing {dining_type} cuisine"

        tour = f"""## Your Foodie Tour of {city}

**Weather**: {weather_desc} ({temp}°C)
**Dining Style**: {dining_type.capitalize()}{dietary_note}

{weather_note}Here's your perfect day exploring {city}'s culinary delights while {dining_context}.

## Breakfast
Start your morning at **{restaurants[0] if restaurants else 'a popular local breakfast spot'}**. Begin with traditional breakfast favorites that {city} is known for. The {weather_desc} weather at {temp}°C makes it {"perfect for a comfortable indoor breakfast" if temp > 30 or "rain" in weather_desc else "lovely for starting your day"}.

## Lunch  
Head to **{restaurants[1] if len(restaurants) > 1 else 'a renowned local restaurant'}** for an authentic {city} lunch experience. {"The warm weather calls for lighter fare and cooling drinks" if temp > 25 else "Perfect weather for enjoying hearty local specialties"}. This is your chance to taste the signature dishes that make {city} famous.

## Dinner
Conclude your culinary journey at **{restaurants[2] if len(restaurants) > 2 else 'a celebrated dinner destination'}**. End your day with the finest local cuisine {city} has to offer. {"The cooler evening temperature makes it ideal for a leisurely dinner" if temp > 20 else "A perfect way to warm up and reflect on your day"}.

*Experience the authentic flavors of {city} - a true culinary adventure!*"""

        return tour

    def _wait_for_completion(self, execution_id: str):
        """Wait for task execution to complete"""
        max_attempts = 30
        attempts = 0

        while attempts < max_attempts:
            result = self.client.executions.get(execution_id)
            if result.status in ['succeeded', 'failed']:
                return result
            time.sleep(1)
            attempts += 1

        return type('Result', (), {'status': 'timeout', 'output': None})()


# Example usage
if __name__ == "__main__":
    tour_planner = TourPlanner()

    city = "Kanpur"
    weather_data = {
        'temperature': 37,
        'description': 'mainly clear',
        'feels_like': 35,
        'humidity': 36
    }
    dining_type = "indoor"
    restaurants = [
        "Thaggu Ke Ladoo - Thaggu Ke Ladoo",
        "Baba Sweets' Samosa - Baba Sweets",
        "Kanpur Ki Nihari - Rahil's Nihari House"
    ]

    tour = tour_planner.create_tour(city, weather_data, dining_type, restaurants)
    print(f"Foodie Tour for {city}:\n{tour}")