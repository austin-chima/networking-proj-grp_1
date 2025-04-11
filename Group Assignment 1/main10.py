from group_1_data_generator import DataGenerator
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.style as mpl_style
import time
import threading

class SensorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Humidity Sensor Monitor - Progress Campus')
        self.root.geometry('1000x800')
        self.root.configure(bg='#f0f0f0')
        
        # Create data generator using proper class instead of random values
        self.generator = DataGenerator(min_value=30)
        self.data = self.generator.generate_values(20)
        
        # Flag to control update thread
        self.running = True
        self.connected = False
        
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
        
        # Control panel
        control_frame = ttk.Frame(self.main_frame, style='Premium.TFrame')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Connection controls
        self.connect_btn = ttk.Button(control_frame, text="Connect", 
                                    command=self.connect, style='Premium.TButton')
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_btn = ttk.Button(control_frame, text="Disconnect", 
                                       command=self.disconnect, style='Premium.TButton')
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)
        self.disconnect_btn.config(state='disabled')
        
        self.update_btn = ttk.Button(control_frame, text="Pause Updates", 
                                    command=self.toggle_updates, style='Premium.TButton')
        self.update_btn.pack(side=tk.LEFT, padx=5)
        self.update_btn.config(state='disabled')
        
        self.status_label = ttk.Label(control_frame, text="Status: Disconnected", 
                                     style='Premium.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        self.stats_label = ttk.Label(control_frame, text="", style='Premium.TLabel')
        self.stats_label.pack(side=tk.RIGHT, padx=5)

        # Graph container
        self.graph_frame = ttk.Frame(self.main_frame, style='Premium.TFrame')
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initial graph
        self.graph_values()

    def connect(self):
        try:
            self.connected = True
            self.connect_btn.config(state='disabled')
            self.disconnect_btn.config(state='normal')
            self.update_btn.config(state='normal')
            self.status_label.config(text="Status: Connected")
            self.start_update_thread()
        except Exception as e:
            self.status_label.config(text=f"Status: Connection Error - {str(e)}")
            self.connected = False

    def disconnect(self):
        self.connected = False
        self.running = False
        self.connect_btn.config(state='normal')
        self.disconnect_btn.config(state='disabled')
        self.update_btn.config(state='disabled')
        self.status_label.config(text="Status: Disconnected")

    def toggle_updates(self):
        self.running = not self.running
        if self.running:
            self.update_btn.config(text="Pause Updates")
            self.status_label.config(text="Status: Connected - Running")
        else:
            self.update_btn.config(text="Resume Updates")
            self.status_label.config(text="Status: Connected - Paused")

    def on_closing(self):
        self.running = False
        self.connected = False
        self.root.destroy()

    def start_update_thread(self):
        thread = threading.Thread(target=self.update_loop)
        thread.daemon = True
        thread.start()

    def update_loop(self):
        while self.connected:
            if self.running:
                try:
                    # Get new data point using the generator
                    new_value = self.generator.generate_values(1)[0]
                    
                    # Update data list - remove oldest, add newest
                    if len(self.data) >= 20:
                        self.data.pop(0)
                    self.data.append(new_value)
                    
                    # Schedule graph update on main thread
                    self.root.after(0, self.graph_values)
                except Exception as e:
                    print(f"Error in update loop: {e}")
            
            # Sleep for 500ms
            time.sleep(0.5)

    def graph_values(self):
        try:
            # Clear current graph
            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            # Update statistics
            avg = sum(self.data) / len(self.data)
            min_val = min(self.data)
            max_val = max(self.data)
            self.stats_label.config(text=f"Avg: {avg:.1f} | Min: {min_val:.1f} | Max: {max_val:.1f}")

            # Create new graph
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
                    marker='o',
                    markersize=4,
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

            # Display graph
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except Exception as e:
            error_label = ttk.Label(self.graph_frame, 
                                   text=f"Error creating graph: {e}", 
                                   foreground='red', 
                                   style='Premium.TLabel')
            error_label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = SensorApp(root)
    root.mainloop()
