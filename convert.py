"""
Converts Via JSON to a CSV file.
"""

import csv
import json
import argparse


def read_json(filepath):
    """Reads a JSON file and returns a dictionary.

    Parameters
    ----------
    filepath : str
        The path to the JSON file.

    Returns
    -------
    dict
        The JSON file as a dictionary.
    """
    with open(filepath, 'r', encoding="utf8") as f:
        return json.load(f)


def write_csv(filepath, data):
    """Writes a CSV file.

    Parameters
    ----------
    filepath : str
        The path to the CSV file.
    data : list
        The data to write to the CSV file.
    """
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def convert_json_to_csv(json_filepath, csv_filepath):
    """Converts a JSON file to a CSV file.

    Parameters
    ----------
    json_filepath : str
        The path to the JSON file.
    csv_filepath : str
        The path to the CSV file.
    """
    metadata_path = "_via_img_metadata"
    data = read_json(json_filepath)

    headers = ["file", "title", "google", "identifiable_yes", "identifiable_no",
               "identifiable_withdetectivework", "diversity_none", "diversity_bipoc",
               "diversity_woman", "diversity_lgbt", "diversity_nonchristian",
               "diversity_disability", "diversity_other", "diversity_ambiguous"]
    csv_data = [headers]
    for book_id in data[metadata_path]:
        obj = data[metadata_path][book_id]

        filename = obj["filename"] if "filename" in obj else ""
        title = obj["file_attributes"]["title"] if "title" in obj["file_attributes"] else ""
        google = obj["file_attributes"]["google"] if "google" in obj["file_attributes"] else ""

        identifiable = obj["file_attributes"]["identifiable"] if "identifiable" in obj["file_attributes"] else ""
        identifiable_yes = int(identifiable == "yes")
        identifiable_no = int(identifiable == "no")
        identifiable_withdetectivework = int(identifiable == "with detective work")

        diversity = obj["file_attributes"]["diversity"] if "diversity" in obj["file_attributes"] else {}
        diversity_name = int("none" in diversity)
        diversity_bipoc = int("bipoc" in diversity)
        diversity_woman = int("woman" in diversity)
        diversity_lgbt = int("lgbt" in diversity)
        diversity_nonchristian = int("nonchristian" in diversity)
        diversity_disability = int("disability" in diversity)
        diversity_other = int("other" in diversity)
        diversity_ambiguous = int("ambiguous" in diversity)

        row = [filename, title, google, identifiable_yes, identifiable_no,
               identifiable_withdetectivework, diversity_name, diversity_bipoc,
               diversity_woman, diversity_lgbt, diversity_nonchristian, diversity_disability,
               diversity_other, diversity_ambiguous]
        csv_data.append(row)

    with open(csv_filepath, 'w+', encoding="utf8", newline="") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(csv_data)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Converts Via JSON to a CSV file.')
    parser.add_argument('json_filepath', help='The path to the JSON file.')
    parser.add_argument('csv_filepath', help='The path to the CSV file.')
    args = parser.parse_args()

    convert_json_to_csv(args.json_filepath, args.csv_filepath)


if __name__ == '__main__':
    # main()
    json_path = "./data/Michelle.json"
    export_path = "./converted/test.csv"
    print("Converting {} to {}".format(json_path, export_path))
    convert_json_to_csv(json_path, export_path)
