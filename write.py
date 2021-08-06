"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
import string
from helpers import datetime_to_str


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')
    with open(filename, 'w', newline = '') as f:
        # write fieldnames:readings as a dictionary onto the output rows
            writer = csv.DictWriter(f, fieldnames = fieldnames)
        # a formatted row of fieldnames as a header
            writer.writeheader()
            for result in results:
                writer.writerow({**result.serialise(), **result.neo.serialise()})

                
def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    list1 = []
        
    keys = ['datetime_utc', 'distance_au', 'velocity_km_s', 'neo']
        
    for approach in results:
        dict1 = {'datetime_utc': approach.time_str, 'distance_au': approach.distance, 
                 'velocity_km_s': approach.velocity,
                 'neo': {'designation': approach.neo.designation, 'name':approach.neo.name,
                             'diameter_km': approach.neo.diameter, 
                         'potentially_hazardous': approach.neo.hazardous}}
        list1.append(dict1)
                
    with open(filename, 'w') as outfile:
        if results:
            json.dump(list1, outfile, indent=2)
        else:
            json.dump([], outfile)
                        
