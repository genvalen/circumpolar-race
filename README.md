# Circumpolar Race Around the World - Spreadsheet Generator



## Context
This project is based around the **Circumpolar Race Around the World 2020** event. This was a year-long virtual racing event where participants formed teams and committed to a year of walking/racing, and uploaded their daily mileage on this [site](https://runsignup.com/Race/CHH/AnywhereAnyPlace/CircumpolarRaceAroundtheWorld).

In brief, the program does the following:
* prompts the user to enter a team name
* exports an Excel spreadsheet summarizing and ranking the results of participants under this team name

**Note:** this program is a WIP and not yet fully functional. To try the program out locally, use the following test team as the input: In Jesper's Footsteps. 

Data for the test team's output is sourced [here](https://runsignup.com/RaceGroups/95983?groupName=In+Jesper%27s+Footsteps).


## Requirements
* See `requirements.txt`
* Python 3.9.7+

## How to Use
Run the app: `$ python app.py`

Test the app: `$ python -m unittest app_test.py`