from group_1_data_generator import DataGenerator
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk  # For themed widgets
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.style as mpl_style

class SensorApp:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title('Humidity Sensor Monitor - Progress Campus')  # Set application title
        self.root.geometry('1000x800')  # Define window size
        self.root.configure(bg='#f0f0f0')  # Set background color (light gray)
        self.min_value = 13  # Minimum humidity value

        # Configure custom visual style for widgets
        style = ttk.Style()
        style.configure('Premium.TFrame', background='#f0f0f0')

        # Create the main container frame
        self.main_frame = ttk.Frame(root, style='Premium.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header section for the application title
        header_frame = ttk.Frame(self.main_frame, style='Premium.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Display the header text
        ttk.Label(
            header_frame,
            text='Humidity Sensor Data Visualization',
            font=('Helvetica', 24, 'bold'),
            style='Premium.TLabel'
        ).pack()

        # Input section for user controls
        input_frame = ttk.Frame(self.main_frame, style='Premium.TFrame')
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # Container for input controls with organized layout
        controls_frame = ttk.Frame(input_frame, style='Premium.TFrame')
        controls_frame.pack()

        # Frame to display sensor data visualization (graph container)
        self.graph_frame = ttk.Frame(self.main_frame, style='Premium.TFrame')
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        # Initialize graph plotting
        self.graph_values()

    def graph_values(self):
        # Clear any existing graphs from the container
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        try:
            min_value = self.min_value  # Use minimum value defined by user
            
            # Generate synthetic humidity data using a DataGenerator
            generator = DataGenerator(min_value)
            generator.generate_values(20)  # Create 20 data points
            
            # Configure Matplotlib styling and appearance
            mpl_style.use('seaborn-v0_8-darkgrid')  # Use dark grid style for plots
            fig, ax = plt.subplots(figsize=(12, 6))  # Create a graph figure
            fig.patch.set_facecolor('#f0f0f0')  # Match figure background to app theme
            
            # Generate gradient color scheme for the bars
            colors = plt.get_cmap('viridis')(np.linspace(0.2, 0.8, len(generator.values)))
            
            # Plot the data as a bar chart with additional enhancements
            ax.bar(
                range(len(generator.values)), 
                generator.values,
                color=colors,
                width=0.8,
                alpha=0.7  # Slight transparency for aesthetic effect
            )
            
            # Add trend line to visualize data movement
            ax.plot(
                range(len(generator.values)),
                generator.values,
                color='#FF5733',  # Bold orange for the line
                linewidth=3,
                alpha=0.8,
                label='Trend Line'  # Label for the legend
            )

            # Add titles and labels for clarity
            ax.set_title(
                'Humidity Sensor Readings',
                fontsize=16,
                pad=20,
                fontweight='bold'
            )
            ax.set_xlabel(
                'Time Intervals',
                fontsize=12,
                labelpad=10
            )
            ax.set_ylabel(
                'Humidity Level',
                fontsize=12,
                labelpad=10
            )

            # Add a legend and customize grid visibility
            ax.legend(fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.7)  # Dashed grid lines
            
            # Embed the plot within the Tkinter application
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        except ValueError:
            # Display an error message if invalid data is entered
            error_label = ttk.Label(
                self.graph_frame,
                text="Please enter a valid number",
                foreground='red',
                style='Premium.TLabel'
            )
            error_label.pack(pady=20)

if __name__ == "__main__":
    # Start the application loop
    root = tk.Tk()
    app = SensorApp(root)
    root.mainloop()