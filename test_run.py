import asyncio

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from browser_use import Agent, Browser, BrowserConfig

load_dotenv()
import os

# prompt = """
# 1. Navigate and login:
#     - Navigate to https://sandbox.reservations.travelhx.com/touch
#     - wait 10 seconds for the page to load
#     - Login using user name VR_Patrick and password SEAWARE_PASSWORD. Once logged in, it will say 'Logged in as: VR_Patrick' at the top of the screen
# 2. Creating new reservation and finding the correct tour:
#     - Click New Reservation at bottom of screen
#     - Click on element by index with id 15
#     - In the calendar under "Select the tour you prefer from the list below", click on the second year dropdown where it says 2025 and click on 2028 using the select_dropdown_option function
#     - In the dropdown for month, using the select_dropdown_option function, click on the month where it says March
#     - Wait 5 seconds for the page to load
#     - Click on the tile on the day 18 of the month. It should be highlighted in blue once selected
#     - Check the tour is on the correct Tour Start date 18 Mar 2028. Repeat this check until the tour is on the correct date. It is CRITICAL that the tour is on the correct date. Click on the tile with the day 18 if it isn't on the correct date.
#     - Find the select checkbox and pick it. It should be in the bottom right of the screen (below the cost). A green tick should appear once selected
#     - Click continue
# 3. Selecting the correct cabin:
#     - Find the row for Outside Cabin. It has code N2. It should have this exact name. Do NOT click on a cabin number with a different code. Use  extract_content with goal "Find the row for Outside Cabin with code N2"
#     - Wait 5 seconds for the page to load
#     - Click on the plus button on the row for the Outside Cabin with code N2, so that a 1 should appear. Be careful not to click on the cabin above or below this one. Verify the row with the extracted data before clicking
#     - Check the + is on the row for the Outside Cabin with code N2
#     - Check if a different row is highlighted. Click the bin to remove it if so
#     - Click continue
#     - Click the "Change Stateroom" button
#     - Search for the cabin 327 in the Stateroom box by typing it in and pressing enter
#     - Click the select button select the cabin 327
#     - Verify that the cabin number is 327 is selected 
#     - Click accept
# """

# prompt = """
# 1. Navigate and login:
#     - Navigate to https://sandbox.reservations.travelhx.com/touch
#     - Login using user name VR_Patrick and password SEAWARE_PASSWORD. Once logged in, it will say 'Logged in as: VR_Patrick' at the top of the screen
# 2. Creating new reservation and finding the correct tour:
#     - Click New Reservation at bottom of screen
#     - Click on element by index with id 15
#     - In the calendar under "Select the tour you prefer from the list below", click on the second year dropdown where it says 2025 and click on 2028 using the select_dropdown_option function
#     - In the dropdown for month, using the select_dropdown_option function, click on the month where it says March
#     - Wait 5 seconds for the page to load
#     - Click on the tile on the day 18 of the month. It should be highlighted in blue once selected
#     - Check the tour is on the correct Tour Start date 18 Mar 2028. Repeat this check until the tour is on the correct date. It is CRITICAL that the tour is on the correct date. Click on the tile with the day 18 if it isn't on the correct date.
#     - Find the select checkbox and pick it. It should be in the bottom right of the screen (below the cost). A green tick should appear once selected
#     - Click continue
# 3. Selecting the correct cabin:
#     - Use extract_content with goal "Find the cabin with code N2 in the list of available cabins and identify its row index."
#     - Click on the plus button for the cabin with code N2. IMPORTANT - note that the row index starts from 1 not 0, so click on the row with index -1 from previous step. - CRITICAL: When clicking the plus button, ALWAYS click on the row ABOVE the one you think is correct. For example, if you think N2 is in row 8, click row 7 instead
#     - Verify the selection by using extract_content with goal "List all selected cabins and their quantities, confirming the Outside Cabin with code N2 has quantity 1"
#     - If the wrong row is selected:
#         - Click the bin icon to remove it
#         - Use extract_content with goal "After removal, list all cabin rows and their current selection state"
#         - Try selecting the row with index-1 if the previous attempt was at index-0, or vice versa
#     - Click continue
#     - Click the "Change Stateroom" button
#     - Search for the cabin 327 in the Stateroom box by typing it in and pressing enter
#     - Click the select button select the cabin 327
#     - Verify that the cabin number is 327 is selected 
#     - Click accept
# """

# prompt = """
# 1. Navigate and login:
#     - Navigate to https://sandbox.reservations.travelhx.com/touch
#     - Login using user name VR_Patrick and password SEAWARE_PASSWORD. Once logged in, it will say 'Logged in as: VR_Patrick' at the top of the screen
# 2. Selecting the correct cabin:
#     - Zoom out so that all cabins are in view
#     - Use extract_content with goal "Find the cabin with code N2 in the list of available cabins and identify its row index."
#     - scroll to text "N2" to that N2 is in view
#     - Click on the plus button for the cabin one above the cabin with code N2
#     - If the wrong row is selected:
#         - Click the bin icon to remove it
#         - Use extract_content with goal "After removal, list all cabin rows and their current selection state"
#         - Try selecting the row with index-1 if the previous attempt was at index-0, or vice versa
#     - Click continue
#     - Click the "Change Stateroom" button
#     - Search for the cabin 327 in the Stateroom box by typing it in and pressing enter
#     - Click the select button select the cabin 327
#     - Verify that the cabin number is 327 is selected 
#     - Click accept
# """


### Zoomed out prompt with Chrome browser (80% zoom)
prompt = """
1. Navigate and login:
    - Navigate to https://sandbox.reservations.travelhx.com/touch
    - Login using user name VR_Patrick and password SEAWARE_PASSWORD. Once logged in, it will say 'Logged in as: VR_Patrick' at the top of the screen
2. Creating new reservation and finding the correct tour:
    - Click New Reservation at bottom of screen
    - Click on element by index with id 14
    - In the calendar under "Select the tour you prefer from the list below", click on the second year dropdown where it says 2025 and click on 2028 using the select_dropdown_option function
    - In the dropdown for month, using the select_dropdown_option function, click on the month where it says March
    - Wait 5 seconds for the page to load
    - Click on the tile on the day 18 of the month. It should be highlighted in blue once selected
    - Check the tour is on the correct Tour Start date 18 Mar 2028. Repeat this check until the tour is on the correct date. It is CRITICAL that the tour is on the correct date. Click on the tile with the day 18 if it isn't on the correct date.
    - Find the select checkbox and pick it. It should be in the bottom right of the screen (below the cost). A green tick should appear once selected
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
    - Click the "Change Stateroom" button
    - Search for the cabin 327 in the Stateroom box by typing it in and pressing enter
    - Click the select button select the cabin 327
    - Verify that the cabin number is 327 is selected 
    - Click accept
"""

async def main():
   # Configure the browser with your Chrome path and user data directory
    browser = Browser(
        config=BrowserConfig(
            browser_binary_path="/Users/patrick/Library/Caches/ms-playwright/chromium-1161/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
            extra_browser_args=[
                "--user-data-dir=/Users/patrick/Library/Application Support/Chromium"
            ]
        )
    )
    
    agent = Agent(
        task=prompt,
        llm=ChatAnthropic(model_name="claude-3-7-sonnet-20250219", temperature=0.0),
        generate_gif=True,
        use_vision=True,
        sensitive_data={"SEAWARE_PASSWORD": os.getenv("SEAWARE_PASSWORD")},
        browser=browser
    )
    await agent.run()

asyncio.run(main())