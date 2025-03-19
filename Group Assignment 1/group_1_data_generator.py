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
        Combines:
        - Sine wave for peaks and valleys (generator_1)
        - Frequency control (generator_3)
        - Added squiggles (generator_2)
        """
        # Update phase for continuous wave
        self._phase += 0.1
        
        # Base sine wave with controlled frequency
        base_wave = math.sin(self._frequency * self._phase)
        
        # Add higher frequency component for squiggles
        squiggles = 0.2 * math.sin(5 * self._frequency * self._phase)
        
        # Add some random noise
        noise = random.uniform(-0.1, 0.1)
        
        # Combine all components
        value = base_wave + squiggles + noise
        
        # Normalize to 0-1 range
        normalized = (value + 1) / 2
        
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