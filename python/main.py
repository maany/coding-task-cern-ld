"""
Entry point of the program.
Do not edit this file.
"""

from area_algorithm import visible_area
from data_fetch import fetch
from landscape import Landscape

URL = "https://cern.ch/sy-epc-ccs-coding-challenge/landscape"
FALLBACK_FILE = "./doc/example_data_set.txt"

# fetch data from server or fallback_file
data = fetch(URL, FALLBACK_FILE)

# parse landscape data into landscape entity objects
landscape = Landscape()
landscape.load(data)
print(landscape)

# prepare mountain dict format based on parsed entities
mountains = [
    {"left": entity.left, "right": entity.right, "height": entity.height}
    for entity in landscape
    if entity.is_mountain
]

# Part 2: calculate and print area
print(visible_area(mountains))
