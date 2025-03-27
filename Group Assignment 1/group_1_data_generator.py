import random
import math

class DataGenerator:
    def __init__(self, min_value):
        """Initialize the data generator with a range of frequencies"""
        self.min_value = min_value
        self.max_value = (min_value + 5)
        self._phase = 0
        self._frequency = random.uniform(0.8, 1.2)
        self._trend = 0.5  # Base trend value
        self._trend_direction = 0.01  # Trend change rate
        self.values = []

    def _generate_normalized_value(self):
        """
        Private method that generates random values in the range 0-1
        Uses multiple components for realistic data generation:
        1. Base trend (slow moving average)
        2. Periodic components (multiple frequencies)
        3. Random walk element
        4. Noise component
        """
        # Update phase for wave components
        self._phase += random.uniform(0.05, 0.15)
        
        # Update trend (random walk with bounds)
        if random.random() < 0.1:  # 10% chance to change trend direction
            self._trend_direction = random.uniform(-0.02, 0.02)
        self._trend += self._trend_direction
        self._trend = max(0.2, min(0.8, self._trend))  # Keep trend within bounds
        
        # Multiple frequency components
        primary_wave = 0.3 * math.sin(self._frequency * self._phase)
        secondary_wave = 0.15 * math.sin(2.5 * self._frequency * self._phase)
        tertiary_wave = 0.1 * math.sin(4 * self._frequency * self._phase)
        
        # Controlled random noise
        short_term_noise = random.gauss(0, 0.05)  # Gaussian noise
        
        # Combine all components
        value = (self._trend +  # Base trend
                primary_wave +   # Main periodicity
                secondary_wave + # Secondary periodicity
                tertiary_wave +  # Higher frequency detail
                short_term_noise)# Random variations
        
        # Normalize to 0-1 range with smooth clipping
        normalized = 1 / (1 + math.exp(-4 * (value - 0.5)))  # Sigmoid function
        
        return normalized

    def generate_values(self, count=1):
        """
        Generate a list of random values within the range
        Ensures smooth transitions between values
        """
        values = []
        prev_value = None
        
        for _ in range(count):
            new_value = self._generate_normalized_value()
            
            # Smooth transitions between values
            if prev_value is not None:
                new_value = 0.7 * new_value + 0.3 * prev_value
            
            # Scale to desired range
            range_value = self.min_value + (self.max_value - self.min_value) * new_value
            values.append(range_value)
            prev_value = new_value
        
        # Update stored values
        self.values.extend(values)
        return values