from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from browser_use.data_pipeline.reservation_data import (
    Cabin,
    CabinInformation,
    PassengerInformation,
    Reservation,
)


class DataPipeline:
    def __init__(self, reservation_data: dict):
        # Set up Jinja environment
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template("reservation_prompt.j2")
        self.reservation_data = Reservation.model_validate(reservation_data)

    def create_prompt_from_reservation_data(self) -> str:
        """Create a prompt from reservation data."""        
        start_date = self.extract_start_date_from_reservation_data()
        cabin_information_list = self.extract_cabin_information_from_reservation_data()
        passenger_information = self.extract_passenger_information_from_reservation_data()

        prompt = self.template.render(
            start_date=start_date,
            cabins=cabin_information_list,
            passengers=passenger_information
        )
        
        return prompt
    
    def extract_start_date_from_reservation_data(self) -> datetime:
        """Extract the start date from the reservation data."""
        return self.reservation_data.start_date_time
    
    def _get_unique_cabins(self, cabins: list[Cabin]) -> list[Cabin]:
        """Get the unique cabins from the reservation data based on category and cabin number."""
        unique_cabins = []
        seen = set()
        
        for cabin in cabins:
            key = (cabin.category, cabin.cabin_number)
            
            if key not in seen:
                seen.add(key)
                unique_cabins.append(cabin)
                
        return unique_cabins
    
    def extract_cabin_information_from_reservation_data(self) -> list[CabinInformation]:
        """Extract the cabin information from the reservation data."""
        passenger_group = self.reservation_data.passenger_groups[0]
        sailing = passenger_group.sailings[0]
        unique_cabins = self._get_unique_cabins(sailing.cabins)

        return [CabinInformation(
            cabin_number=cabin.cabin_number,
            cabin_type=cabin.passenger_details[0].seaware_stage_type if cabin.passenger_details else "Unknown",
            cabin_category=cabin.category,
        ) for cabin in unique_cabins]
    

    def extract_passenger_information_from_reservation_data(self) -> list[PassengerInformation]:
        """Extract the passenger information from the reservation data."""
        passenger_group = self.reservation_data.passenger_groups[0]
        return [PassengerInformation(
            passenger_name=passenger.name,
            passenger_email=passenger.email,
        ) for passenger in passenger_group.passengers]