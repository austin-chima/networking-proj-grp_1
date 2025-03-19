import random
import math

class DataGenerator:
    def __init__(self):
        """
        Initialize the data generator with your preferred range
        """
        self._min = 80  # Minimum frequency (Hz)
        self._max = 120  # Maximum frequency (Hz)
        self._frequency = 1.0  # Base frequency for peaks
        self._phase = 0.0  # Current phase of the wave
        
    def _generate_normalized_value(self) -> float:
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
        
        # Ensure we stay within [0, 1] range
        return max(0, min(1, normalized))
    
    @property
    def random_value(self) -> float:
        """
        Public property that returns a value in your preferred range
        Uses the formula y = mx + c where:
        y is the intended output
        m is the range (max - min)
        x is the normalized value from _generate_normalized_value
        c is the minimum value
        """
        x = self._generate_normalized_value()
        m = self._max - self._min  # Range of values
        c = self._min  # Minimum value
        return m * x + c

if __name__ == "__main__":
    # Create an instance of our generator
    generator = DataGenerator()
    
    # Test by generating a few values
    print("Sample generated values:")
    for _ in range(5):
        value = generator.random_value
        print(f"{value:.2f} Hz")

def generator_1() -> float:
    """
    This generator creates a pattern using sine waves
    It returns values that create peaks and valleys
    """
    t = random.uniform(0, 2 * math.pi)
    value = math.sin(3 * t)  # Higher frequency base wave
    # Normalize to 0-1 range
    return (value + 1) / 2

def generator_2() -> float:
    """
    This generator adds variation to the pattern
    It combines multiple frequencies for more natural peaks
    """
    t = random.uniform(0, 2 * math.pi)
    value = (
        0.5 * math.sin(2 * t) +          # Lower frequency component
        0.3 * math.sin(5 * t) +          # Medium frequency component
        0.2 * math.sin(8 * t)            # Higher frequency component
    )
    # Normalize to 0-1 range
    return (value + 1) / 2

def generator_3() -> float:
    """
    This generator adds random noise to create squiggles
    It uses random variation for natural randomness
    """
    base = generator_2()
    noise = random.uniform(-0.15, 0.15)  # Increased noise range
    value = base + noise
    # Ensure value stays in 0-1 range
    return max(0, min(1, value))

# Store the base value and change amount
_base = {'value': 0.5}
_delta = {'value': 0.08}  # Increased step size

def generator_4(increment: bool = True) -> float:
    """
    This generator creates a pattern that goes up and down
    Similar to the pattern values example in the sample code
    """
    if increment:
        _base['value'] += _delta['value']
        if _base['value'] > 1:
            _base['value'] = 1
            return generator_3()
    else:
        _base['value'] -= _delta['value']
        if _base['value'] < 0:
            _base['value'] = 0
            return generator_3()
    return _base['value']

if __name__ == "__main__":
    # Test individual values first
    print("Testing different generators:")
    for i in range(5):
        val = generator_4(increment=i % 2 == 0)
        # Scale to frequency range (80-120 Hz)
        freq = 80 + (val * 40)
        print(f"Value {i+1}: {freq:.2f} Hz")
    
    # Generate sequence of values
    number_of_values = 200  # Same as sample code
    
    # Generate x and y values using generator_4
    x = []
    y = []
    for i in range(number_of_values):
        # Alternate between incrementing and decrementing
        val = generator_4(increment=i % 2 == 0)
        # Scale to our frequency range (80-120 Hz)
        freq = 80 + (val * 40)
        x.append(i)  # Time/sequence number
        y.append(freq)  # Frequency value
    
    # Print some statistics about the generated data
    print("\nData Statistics:")
    print(f"Number of points: {len(x)}")
    print(f"Frequency range: {min(y):.2f} Hz to {max(y):.2f} Hz")
    
