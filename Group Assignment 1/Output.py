import matplotlib.pyplot as plt
import numpy as np
import group_1_data_generator as DataGenerator

plt.style.use('_mpl-gallery-nogrid')

# Generate some sample values
generator = DataGenerator.DataGenerator(min_value=10, max_value=50)
x = generator.generate_values(5)
labels = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
    
colors = plt.get_cmap('Blues')(np.linspace(0.1, 0.9, len(x)))

#plot
fig, ax= plt.subplots()
ax.pie(
    x,
    labels= labels,
    radius=3,
    center=(4, 4),
    wedgeprops={"linewidth": 1, "edgecolor": "white"}, 
    frame=True
)

ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()