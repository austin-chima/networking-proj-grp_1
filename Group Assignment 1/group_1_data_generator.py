import math
import random
import matplotlib.pyplot as plt

import random
import math

class DataGenerator:
    def __init__(self, min_value=80, max_value=120):
        """
        Initialize the data generator with a range of frequencies
        """
        self.min_value = min_value  # Minimum frequency value
        self.max_value = max_value  # Maximum frequency value

    def _generate_normalized_value(self):
        """
        Private method that generates random values in the range 0-1
        Uses a combination of sine waves to create peaks and valleys
        """
        # Get current time as a basis for our wave
        t = random.uniform(0, 2 * math.pi)
        
        # Create a wave pattern with multiple frequencies
        value = (
            0.4 * math.sin(t) +                  # Base wave
            0.2 * math.sin(2.5 * t) +            # Higher frequency component
            0.1 * random.uniform(-1, 1)          # Random variation
        )
        
        # Normalize to 0-1 range
        value = (value + 1) / 2
        
        # Ensure we stay within bounds
        return max(0, min(1, value))

    def generate_values(self, count=1):
        """
        Generate a list of random values within the range
        """
        values = []
        for _ in range(count):
            x = self._generate_normalized_value()  # Generate normalized value (0-1)
            range_value = self.min_value + (self.max_value - self.min_value) * x
            values.append(range_value)
        return values