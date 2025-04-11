import math
import random


class DataGenerator:
    def __init__(
        self, amplitude=5.0, period=60.0, phase=0.0, baseline=20.0, noise_std=1.0
    ):
        """Initialize the data generator with parameters for a sine wave plus noise."""
        self.amplitude = amplitude  # Amplitude of the sine wave
        self.omega = 2 * math.pi / period  # Angular frequency (period in seconds)
        self.phase = phase  # Phase shift
        self.baseline = baseline  # Baseline value
        self.noise_std = noise_std  # Standard deviation of Gaussian noise
        self.t = 0  # Time step counter

    def next_value(self):
        """Generate the next value based on a sine wave with added noise."""
        value = (
            self.amplitude * math.sin(self.omega * self.t + self.phase)
            + self.baseline
            + random.gauss(0, self.noise_std)
        )
        self.t += 1
        return value
