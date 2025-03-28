from group_1_data_generator import DataGenerator
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.style as mpl_style
import threading
import random

class SensorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Humidity Sensor Monitor - Progress Campus')
        self.root.geometry('1000x800')
        self.root.configure(bg='#f0f0f0')  

        self.data = [random.randint(30, 80) for _ in range(20)]

        # Configure style
        style = ttk.Style()
        style.configure('Premium.TFrame', background='#f0f0f0')
        style.configure('Premium.TLabel', font=('Helvetica', 12), background='#f0f0f0')
        style.configure('Premium.TButton', font=('Helvetica', 11, 'bold'), padding=10)
        style.configure('Premium.TEntry', padding=8)

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

        # Graph container
        self.graph_frame = ttk.Frame(self.main_frame, style='Premium.TFrame')
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        self.start_update_thread()

    def start_update_thread(self):
        thread = threading.Thread(target=self.update_loop)
        thread.daemon = True
        thread.start()

    def update_loop(self):
        while True:
            self.data.pop(0)
            self.data.append(random.randint(30, 80))
            self.root.after(0, self.graph_values)
            threading.Event().wait(0.5)

    def graph_values(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        mpl_style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#f0f0f0')

        colors = plt.get_cmap('viridis')(np.linspace(0.2, 0.8, len(self.data)))

        # Bar chart
        ax.bar(range(len(self.data)),
               self.data,
               color=colors,
               width=0.8,
               alpha=0.7)

        # Line chart
        ax.plot(range(len(self.data)),
                self.data,
                color='#FF5733',
                linewidth=3,
                alpha=0.8,
                label='Trend Line')

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

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SensorApp(root)
    root.mainloop()
