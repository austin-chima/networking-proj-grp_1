
from group_1_data_generator import DataGenerator

# Get minimum value from the user
min_value = float(input("Enter the minimum value: "))

# Initialize the generator with the given min_value
generator = DataGenerator(min_value)

# Collect exactly 20 random values
values = []
for _ in range(20):  # Loop 20 times to get 20 individual values
    single_value = generator.generate_values(1)[0]  # Generate 1 value and extract it
    values.append(single_value)

print(values)