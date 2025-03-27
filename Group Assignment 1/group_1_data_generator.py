import random
import math

class DataGenerator:
    def __init__(self, min_value):
        """Initialize the data generator with a range of frequencies"""
        self.min_value = min_value
        self.max_value = (min_value + 5)
        self._phase = 0
        self._frequency = random.uniform(0.8, 1.2)
        
        # Add an attribute to store the generated values
        self.values = []

    def _generate_normalized_value(self):
        """Private method that generates random values in the range 0-1"""
        self._phase += random.uniform(0.05, 0.15)
        base_wave = math.sin(self._frequency * self._phase)
        squiggles = 0.2 * math.sin(5 * self._frequency * self._phase)
        extra_randomness = random.uniform(-0.2, 0.2)
        value = base_wave + squiggles + extra_randomness
        normalized = (value + 1) / 2
        return max(0, min(1, normalized))

    def generate_values(self, count=1):
        """Generate a list of random values within the range"""
        values = []
        for _ in range(count):
            x = self._generate_normalized_value()
            range_value = self.min_value + (self.max_value - self.min_value) * x
            values.append(range_value)
        
        # Append generated values to the class attribute
        self.values.extend(values)
        return values