from group_1_data_generator import DataGenerator
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # For embedding the plot

def graph_values():
    # Get the minimum value from the Entry widget
    min_value = int(txtmin.get())
    
    # Generate data using the DataGenerator class
    generator = DataGenerator(min_value)
    generator.generate_values(20)

    # Style and create the graphs
    plt.style.use('_mpl-gallery-nogrid')
    colors = plt.get_cmap('Greens')(np.linspace(0.2, 0.7, len(generator.values)))
    fig, ax = plt.subplots(figsize=(19, 9.5))

    # Create bar graph
    ax.bar(range(len(generator.values)), generator.values, color=colors, width=0.8, label='Temperature changes over time')
    ax.plot(range(len(generator.values)), generator.values, color='red', linewidth=2, alpha=0.8)
    ax.legend()

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=m)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()

# Create the Tkinter application
m = tk.Tk()
m.title('Humidity Sensor at Progress Campus')

# Add widgets for user input
lblmin = tk.Label(m, text='Minimum Value')
txtmin = tk.Entry(m)
lblmin.pack()
txtmin.pack()

# Add Start button to generate the graph
btnstart = tk.Button(m, text='Start', width=25, command=graph_values)
btnstart.pack()

# Run the Tkinter main loop
m.mainloop()