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

    # Style and create the pie chart
    plt.style.use('_mpl-gallery-nogrid')
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, 20))
    fig, ax = plt.subplots()
    ax.pie(generator.values, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

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