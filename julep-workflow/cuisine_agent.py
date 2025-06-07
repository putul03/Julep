from julep import Julep
import yaml
import time
import os
from typing import List


class CuisineAgent:
    def __init__(self):
        self.client = Julep(api_key=os.getenv('JULEP_API_KEY'))
        self.agent = self._create_agent()
        self.dishes_task = self._create_dishes_task()
        self.restaurants_task = self._create_restaurants_task()

    def _create_agent(self):
        """Create the foodie agent"""
        return self.client.agents.create(
            name="Foodie Guide",
            model="gpt-4o",
            about="A culinary expert that knows local dishes and restaurants worldwide."
        )

    def _create_dishes_task(self):
        """Create task to get iconic local dishes"""
        task_definition = yaml.safe_load("""
    name: Get Local Dishes
    description: Get 3 iconic local dishes for a city
    main:
    - prompt:
        - role: system
          content: You are a culinary expert. Provide exactly 3 iconic local dishes for the given city.
        - role: user
          content: "List 3 iconic local dishes from {{steps[0].input.city}}. Return only the dish names, one per line, no descriptions."
    """)
        return self.client.tasks.create(
            agent_id=self.agent.id,
            **task_definition
        )

    def _create_restaurants_task(self):
        """Create task to find restaurants"""
        task_definition = yaml.safe_load("""
        name: Find Restaurants
        description: Find top-rated restaurants for specific dishes
        main:
        - prompt:
            - role: system
              content: You are a restaurant guide expert. Provide restaurant recommendations.
            - role: user
              content: "For {{steps[0].input.city}}, suggest 1 top-rated restaurant for each dish: {{steps[0].input.dishes}}. Return ONLY the restaurant suggestions, one per line, in the format 'Dish - Restaurant Name'. Do not include any introductory text or explanations."
        """)
        return self.client.tasks.create(
            agent_id=self.agent.id,
            **task_definition
        )

    def get_local_dishes(self, city: str) -> List[str]:
        """Get 3 iconic local dishes for a city"""
        execution = self.client.executions.create(
            task_id=self.dishes_task.id,
            input={"city": city}
        )
        result = self._wait_for_completion(execution.id)
        if result.status == "succeeded":
            output_text = ""
            if isinstance(result.output, dict) and 'choices' in result.output:
                choices = result.output.get('choices', [])
                if choices and isinstance(choices, list) and 'message' in choices[0]:
                    output_text = choices[0]['message'].get('content', '')
            dishes = [dish.strip() for dish in output_text.split('\n') if dish.strip()]
            return dishes[:3]
        return [f"{city} Special Dish {i + 1}" for i in range(3)]

    def find_restaurants(self, city: str, dishes: List[str]) -> List[str]:
        """Find restaurants for the dishes"""
        dishes_str = ", ".join(dishes)
        execution = self.client.executions.create(
            task_id=self.restaurants_task.id,
            input={"city": city, "dishes": dishes_str}
        )
        result = self._wait_for_completion(execution.id)
        if result.status == "succeeded":
            output_text = ""
            if isinstance(result.output, dict) and 'choices' in result.output:
                choices = result.output.get('choices', [])
                if choices and isinstance(choices, list) and 'message' in choices[0]:
                    output_text = choices[0]['message'].get('content', '')
            restaurants = [
                rest.strip() for rest in output_text.split('\n')
                if rest.strip() and '-' in rest
            ]
            return restaurants
        return [f"Restaurant for {dish}" for dish in dishes]

    def _wait_for_completion(self, execution_id: str):
        """Wait for task execution to complete"""
        while True:
            result = self.client.executions.get(execution_id)
            if result.status in ['succeeded', 'failed']:
                return result
            time.sleep(1)


if __name__ == "__main__":
    cuisine_agent = CuisineAgent()
    city = "Tokyo"
    dishes = cuisine_agent.get_local_dishes(city)
    print(f"Local dishes in {city}:")
    for dish in dishes:
        print(f"- {dish}")
    restaurants = cuisine_agent.find_restaurants(city, dishes)
    print(f"\nRestaurants in {city}:")
    for restaurant in restaurants:
        print(f"- {restaurant}")

"""
#example code
if __name__ == "__main__":
    cuisine_agent = CuisineAgent()
    city = "Tokyo"
    dishes = cuisine_agent.get_local_dishes(city)
    print(f"Local dishes in {city}:")
    for dish in dishes:
        print(f"- {dish}")
    restaurants = cuisine_agent.find_restaurants(city, dishes)
    print(f"\nRestaurants in {city}:")
    for restaurant in restaurants:
        print(f"- {restaurant}")
"""