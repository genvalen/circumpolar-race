from typing import List, Dict, Tuple, Set
import utils.writer as write
import pandas as pd
import glob
from bs4 import BeautifulSoup
import requests
from collections import defaultdict


def get_html(url="https://runsignup.com/RaceGroups" \
        "/95983?groupName=In+Jesper%27s+Footsteps"
        ) -> str:
    resp = requests.get(url).text
    soup = BeautifulSoup(resp, 'lxml')
    return soup


def get_region_paths() -> Dict[int, str]:
    """Return a dictionary that contains region numbers and a path to
    the webpage containing data for that region as a key-value pair.
    """
    soup = get_html()
    region_url_dict = {}

    # URL path and region numbers are scaped at dif iterations of loop;
    # path comes before region, so save path until region is found.

    path = ""
    for tag in soup.find_all('td'):

        # Search for URL to the next page
        match = tag.find_all(name='a', \
            class_='fs-lg d-block margin-t-10 margin-b-10 bold')

        if match:
            path = match[0]['href'].strip()

        # Search for the region that URL represents
        if "region" in tag.text.lower():
            region = int(tag.text.split()[1]) # extract region number
            region_url_dict[region] = path

    return region_url_dict


def get_identifiers(href: str) -> Tuple[str, str, str, str, str, str]:
    """Make HTTP request and, from the response, return the following
    participant identifiers: first name, last name, gender, age, city, and state.
    """
    # Prepare URL and header parameters for the HTTP request.
    url_base = "https://runsignup.com/Race/Results/95983/LookupParticipant/?"
    result_id, user_id = href.split("=")[1].split("#U") #parse HREF query portion
    result = f"resultSetId={result_id}&"
    user = f"userId={user_id}#U{user_id}"
    url = url_base+result+user
    headers = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept" : "application/json, */*; q=0.01",
        "Accept-Language" : "en-US,en;q=0.5",
        "X-Requested-With" : "XMLHttpRequest",
        "Connection" : "keep-alive",
        "Referer" : f"https://runsignup.com/Race/Results/95983/IndividualResult/?{result_id}",
        "Cookie" : "winWidth=1680; _ga=GA1.2.279797247.1629283759; __atuvc=128%7C36%2C6%7C37%2C11%7C38%2C38%7C39%2C4%7C40; cookie_policy_accepted=T; analytics={\"asset\":\"a1ca985c-904e-459a-bfd7-7480afe5b588\",\"source\":1,\"medium\":1}; PHPSESSID=9r2ImrtyrSszLIsWF2YCV3widCfGI9RJ; _mkto_trk=id:350-KBZ-109&token:_mch-runsignup.com-1632559648074-71989; _gid=GA1.2.2082540081.1633160300; __atuvs=615a3572229b618f002"
    }

    # Make HTTP request.
    resp = requests.get(url, headers=headers)

    # Convert response to JSON obj and parse relevant output.
    # If error, return empty dictionary.
    try:
        resp_dict = resp.json()['participants'][0]
        keys = ['first_name', 'last_name', 'gender', 'age', 'city', 'state']
        data = tuple(resp_dict[k] for k in keys)
    except:
        data = {}

    return data


def get_participant_data() -> Tuple[
    Set[str],
    Dict[int, Dict[str, float]],
    Tuple[str]
]:
    """Return a tuple containing 3 items:
        1) a set of participants' full names

        2) a dict of participant race results where the key is region number
            and the value is a dict of participants (k) and mileage (v)
            for that region.

        3) a list of tuples where each tuple contains participant identifers:
            name, gender, and age
    """
    url_base = "https://runsignup.com"
    region_url_dict = get_region_paths()

    race_results = {}
    participant_names = set()
    participant_identifiers = []

    # Using `path` param, parse webpage of each region in the race (12 total).
    for region, path in region_url_dict.items():
        url = url_base + path
        soup = get_html(url)

        region_results = {}
        tup = []

        # Scrape webpage for data for every participant in current region.
        for tag in soup.find_all(name="td"):

            # This condition scrapes name (not full), and miles, in that order.
            # Name identifies the participant whose data is upcoming.
            # Miles indicates all data for cur particpant had been scraped.
            # When miles, save dict where participant-> key, miles-> value,
            # and make HTTP request; response returns the following details:
            # full name, gender, age, city, and state. (to be used for NER)

            if tag.a:
                if "miles" in tag.a.text.lower():
                    # Update dict with participant mileage for cur region.
                    miles = float(tag.a.text.lower().split()[0])
                    participant = tup[0]
                    region_results[participant] = miles

                    # Make API request to look-up particpant ID details.
                    # Store tuple of details.
                    if len(tup) == 4:
                        if tup[0] not in participant_names:
                            identifiers = get_identifiers(tag.a['href'])
                            participant_identifiers.append(tuple(identifiers))

                        tup.clear()

                    # Note: Name is scraped prior to miles, however, due to how
                    # ID info is stored, we record it as "seen" here.
                    participant_names.add(participant)

                else:
                    participant = tag.a.text.strip().strip(".")
                    tup.append(participant)

        race_results[region] = region_results

    return participant_names, race_results, participant_identifiers


def get_dataframe():
    names, src_data = get_participant_data()
    names = sorted(list(names))

    data = defaultdict(list)

    data["Team Member"].extend(names)

    # add row of data for each participant in `names`
    # region is key, list of miles logged per region is value
    for name in names:
        for region in range(1,13):
            col = "Region {}".format(str(region))

            if name in src_data[region]:
                data[col].append(src_data[region][name])
            else:
                data[col].append(0)

    df = pd.DataFrame(data)

    # Add column: Total Mileage
    df['Total Mileage'] = df.loc[:].sum(axis=1, numeric_only=True)

    # Sort results by Total Mileage column
    df = df.sort_values(by='Total Mileage', ascending=False)

    # Reset indices
    df = df.reset_index(drop=True)
    df.index += 1
    df.index.name = "Rank"

    # Add row: Miles Per Region
    totals_per_region = ["Miles Per Region"]
    row_values = list(df.sum(axis=0, numeric_only=True))
    totals_per_region.extend(row_values)
    df.loc[len(df.index)+1] = totals_per_region

    # Export excel file
    output_file = r"circumpolar.xlsx"
    df.to_excel(output_file, index=1)


def sort_files_by_region(name: str) -> List[str]:
    # restructure `name` so it resembles the directory name
    name: str = name.lower().replace(" ", "-")

    # import filenames
    path: str = f"participants/{name}/*"
    filenames: list = glob.glob(path)

    part1, part2, part3 = filenames[0].partition("-Region")
    part3 = list(part3.partition("Running_"))
    seen: set  = set()

    # prep filenames to be sorted by region (a number)
    for i, f in enumerate(filenames):
        f = list(f.partition("-Region"))
        f[2] = list(f[2].partition("Running_"))
        region = int(f[2][0])
        f[2][0] = region

        seen.add(region)

        filenames[i] = f

    # Add any missing filenames into the list of filenames
    missing_regions = set(range(1,13)).difference(seen)
    for region in missing_regions:
        new_part3 = [region] + part3[1:]
        new_file = [part1, part2, new_part3]
        filenames.append(new_file)

    # sort by region
    filenames = sorted(filenames, key=lambda x: x[2])

    # convert files back to strs
    sorted_files = []
    for i, f in enumerate(filenames, 1):
        f[2][0] = str(f[2][0])
        f[2] = "".join(f[2])
        f = "".join(f)

        # create a file if there isn't one
        if i not in seen:
            write.write_csv(f)

        sorted_files.append(f)

    return sorted_files


def format_participant_data(participant: str, filenames: List[str]) -> list:
    participant_data = []
    participant_data.append(participant)

    df_objects = [pd.read_csv(f) for f in filenames]

    for df in df_objects:
        miles = round(df['Distance in Miles'].sum(), 2)
        participant_data.append(miles)

    return participant_data


if __name__ == '__main__':
    participants = [
        "Sketch Ditty",
        "David Eckardt",
        "Phil Essam",
        "Joshua Fosberg",
        "Salley Hernandez",
        "James Huller",
        "Connie Karras",
        "Zack Lever",
        "David Ralston",
        "Don Willis",
        "Ashley Blake",
        "Chris Head",
        "Frank Bozanich",
        "Micha Shines",
        "Norm Williams",
        "Shawn Roberts",
        "Steven Kornhaus",
        "Tim Post"
    ]

    # format data
    data = []
    for participant in participants:
        files = sort_files_by_region(participant)
        participant_data = format_participant_data(participant, files)
        data.append(participant_data)

    # create a DF
    columns = [
        " ",
        "Region 1", 
        "Region 2", 
        "Region 3", 
        "Region 4", 
        "Region 5", 
        "Region 6", 
        "Region 7", 
        "Region 8", 
        "Region 9", 
        "Region 10", 
        "Region 11", 
        "Region 12"
    ]

    region_names = [
        " ",
        "Latin America",
        "Andes",
        "Pampas",
        "Antarctica",
        "Down Under",
        "The Islands",
        "SE Asia",
        "Indian Sub",
        "The Stans",
        "Europe",
        "GW North",
        "Lower 48"
    ]

    start_date = [
        " ",
        "Sept, 2020",
        "Oct, 2020",
        "Nov, 2020",
        "Dec, 2020",
        "Jan, 2021",
        "Feb, 2021",
        "Mar, 2021",
        "Apr, 2021",
        "May, 2021",
        "Jun, 2021",
        "Jul, 2021",
        "Aug, 2021"
    ]

    space = [" "] * 13

    header = pd.MultiIndex.from_arrays([
        # top thre rows need to be formatted with "merge and center" in excel
        ["", "2020 CIRCUMPOLAR RACE AROUND THE WORLD"] + [" "]*11, 
        ["", "TEAM \"IN JESPER'S FOOTSTEPS\""] + [" "]*11,
        ["", "30,208 MILES / 48,615 KILOMETERS / 362 DAYS"] + [" "]*11, 
        space, 
        space, 
        start_date, 
        columns, 
        region_names, 
        space, 
        space, 
        space
        ])

    df = pd.DataFrame(data, columns=header)

    # Create rows/cols that contain totals
    df['Total Mileage'] = df.loc[:].sum(axis=1, numeric_only=True)
    row_total = list(df.sum(axis=0, numeric_only=True))
    row_total.insert(0, "Miles Per Region")

    # sorting
    df = df.sort_values(by='Total Mileage', ascending=False)
    df = df.reset_index(drop=True)
    df.index += 1

    df.index.name = "Rank"

    # add row totals
    df.loc[len(df.index)+1] = row_total

    # Export df as an Excel file
    output_file = r"circumpolar-race-results.xlsx"
    df.to_excel(output_file, index=1)

    # Export df as a CSV file
    output_file = r"circumpolar-race-results.csv"
    df.to_csv(output_file, index=1)
