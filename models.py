"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
#import math

class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        #This section creates the framework for the database dictionaries. It standarizes the font and checks for edge cases in each of the fieldnames.
        for key, value in info.items():
            if key.lower() == 'pdes':
                try:
                    self.designation = str(value)
                except ValueError:
                    print(f'The type of this {key} is not a string')
                    
                    
            elif key.lower() == 'name':
                if len(value) != 0:
                    try:
                        self.name = str(value)
                    except ValueError:
                        print(f'The type of this {key} is not a string')
                else:
                    self.name = None
 
            elif key.lower() == 'diameter':
                if len(value) != 0:
                    try:
                        self.diameter = float(value)
                    except ValueError:
                        print(f'The type of {key} is not a float')
                else:
                    self.diameter = float('nan')
                        
                
            elif key.lower() == 'pha':
                try:
                    self.hazardous = str(value)
                    if self.hazardous.lower() == 'y':
                        self.hazardous = True
                    else:
                        self.hazardous = False
                except ValueError:
                    print(f'I\'m afraid that {key} is not a string thing has happened again...')
                        
                        

        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f'The full name of this near earth object is {self.designation} + {self.name}.' 
        else:
            return f'{self.designation}'

    def __str__(self):
        """Return `str(self)`."""
        if not self.diameter:
            return f"A NearEarthObject is called {self.name} and it is {self.hazardous} that it is considered HAZARDOUS to the denizens of the Earth."
    
        return f"A NearEarthObject is called {self.name}, has a diameter of {self.diameter}km, and it is {self.hazardous} that it is considered HAZARDOUS to the denizens of the Earth."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    
    def append(self, approach):
        """Public function appending approaches."""
        if type(approach) == CloseApproach:
            self.approaches.append(approach)
    #added a serialise method as per advice in the Knowledge section
    def serialise(self):
        """Public function linking dictionary with class information.
        
        This enables test_query relevant data.
        """
        return {'designation': self.designation,
                'name': self.name,
                'potentially_hazardous': self.hazardous,
                'diameter_km': self.diameter,
               }

class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # as with the NearEarth object, this section standardises the font, converts to datetime and string/float, and checks for edge cases.
        for key, value in info.items():
            if key.lower() == 'des':
                try:
                    self._designation = str(value)
                except ValueError:
                    print(f'The type of {key} isn\'t a string!')
            
            elif key.lower() == 'cd':
                try:
                    self.time = str(value)
                    self.time = cd_to_datetime(self.time)
                except ValueError:
                    print(f'The type of {key} isn\'t a string!')
        
            elif key.lower() == 'dist':
                try: 
                    self.distance = float(value)
                except ValueError:
                    print(f'The type of {key} is not a float!')
            
            elif key.lower() == 'v_rel':
                try:
                    self.velocity = float(value)
                except ValueError:
                    print(f'Ah, it seems the type of {key} isn\'t a float!')
            
    
        self.neo = self._designation        

    #added a serialise method as per advice in Knowledge section
    
    def serialise(self):
        """Public function linking dictionary with class information.
        
        This enables test_query relevant data.
        """
        return {'datetime_utc': datetime_to_str(self.time),
                'distance_au': self.distance,
                'velocity_km_s': self.velocity,
               }


    @property
    def designation(self):
        """Return a formatted representation of this `CloseApproach`'s approach time."""
        return self._designation

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"A CloseApproach, happening at {self.time_str}, and going by the name of {neo.fullname}, will approach at a distance of {self.distance} au and has the velocity of {self.velocity} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    
