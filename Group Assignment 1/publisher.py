import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
from datetime import datetime
import random
import paho.mqtt.client as mqtt
from group_1_data_generator import DataGenerator

class Publisher:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Publisher")
        self.root.geometry('600x700')
        self.root.configure(bg='#f0f0f0')
        
        self.is_publishing = False
        self.packet_id = 0
        self.client = mqtt.Client()
        self.packets_sent = 0
        self.last_update = time.time()

        # Configure style
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', padding=5)
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), background='#f0f0f0', padding=10)
        style.configure('Status.TLabel', font=('Helvetica', 10), background='#f0f0f0')
        style.configure('Value.TLabel', font=('Helvetica', 12), background='#f0f0f0')
        
        # Create a main container with padding
        main = ttk.Frame(root, padding="10")
        main.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Header with icon
        header_frame = ttk.Frame(main)
        header_frame.grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(header_frame, text="📡 MQTT Publisher", style='Header.TLabel').pack()
        ttk.Label(header_frame, text="Data Generation and Publishing Interface", style='Status.TLabel').pack()

        # Left side - Connection Settings
        left_frame = ttk.Frame(main)
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 5))
        
        # Connection Settings
        conn_frame = ttk.LabelFrame(left_frame, text="Connection Settings", padding="10")
        conn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(conn_frame, text="🌐 Broker Host:").grid(row=0, column=0, sticky=tk.W)
        self.host_entry = ttk.Entry(conn_frame)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)

        ttk.Label(conn_frame, text="🔌 Port:").grid(row=1, column=0, sticky=tk.W)
        self.port_entry = ttk.Entry(conn_frame)
        self.port_entry.insert(0, "1883")
        self.port_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)

        ttk.Label(conn_frame, text="📢 Topic:").grid(row=2, column=0, sticky=tk.W)
        self.topic_entry = ttk.Entry(conn_frame)
        self.topic_entry.insert(0, "iot/data")
        self.topic_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)

        # Data Generation Settings
        data_frame = ttk.LabelFrame(left_frame, text="Data Generation Settings", padding="10")
        data_frame.pack(fill=tk.X)

        ttk.Label(data_frame, text="📊 Base Value:").grid(row=0, column=0, sticky=tk.W)
        self.base_entry = ttk.Entry(data_frame)
        self.base_entry.insert(0, "20.0")
        self.base_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)

        # Right side - Status and Controls
        right_frame = ttk.Frame(main)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N), padx=(5, 0))

        # Status Display
        status_frame = ttk.LabelFrame(right_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))

        self.status_label = ttk.Label(status_frame, text="⚫ Stopped", style='Status.TLabel')
        self.status_label.pack(fill=tk.X)

        self.value_label = ttk.Label(status_frame, text="Last Value: --", style='Value.TLabel')
        self.value_label.pack(fill=tk.X, pady=5)

        self.stats_label = ttk.Label(status_frame, text="📊 Packets: 0 | Rate: 0/s")
        self.stats_label.pack(fill=tk.X)

        # Control Panel
        control_frame = ttk.LabelFrame(right_frame, text="Controls", padding="10")
        control_frame.pack(fill=tk.X)

        self.start_button = ttk.Button(
            control_frame, 
            text="▶ Start Publishing",
            command=self.start_publishing,
            style='TButton'
        )
        self.start_button.pack(fill=tk.X, pady=(0, 5))

        self.stop_button = ttk.Button(
            control_frame,
            text="⏹ Stop Publishing",
            command=self.stop_publishing,
            state="disabled"
        )
        self.stop_button.pack(fill=tk.X)

        # Message Log
        log_frame = ttk.LabelFrame(main, text="Message Log", padding="10")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Text display with scrollbar
        self.log_display = tk.Text(log_frame, height=10, width=50)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_display.yview)
        self.log_display.configure(yscrollcommand=scrollbar.set)
        
        self.log_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.log_display.tag_configure("success", foreground="green")
        self.log_display.tag_configure("error", foreground="red")

        # Configure weights for resizing
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(2, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        # Configure weights for entry fields
        for frame in [conn_frame, data_frame]:
            frame.columnconfigure(1, weight=1)

    def start_publishing(self):
        try:
            # Initialize DataGenerator with GUI parameters
            self.generator = DataGenerator(min_value=float(self.base_entry.get()))
            
            # Connect to broker
            self.client.connect(self.host_entry.get(), int(self.port_entry.get()))
            self.client.loop_start()
            
            self.is_publishing = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text="🟢 Publishing")
            self.packets_sent = 0
            self.last_update = time.time()
            
            self.log_message("Started publishing", "success")
            self.publish_data()
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numeric values for all fields.")
            self.status_label.config(text="🔴 Error - Invalid Input")
            self.log_message("Error: Invalid input values", "error")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start: {e}")
            self.status_label.config(text="🔴 Error")
            self.log_message(f"Error: {str(e)}", "error")

    def stop_publishing(self):
        try:
            self.is_publishing = False
            self.client.loop_stop()
            self.client.disconnect()
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="⚫ Stopped")
            self.log_message("Stopped publishing", "success")
        except Exception as e:
            messagebox.showerror("Error", f"Error while stopping: {e}")
            self.log_message(f"Error while stopping: {str(e)}", "error")

    def publish_data(self):
        if not self.is_publishing:
            return
            
        try:
            self.packet_id += 1
            value = self.generator.generate_values(1)[0]  # Get a single value
            
            packet = {
                "packet_id": self.packet_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "value": value
            }
            
            # Send with 99% probability (1% chance to skip)
            if random.random() >= 0.01:
                payload = json.dumps(packet)
                self.client.publish(self.topic_entry.get(), payload)
                self.value_label.config(text=f"Last Value: {value:.2f}")
                self.log_message(f"Published: Value {value:.2f} (ID: {self.packet_id})", "success")
                self.packets_sent += 1
            else:
                self.value_label.config(text="Last Value: Skipped")
                self.log_message(f"Skipped packet ID: {self.packet_id}", "warning")
            
            # Update statistics every second
            current_time = time.time()
            if current_time - self.last_update >= 1.0:
                rate = self.packets_sent / (current_time - self.last_update)
                self.stats_label.config(text=f"📊 Packets: {self.packets_sent} | Rate: {rate:.1f}/s")
                self.packets_sent = 0
                self.last_update = current_time
            
            # Schedule next publication in 1 second
            self.root.after(1000, self.publish_data)
            
        except Exception as e:
            self.status_label.config(text="🔴 Error")
            self.is_publishing = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.log_message(f"Error: {str(e)}", "error")
            messagebox.showerror("Error", f"Publishing error: {e}")

    def log_message(self, message, tag=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_display.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.log_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = Publisher(root)
    root.mainloop()