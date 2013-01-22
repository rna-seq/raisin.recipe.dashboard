import csv
import itertools
from raisin.recipe.dashboard import Dashboard

MEASURE = None


class Coordinates:

    def __init__(self):
        self.coordinates = []

    def __iter__(self):
        for item in self.coordinates:
            yield item

    def __len__(self):
        return len(self.coordinates)

    def set(self, coordinates):
        self.coordinates = coordinates

    def get(self):
        return self.coordinates

    def append(self, coordinate):
        self.coordinates.append(coordinate)


class Cube:
    """
    A nested data cube (NDC).
    """

    def __init__(self):
        self.attributes = []
        self.coordinates = None
        self.sub_cube = None
        self.bag = None
        self.agg = None

    def initialize(self, coordinates, attributes):
        """
        Feed the coordinates into the cube
        """
        self.coordinates = Coordinates()
        self.coordinates.set(coordinates)
        self.attributes = attributes

    def duplicate(self, attribute, coercion=float):
        """
        Duplicate an attribute to become the measure.
        """
        cube = Cube()
        cube.attributes = self.attributes[:]
        cube.coordinates = self.coordinates
        coordinates = cube.coordinates.get()
        coordinates[MEASURE] = coordinates[attribute].apply(coercion)
        return cube

    def extend(self, existing_attribute, attribute, rollup=lambda x: x):
        """
        Add an attribute to the coordinate type.
        """
        cube = Cube()
        if attribute in self.attributes:
            raise AttributeError("Already contains that attribute")
        cube.attributes = self.attributes[:]
        cube.attributes.append(attribute)
        cube.coordinates = self.coordinates
        coordinates = self.coordinates.get()
        coordinates[attribute] = coordinates[existing_attribute].apply(rollup)
        return cube

    def nest(self, attribute):
        """
        Nest the attribute
        """
        if not attribute in self.attributes:
            if self.sub_cube is None:
                raise AttributeError("Attribute not found: %s" % attribute)
            # Look for the right level to nest in
            self.sub_cube = self.sub_cube.nest(attribute)
            # Having changed the sub cube in place still return the top one
            return self
        sub_cube = Cube()
        # The attributes of the sub cube don't have the attribute any more
        sub_cube.attributes = [a for a in self.attributes if a != attribute]
        # Copy over the coordinates to the sub_cube
        sub_cube.coordinates = self.coordinates
        # Put the sub cube into the current cube
        self.sub_cube = sub_cube
        # The only attribute of the cube is added
        self.attributes = [attribute]
        return self

    def select(self, attribute, value):
        """
        Decrease the number of tuples by keeping only those where the attribute
        matches the value
        """
        coordinates = self.coordinates.get()
        coordinates = coordinates[coordinates[attribute] == value]
        self.coordinates.set(coordinates)
        return self

    def unnest(self):
        """
        Unnest the cube by joining the top coordinate types
        """
        self.sub_cube.attributes = self.attributes + self.sub_cube.attributes
        return self.sub_cube

    def bagify(self, attributes=[]):
        """
        Collapse data on lowest level into bags.
        """
        attributes = attributes + self.attributes
        coordinates = self.coordinates.get()
        # XXX 
        # Would have to remove attributes not needed
        # For the moment keeping them all
        self.bag = coordinates.reset_index().set_index(attributes)
        if not self.sub_cube is None:
            self.sub_cube.bagify(attributes)
        return self

    def aggregate(self, function, attributes=[]):
        """
        Aggregate over the cube bags using the function
        """
        attributes = attributes + self.attributes
        coordinates = self.coordinates.get()
        self.agg = coordinates.groupby(attributes).agg(function)
        if not self.sub_cube is None:
            self.sub_cube.bagify(attributes)
        return self




