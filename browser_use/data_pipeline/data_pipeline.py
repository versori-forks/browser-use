from datetime import datetime

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
        pass

    def create_prompt_from_reservation_data(self, reservation_data: dict) -> str:
        """Create a prompt from reservation data."""
        start_date = self.extract_start_date_from_reservation_data(reservation_data)
        cabin_information = self.extract_cabin_information_from_reservation_data(reservation_data)[0]
        passenger_information = self.extract_passenger_information_from_reservation_data(reservation_data)

        prompt = f"""
        1. Navigate and login:
            - Navigate to https://sandbox.reservations.travelhx.com/touch
            - Login using user name VR_Patrick and password SEAWARE_PASSWORD. Once logged in, it will say 'Logged in as: VR_Patrick' at the top of the screen
        2. Creating new reservation and finding the correct tour:
            - Click New Reservation at bottom of screen
            - Click on element by index with id 13
            - In the calendar under "Select the tour you prefer from the list below", click on the second year dropdown where it says 2025 and click on {start_date.year} using the select_dropdown_option function
            - In the dropdown for month, using the select_dropdown_option function, click on the month where it says {start_date.strftime("%B")}
            - Wait 5 seconds for the page to load
            - Click on the tile on the day {start_date.day} of the month. It should be highlighted in blue once selected
            - Check the tour is on the correct Tour Start date {start_date.strftime("%d %b %Y")}. Repeat this check until the tour is on the correct date. It is CRITICAL that the tour is on the correct date. Click on the tile with the day {start_date.day} if it isn't on the correct date.
            - Find the select checkbox and click on it if it is not already selected. It should be in the bottom right of the screen (below the cost). A green tick should appear once selected
            - Click continue
        3. Selecting the correct cabin:
            - Use extract_content with goal "Find the cabin with code {cabin_information.cabin_category} in the list of available cabins and identify its row index."
            - Click on the plus button for the cabin with code {cabin_information.cabin_category}
            - Verify the selection by using extract_content with goal "List all selected cabins and their quantities, confirming the {cabin_information.cabin_type} with code {cabin_information.cabin_category} has quantity 1"
            - If the wrong row is selected:
                - Click the bin icon to remove it
                - Use extract_content with goal "After removal, list all cabin rows and their current selection state"
                - Try selecting the row with index-1 if the previous attempt was at index-0, or vice versa
            - Click continue
            - Click the "Change" button
            - Search for the cabin {cabin_information.cabin_number} in the Stateroom box by typing it in and pressing enter
            - Click the select button select the cabin {cabin_information.cabin_number}
            - Verify that the cabin number is {cabin_information.cabin_number} is selected 
            - Click accept
        """

        return prompt
    
    def extract_start_date_from_reservation_data(self, reservation_data: dict) -> datetime:
        """Extract the start date from the reservation data."""
        reservation_data_start_date = reservation_data["startDateTime"]
        return datetime.strptime(reservation_data_start_date, "%Y-%m-%dT%H:%M:%S")
    
    def extract_cabin_information_from_reservation_data(self, reservation_data: dict) -> list[CabinInformation]:
        """Extract the cabin information from the reservation data."""
        passenger_groups = reservation_data["passengerGroups"]
        sailings = passenger_groups[0]["sailings"]
        cabins = sailings[0]["cabins"]

        return [CabinInformation(
            cabin_number=cabin["cabinNumber"],
            cabin_type=cabin.get("passengerDetails")[0]["seawareStageType"],
            cabin_category=cabin["category"],
        ) for cabin in cabins]
    

    def extract_passenger_information_from_reservation_data(self, reservation_data: dict) -> list[PassengerInformation]:
        """Extract the passenger information from the reservation data."""
        passenger_groups = reservation_data["passengerGroups"]
        passengers = passenger_groups[0]["passengers"]
        return [PassengerInformation(
            passenger_name=passenger["name"],
            passenger_email=passenger["email"],
        ) for passenger in passengers]