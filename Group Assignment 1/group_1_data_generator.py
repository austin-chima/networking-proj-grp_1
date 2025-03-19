import math
import random
import matplotlib.pyplot as plt

class DataGenerator:
    def __init__(self):
        """
        Initialize the data generator
        """
        self._frequency = 100  # Base frequency for our generator
        
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
    
    @property
    def random_value(self):
        """
        Public property that returns a frequency value
        Uses y = mx + c where:
        - x is the normalized value (0-1)
        - m is the range (40)
        - c is the minimum value (80)
        This gives us frequencies between 80-120 Hz
        """
        x = self._generate_normalized_value()
        m = 40  # range: 120 - 80 = 40
        c = 80  # minimum value
        return m * x + c

if __name__ == "__main__":
    # Create our generator
    generator = DataGenerator()
    
    # Generate frequency-amplitude pairs
    frequencies = []
    amplitudes = []
    
    # Generate 500 data points as shown in the example
    for _ in range(500):
        freq = generator.random_value
        # Create an amplitude that varies with frequency
        amp = generator._generate_normalized_value()
        frequencies.append(freq)
        amplitudes.append(amp)
    
    # Plot using matplotlib as required
    plt.figure(figsize=(10, 4))
    plt.plot(frequencies, amplitudes, 'g-', linewidth=1)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequency vs Amplitude')
    plt.grid(True, alpha=0.3)
    plt.show()
    
