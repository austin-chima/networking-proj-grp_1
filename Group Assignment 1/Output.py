import matplotlib.pyplot as plt
import numpy as np
import group_1_data_generator as DataGenerator

plt.style.use('_mpl-gallery-nogrid')

# Generate some sample values
generator = DataGenerator.DataGenerator(min_value=10, max_value=50)
x = []
flg = 5
counter = 0
labels = ['Category A', 'Category B', 'Category C']

while counter < flg:
    x.append(generator.random_value)
    counter += 1
    
colors = plt.get_cmap('Blues')(np.linspace(0.1, 0.9, len(x)))

#plot
fig, ax= plt.subplots()
ax.pie(
    x,
    colors=colors,
    radius=3,
    center=(4, 4),
    wedgeprops={"linewidth": 1, "edgecolor": "white"},
    frame=True,
    labels=labels  # Add this line to include labels
)

ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()