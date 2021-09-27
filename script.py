from typing import List, Dict, Tuple
import utils.writer as write
import pandas as pd
import glob
from bs4 import BeautifulSoup
import requests


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


def get_participant_data() -> Tuple[str, Dict[int, Dict[str, float]]]:
    """Return a tuple containing a set of participant names (first and last)
    and a dictionary of participants and mileage organized by region.
    """
    url_base = "https://runsignup.com"
    region_url_dict = get_region_paths()

    data = {}
    names = set()

    for region, path in region_url_dict.items():
        url = url_base + path
        soup = get_html(url)
        region_data = {}

        name = ""
        for tag in soup.find_all(name="td"):

            if tag.a:
                if "miles" in tag.a.text.lower():
                    miles = float(tag.a.text.split()[0])
                    region_data[name] = miles
                    names.add(name)
                else:
                    name = tag.a.text.strip().strip('.')

        data[region] = region_data

    return names, data


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
