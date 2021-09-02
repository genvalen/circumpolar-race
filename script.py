from typing import List
import utils.writer as write
import pandas as pd
import glob


def sort_files_by_region(name: str) -> List[str]:
    # restructure `name` so it resembles the directory name
    name: str = name.lower().replace(" ", "-")

    # import filenames
    path: str = f"participants/{name}/*"
    filenames: list = glob.glob(path)
    print(participant)
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


if __name__ == "__main__":
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
        "Don Willis"
    ]

    # format data
    data = []
    for participant in participants:
        files = sort_files_by_region(participant)
        participant_data = format_participant_data(participant, files)
        data.append(participant_data)

    # create a DF
    columns = [
        "Team Member",
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

    df = pd.DataFrame(data, columns=columns)
    df["Total"] = df.loc[:].sum(axis=1, numeric_only=True)

    # Export df as an Excel file
    output_file = r"circumpolar-race-results.xlsx"
    df.to_excel(output_file, index = False)

    # Export df as a CSV file
    output_file = r"circumpolar-race-results.csv"
    df.to_csv(output_file, index = False)
