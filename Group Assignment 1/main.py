import matplotlib.pyplot as plt
import numpy as np
from group_1_data_generator import DataGenerator


plt.style.use('seaborn-v0_8-darkgrid')

generator = DataGenerator(min_value=0)  
x = generator.generate_values(500)  


plt.figure(figsize=(10, 5))
plt.plot(x, color='#1f77b4', linewidth=2, alpha=0.8)  


plt.xlabel("Time (s)", fontsize=14, fontweight='bold')
plt.ylabel("Sensor Value", fontsize=14, fontweight='bold')
plt.title("Humidity Sensor at Progress Campus", fontsize=16, fontweight='bold')


plt.grid(True, linestyle='--', linewidth=0.6, alpha=0.6)


plt.xticks(fontsize=12)
plt.yticks(fontsize=12)


plt.show()
