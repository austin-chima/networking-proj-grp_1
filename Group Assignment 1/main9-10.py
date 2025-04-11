from group_1_data_generator import DataGenerator
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk  # For themed widgets
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.style as mpl_style

class SensorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Humidity Sensor Monitor - Progress Campus')
        self.root.geometry('1000x800')
        self.root.configure(bg='#f0f0f0')  # Light gray background
        self.min_value = 13
        
        # Configure style
        style = ttk.Style()
        style.configure('Premium.TFrame', background='#f0f0f0')
        style.configure('Premium.TLabel', 
                       font=('Helvetica', 12),
                       background='#f0f0f0')
        style.configure('Premium.TButton',
                       font=('Helvetica', 11, 'bold'),
                       padding=10)
        style.configure('Premium.TEntry',
                       padding=8)
        
        # Main container
        self.main_frame = ttk.Frame(root, style='Premium.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(self.main_frame, style='Premium.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame,
                 text='Humidity Sensor Data Visualization',
                 font=('Helvetica', 24, 'bold'),
                 style='Premium.TLabel').pack()
        
        # Input section
        input_frame = ttk.Frame(self.main_frame, style='Premium.TFrame')
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Input controls with better layout
        controls_frame = ttk.Frame(input_frame, style='Premium.TFrame')
        controls_frame.pack()
        
        # Graph container
        self.graph_frame = ttk.Frame(self.main_frame, style='Premium.TFrame')
        self.graph_frame.pack(fill=tk.BOTH, expand=True)        
        
        self.graph_values()
        
    def graph_values(self):
        # Clear previous graph if it exists
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        try:
            min_value = self.min_value
            
            # Generate data
            generator = DataGenerator(min_value)
            generator.generate_values(20)
            
            # Create figure with premium styling
            mpl_style.use('seaborn-v0_8-darkgrid')
            fig, ax = plt.subplots(figsize=(12, 6))
            fig.patch.set_facecolor('#f0f0f0')
            
            # Create gradient colors
            colors = plt.get_cmap('viridis')(np.linspace(0.2, 0.8, len(generator.values)))
            
            # Plot data with enhanced styling
            ax.bar(range(len(generator.values)), 
                  generator.values,
                  color=colors,
                  width=0.8,
                  alpha=0.7)
            
            ax.plot(range(len(generator.values)),
                   generator.values,
                   color='#FF5733',
                   linewidth=3,
                   alpha=0.8,
                   label='Trend Line')
            
            # Enhance graph appearance
            ax.set_title('Humidity Sensor Readings',
                        fontsize=16,
                        pad=20,
                        fontweight='bold')
            ax.set_xlabel('Time Intervals',
                         fontsize=12,
                         labelpad=10)
            ax.set_ylabel('Humidity Level',
                         fontsize=12,
                         labelpad=10)
            
            ax.legend(fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Embed plot in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except ValueError:
            error_label = ttk.Label(self.graph_frame,
                                  text="Please enter a valid number",
                                  foreground='red',
                                  style='Premium.TLabel')
            error_label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = SensorApp(root)
    root.mainloop()