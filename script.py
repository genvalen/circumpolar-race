from typing import Dict, Tuple, Set
import pandas as pd
from bs4 import BeautifulSoup
import requests
from collections import defaultdict


def get_bs4_soup(url="https://runsignup.com/RaceGroups" \
        "/95983?groupName=In+Jesper%27s+Footsteps"
    ) -> str:
    """ Make HTTP request and convert HTML response into bs4 soup."""
    resp = requests.get(url).text
    soup = BeautifulSoup(resp, 'lxml')
    return soup


def get_region_paths() -> Dict[int, str]:
    """Return a dictionary that contains region numbers and a path to
    the webpage containing data for that region as a key-value pair.
    """
    soup = get_bs4_soup()
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
    # Prepare headers for HTTP request.
    headers = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept" : "application/json, */*; q=0.01",
        "Accept-Language" : "en-US,en;q=0.5",
        "X-Requested-With" : "XMLHttpRequest",
        "Connection" : "keep-alive",
        "Referer" : "https://runsignup.com/Race/Results/95983/IndividualResult/",
        "Cookie" : "winWidth=1680; _ga=GA1.2.279797247.1629283759; __atuvc=128%7C36%2C6%7C37%2C11%7C38%2C38%7C39%2C4%7C40; cookie_policy_accepted=T; analytics={\"asset\":\"a1ca985c-904e-459a-bfd7-7480afe5b588\",\"source\":1,\"medium\":1}; PHPSESSID=9r2ImrtyrSszLIsWF2YCV3widCfGI9RJ; _mkto_trk=id:350-KBZ-109&token:_mch-runsignup.com-1632559648074-71989; _gid=GA1.2.2082540081.1633160300; __atuvs=615a3572229b618f002"
    }

    # Prepare URL for HTTP request: parse href for query details.
    url_base = "https://runsignup.com/Race/Results/95983/LookupParticipant/"
    result_id, user_id = href.split("=")[1].split("#U")
    payload = {"resultSetId": result_id, "userId": user_id}

    # Make HTTP request.
    resp = requests.get(url_base, params=payload, headers=headers)

    # Convert response to JSON obj and parse relevant output.
    # If error, return empty tuple.
    try:
        resp_dict = resp.json()['participants'][0]
        keys = ['first_name', 'last_name', 'gender', 'age', 'city', 'state']
        data = tuple(resp_dict[k] for k in keys)
    except:
        data = Tuple()

    return data


def get_miles(href: str) -> float:
    """Make HTTP request and, from the response, return the total miles tallied
    for specified participant at the end of the region.
    """
    # Prepare headers for the HTTP request.
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept" : "application/json, */*; q=0.01",
        "Accept-Language" : "en-US,en;q=0.5",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With" : "XMLHttpRequest",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://runsignup.com/Race/Results/95983/IndividualResult/",
    }

    # Prepare URL for HTTP request; parse href for data parameter details.
    url = "https://runsignup.com" + href
    _, user_id = href.split("=")[1].split("#U")

    # Prepare data for HTTP request.
    data = f"userIdCsv={user_id}"

    # Make HTTP request.
    resp = requests.post(url, headers=headers, data=data)

    # Convert response into JSON obj and parse for relevent output.
    # If error, return `None`.
    try:
        miles = resp.json()['results'][0]['result_tally_value']
    except:
        miles = None

    return miles


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
    participant_identifiers = []

    # Save scraped version of particpants' names and map them to full names
    # (eg., Carol G --> Carol Grant).
    # Incomplete names are scraped from website's HTML.
    # Full names are returned by `get_identifiers` in an HTTP request.
    # Saving names ensures HTTP call is made only once per participant
    # while still giving program access to full names as often as needed.

    participants_seen = {}

    # Iterate through designated webpage for each region in the race (12).
    for region, path in region_url_dict.items():
        url = url_base + path
        soup = get_bs4_soup(url)

        region_results = {}

        # Iterate through each particpant in the current region.
        # Scrape name and HREF for each.
        # HREF - used in HTTP call returning participant's data for cur region.
        # Name - used w/ `participants_seen` to prevent over-use of HTTP calls.
        for tag in soup.find_all("a", class_="rsuBtn rsuBtn--text-whitebg rsuBtn--xs margin-r-0"):
            href = tag['href']
            name = tag.text.strip() # incomplete name -> first name/last initial

            if name not in participants_seen:

                # Make HTTP call returning: full name, age, gender, city.
                identifiers = get_identifiers(href)

                # Store identifiers for entity resolution.
                participant_identifiers.append(tuple(identifiers))

                # Update dict of participants seen.
                full_name = " ".join(identifiers[:2]) # full name
                participants_seen[name] = full_name

            # Make HTTP call returning: total miles
            # Update region_results with participant's total miles.
            full_name = participants_seen[name]
            region_results[full_name] = get_miles(href)

        # Update overall race results with results from current region.
        race_results[region] = region_results

    # Create set of full names of participants in the race
    participant_names = set(participants_seen.values())

    return participant_names, race_results, participant_identifiers


def get_dataframe():
    names, src_data, _ = get_participant_data()
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

    print("An Excel spreadsheet has been exported.")


if __name__ == '__main__':
    get_dataframe()
