"""A utility that creates files for regions that are missing
from a participant's directory."""

from typing import List

def write_csv(
    output_file: str, 
    header: List[str] = [
        "Activity Date", 
        "Distance in Miles", 
        "Activity Type",
        "Comment"
        ]
    ) -> None:

    """Export a CSV file with the given file name.
    The program will write a header and a row of zeros
    to the file.
    """
    import csv

    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow ([0,0,0,0])

    return None