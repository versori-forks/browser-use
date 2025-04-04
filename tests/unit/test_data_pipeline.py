import datetime
import json

import pytest

from browser_use.data_pipeline.data_pipeline import (
    CabinInformation,
    DataPipeline,
    PassengerInformation,
)


class TestDataPipeline:
    def test_structuring_agent_instructions_from_json(self):
        """Test that the structuring agent instructions are correctly structured from the json file"""
        
        # Arrange
        with open("tests/unit/data/synthetic_data.json", "r") as f:
            json_data = json.load(f)
        data_pipeline = DataPipeline()
        expected_prompt = """
        1. Navigate and login:
            - Navigate to https://sandbox.reservations.travelhx.com/touch
            - Login using user name VR_Patrick and password SEAWARE_PASSWORD. Once logged in, it will say 'Logged in as: VR_Patrick' at the top of the screen
        2. Creating new reservation and finding the correct tour:
            - Click New Reservation at bottom of screen
            - Click on element by index with id 13
            - In the calendar under "Select the tour you prefer from the list below", click on the second year dropdown where it says 2025 and click on 2028 using the select_dropdown_option function
            - In the dropdown for month, using the select_dropdown_option function, click on the month where it says March
            - Wait 5 seconds for the page to load
            - Click on the tile on the day 18 of the month. It should be highlighted in blue once selected
            - Check the tour is on the correct Tour Start date 18 Mar 2028. Repeat this check until the tour is on the correct date. It is CRITICAL that the tour is on the correct date. Click on the tile with the day 18 if it isn't on the correct date.
            - Find the select checkbox and click on it if it is not already selected. It should be in the bottom right of the screen (below the cost). A green tick should appear once selected
            - Click continue
        3. Selecting the correct cabin:
            - Use extract_content with goal "Find the cabin with code N2 in the list of available cabins and identify its row index."
            - Click on the plus button for the cabin with code N2
            - Verify the selection by using extract_content with goal "List all selected cabins and their quantities, confirming the Outside Cabin with code N2 has quantity 1"
            - If the wrong row is selected:
                - Click the bin icon to remove it
                - Use extract_content with goal "After removal, list all cabin rows and their current selection state"
                - Try selecting the row with index-1 if the previous attempt was at index-0, or vice versa
            - Click continue
            - Click the "Change" button
            - Search for the cabin 336 in the Stateroom box by typing it in and pressing enter
            - Click the select button select the cabin 336
            - Verify that the cabin number is 336 is selected 
            - Click accept"""

        # Act
        prompt = data_pipeline.create_prompt_from_reservation_data(json_data)

        # Assert
        assert prompt == expected_prompt

    def test_extracting_date_from_reservation_data(self):
        """Test that the date is correctly extracted from the reservation data"""

        # Arrange
        with open("tests/unit/data/synthetic_data.json", "r") as f:
            json_data = json.load(f)
        
        data_pipeline = DataPipeline()
        expected_date = datetime.datetime(2028, 3, 18, 0, 0)

        # Act
        date = data_pipeline.extract_start_date_from_reservation_data(json_data)

        # Assert
        assert date == expected_date

    def test_extracting_cabin_information_from_reservation_data(self):
        """Test that the cabin information is correctly extracted from the reservation data"""

        # Arrange
        with open("tests/unit/data/synthetic_data.json", "r") as f:
            json_data = json.load(f)

        data_pipeline = DataPipeline()
        expected_cabin_information = [
            CabinInformation(
                cabin_number="336",
                cabin_type="Outside Cabin",
                cabin_category="N2",
            )
        ]

        # Act
        cabin_information = data_pipeline.extract_cabin_information_from_reservation_data(json_data)

        # Assert
        assert cabin_information == expected_cabin_information

    def test_extracting_passenger_information_from_reservation_data(self):
        """Test that the passenger information is correctly extracted from the reservation data"""

        # Arrange
        with open("tests/unit/data/synthetic_data.json", "r") as f:
            json_data = json.load(f)
            
        data_pipeline = DataPipeline()
        expected_passenger_information = [
            PassengerInformation(
                passenger_name="FREDI KRUGER",
                passenger_email="test@test.com",
            ),
            PassengerInformation(
                passenger_name="TEST JEAN PIERRE LAFFONT",
                passenger_email="test.fr@icloud.com",
            )
        ]

        # Act
        passenger_information = data_pipeline.extract_passenger_information_from_reservation_data(json_data)

        # Assert
        assert passenger_information == expected_passenger_information


    def test_creating_prompt_where_passengers_staying_in_different_cabins(self):
        """Test that the prompt is correctly created where passengers are staying in different cabins"""

        # Arrange
        with open("tests/unit/data/reservation_different_cabings.json", "r") as f:
            json_data = json.load(f)
            
        data_pipeline = DataPipeline()
        expected_prompt = """
        1. Navigate and login:
            - Navigate to https://sandbox.reservations.travelhx.com/touch
            - Login using user name VR_Patrick and password SEAWARE_PASSWORD. Once logged in, it will say 'Logged in as: VR_Patrick' at the top of the screen
        2. Creating new reservation and finding the correct tour:
            - Click New Reservation at bottom of screen
            - Click on element by index with id 13
            - In the calendar under "Select the tour you prefer from the list below", click on the second year dropdown where it says 2025 and click on 2028 using the select_dropdown_option function
            - In the dropdown for month, using the select_dropdown_option function, click on the month where it says March
            - Wait 5 seconds for the page to load
            - Click on the tile on the day 18 of the month. It should be highlighted in blue once selected
            - Check the tour is on the correct Tour Start date 18 Mar 2028. Repeat this check until the tour is on the correct date. It is CRITICAL that the tour is on the correct date. Click on the tile with the day 18 if it isn't on the correct date.
            - Find the select checkbox and click on it if it is not already selected. It should be in the bottom right of the screen (below the cost). A green tick should appear once selected
            - Click continue
        3. Selecting the correct cabin:
            - Use extract_content with goal "Find the cabin with code N2 in the list of available cabins and identify its row index."
            - Click on the plus button for the cabin with code N2
            - Verify the selection by using extract_content with goal "List all selected cabins and their quantities, confirming the Outside Cabin with code N2 has quantity 1"
            - If the wrong row is selected:
                - Click the bin icon to remove it
                - Use extract_content with goal "After removal, list all cabin rows and their current selection state"
                - Try selecting the row with index-1 if the previous attempt was at index-0, or vice versa
            - Use extract_content with goal "Find the cabin with code Q2 in the list of available cabins and identify its row index."
            - Click on the plus button for the cabin with code Q2
            - Verify the selection by using extract_content with goal "List all selected cabins and their quantities, confirming the Expedition suite, mini suite with code Q2 has quantity 1"
            - If the wrong row is selected:
                - Click the bin icon to remove it
                - Use extract_content with goal "After removal, list all cabin rows and their current selection state"
                - Try selecting the row with index-1 if the previous attempt was at index-0, or vice versa
            - Click continue
            - Click the "Change" button
            - Search for the cabin 336 in the Stateroom box by typing it in and pressing enter
            - Click the select button select the cabin 336
            - Verify that the cabin number is 336 is selected 
            - Click accept
            - Click the "Change" button
            - Search for the cabin 528 in the Stateroom box by typing it in and pressing enter
            - Click the select button select the cabin 528
            - Verify that the cabin number is 528 is selected 
            - Click accept"""

        # Act
        prompt = data_pipeline.create_prompt_from_reservation_data(json_data)

        # Assert
        assert prompt == expected_prompt

    @pytest.mark.parametrize(
        "input_cabins,expected_unique_cabins,test_description",
        [
            (
                [
                    {"category": "N2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                    {"category": "N2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                ],
                [
                    {"category": "N2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                ],
                "Same cabin category and number should be deduplicated",
            ),
            (
                [
                    {"category": "N2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                    {"category": "Q2", "cabinNumber": "528", "passengerDetails": [{"seawareStageType": "Expedition suite, mini suite"}]},
                ],
                [
                    {"category": "N2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                    {"category": "Q2", "cabinNumber": "528", "passengerDetails": [{"seawareStageType": "Expedition suite, mini suite"}]},
                ],
                "Different cabin categories and numbers should be kept",
            ),
            (
                [
                    {"category": "N2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                    {"category": "N2", "cabinNumber": "337", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                ],
                [
                    {"category": "N2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                    {"category": "N2", "cabinNumber": "337", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                ],
                "Same category but different cabin numbers should be kept",
            ),
            (
                [
                    {"category": "N2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                    {"category": "Q2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Expedition suite, mini suite"}]},
                ],
                [
                    {"category": "N2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Outside Cabin"}]},
                    {"category": "Q2", "cabinNumber": "336", "passengerDetails": [{"seawareStageType": "Expedition suite, mini suite"}]},
                ],
                "Same cabin number but different categories should be kept",
            ),
            (
                [],
                [],
                "Empty list should return empty list",
            ),
        ],
    )
    def test_get_unique_cabins(self, input_cabins, expected_unique_cabins, test_description):
        """Test the _get_unique_cabins method with various scenarios."""
        # Arrange
        data_pipeline = DataPipeline()
        
        # Act
        result = data_pipeline._get_unique_cabins(input_cabins)
        
        # Assert
        assert len(result) == len(expected_unique_cabins), f"Expected {len(expected_unique_cabins)} unique cabins, got {len(result)}"
        
        # Check that each expected cabin is in the result
        for expected_cabin in expected_unique_cabins:
            found = False
            for result_cabin in result:
                if (result_cabin["category"] == expected_cabin["category"] and 
                    result_cabin["cabinNumber"] == expected_cabin["cabinNumber"]):
                    found = True
                    break
            assert found, f"Expected cabin {expected_cabin} not found in result"
