import os
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel


class CabinInformation(BaseModel):
    cabin_number: str
    cabin_type: str
    cabin_category: str

class PassengerInformation(BaseModel):
    passenger_name: str
    passenger_email: str

class DataPipeline:
    def __init__(self):
        # Set up Jinja environment
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template("reservation_prompt.j2")

    def create_prompt_from_reservation_data(self, reservation_data: dict) -> str:
        """Create a prompt from reservation data."""
        start_date = self.extract_start_date_from_reservation_data(reservation_data)
        cabin_information_list = self.extract_cabin_information_from_reservation_data(reservation_data)
        passenger_information = self.extract_passenger_information_from_reservation_data(reservation_data)

        # Render the template with the data
        prompt = self.template.render(
            start_date=start_date,
            cabins=cabin_information_list,
            passengers=passenger_information
        )
        
        return prompt
    
    def extract_start_date_from_reservation_data(self, reservation_data: dict) -> datetime:
        """Extract the start date from the reservation data."""
        reservation_data_start_date = reservation_data["startDateTime"]
        return datetime.strptime(reservation_data_start_date, "%Y-%m-%dT%H:%M:%S")
    
    def _get_unique_cabins(self, cabins: list[dict]) -> list[dict]:
        """Get the unique cabins from the reservation data based on category and cabin number."""
        unique_cabins = []
        seen = set()
        
        for cabin in cabins:
            # Create a unique key based on category and cabin number
            key = (cabin["category"], cabin["cabinNumber"])
            
            # Only add if we haven't seen this combination before
            if key not in seen:
                seen.add(key)
                unique_cabins.append(cabin)
                
        return unique_cabins
    
    def extract_cabin_information_from_reservation_data(self, reservation_data: dict) -> list[CabinInformation]:
        """Extract the cabin information from the reservation data."""
        passenger_groups = reservation_data["passengerGroups"]
        sailings = passenger_groups[0]["sailings"]
        cabins = sailings[0]["cabins"]
        unique_cabins = self._get_unique_cabins(cabins)

        return [CabinInformation(
            cabin_number=cabin["cabinNumber"],
            cabin_type=cabin.get("passengerDetails", [{}])[0].get("seawareStageType", "Unknown"),
            cabin_category=cabin["category"],
        ) for cabin in unique_cabins]
    

    def extract_passenger_information_from_reservation_data(self, reservation_data: dict) -> list[PassengerInformation]:
        """Extract the passenger information from the reservation data."""
        passenger_groups = reservation_data["passengerGroups"]
        passengers = passenger_groups[0]["passengers"]
        return [PassengerInformation(
            passenger_name=passenger["name"],
            passenger_email=passenger["email"],
        ) for passenger in passengers]