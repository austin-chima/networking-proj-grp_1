import numpy as np

class DataGenerator:
    def __init__(self, min_value=0, max_value=1):
        """
        Initialize the data generator with a range for scaling
        min_value: minimum value for the output range
        max_value: maximum value for the output range
        """
        self._min_value = min_value
        self._max_value = max_value
        
    def _generate_normalized_value(self):
        """
        Private method to generate a normalized random value between 0 and 1
        using a combination of sine waves and noise for natural variation
        """
        # Generate base signal using time
        t = np.random.uniform(0, 2 * np.pi)
        
        # Combine multiple frequencies with different weights
        value = (
            0.4 * np.sin(t) +                    # Primary wave
            0.2 * np.sin(2.5 * t) +              # Higher frequency component
            0.1 * np.random.normal(0, 1)         # Random noise
        )
        
        # Normalize to 0-1 range
        value = (value + 1) / 2  # First shift from [-1,1] to [0,2], then scale to [0,1]
        
        # Ensure value stays within bounds
        return np.clip(value, 0, 1)
    
    @property
    def random_value(self):
        """
        Public property that returns a scaled random value in the desired range
        Uses the formula y = mx + c where:
        m = (max_value - min_value)
        c = min_value
        x = normalized value between 0 and 1
        """
        normalized_value = self._generate_normalized_value()
        
        # Scale to desired range using y = mx + c
        m = self._max_value - self._min_value
        c = self._min_value
        scaled_value = m * normalized_value + c
        
        return scaled_value

# Test the generator
if __name__ == "__main__":
    # Create generator with custom range (e.g., for frequency 80-120 Hz)
    generator = DataGenerator(min_value=80, max_value=120)

    # Generate some sample values
    print("Sample generated values:")
    for _ in range(5):
        value = generator.random_value
        print(f"{value:.2f}")
    
