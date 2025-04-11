import tkinter as tk
from tkinter import messagebox
import json
import time
from datetime import datetime
import random
import paho.mqtt.client as mqtt
from data_generator import DataGenerator

class Publisher:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Publisher")
        self.is_publishing = False
        self.packet_id = 0
        self.client = mqtt.Client()

        # GUI Components
        tk.Label(root, text="Broker Host:").grid(row=0, column=0)
        self.host_entry = tk.Entry(root)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1)

        tk.Label(root, text="Broker Port:").grid(row=1, column=0)
        self.port_entry = tk.Entry(root)
        self.port_entry.insert(0, "1883")
        self.port_entry.grid(row=1, column=1)

        tk.Label(root, text="Topic:").grid(row=2, column=0)
        self.topic_entry = tk.Entry(root)
        self.topic_entry.insert(0, "iot/data")
        self.topic_entry.grid(row=2, column=1)

        tk.Label(root, text="Amplitude:").grid(row=3, column=0)
        self.amp_entry = tk.Entry(root)
        self.amp_entry.insert(0, "5.0")
        self.amp_entry.grid(row=3, column=1)

        tk.Label(root, text="Period (s):").grid(row=4, column=0)
        self.period_entry = tk.Entry(root)
        self.period_entry.insert(0, "60.0")
        self.period_entry.grid(row=4, column=1)

        tk.Label(root, text="Baseline:").grid(row=5, column=0)
        self.base_entry = tk.Entry(root)
        self.base_entry.insert(0, "20.0")
        self.base_entry.grid(row=5, column=1)

        tk.Label(root, text="Noise Std:").grid(row=6, column=0)
        self.noise_entry = tk.Entry(root)
        self.noise_entry.insert(0, "1.0")
        self.noise_entry.grid(row=6, column=1)

        self.start_button = tk.Button(root, text="Start", command=self.start_publishing)
        self.start_button.grid(row=7, column=0)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_publishing, state="disabled")
        self.stop_button.grid(row=7, column=1)

        self.status_label = tk.Label(root, text="Status: Stopped")
        self.status_label.grid(row=8, column=0, columnspan=2)
        self.value_label = tk.Label(root, text="Last Value: None")
        self.value_label.grid(row=9, column=0, columnspan=2)

    def start_publishing(self):
        try:
            # Initialize DataGenerator with GUI parameters
            self.generator = DataGenerator(
                amplitude=float(self.amp_entry.get()),
                period=float(self.period_entry.get()),
                phase=0.0,
                baseline=float(self.base_entry.get()),
                noise_std=float(self.noise_entry.get())
            )
            # Connect to broker
            self.client.connect(self.host_entry.get(), int(self.port_entry.get()))
            self.client.loop_start()
            self.is_publishing = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text="Status: Publishing")
            self.publish_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start: {e}")

    def stop_publishing(self):
        self.is_publishing = False
        self.client.loop_stop()
        self.client.disconnect()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Status: Stopped")

    def publish_data(self):
        if not self.is_publishing:
            return
        self.packet_id += 1
        value = self.generator.next_value()
        packet = {
            "packet_id": self.packet_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "value": value
        }
        # Send with 99% probability (1% chance to skip)
        if random.random() >= 0.01:
            payload = json.dumps(packet)
            self.client.publish(self.topic_entry.get(), payload)
            self.value_label.config(text=f"Last Value: {value:.2f} (ID: {self.packet_id})")
        else:
            self.value_label.config(text=f"Last Value: Skipped (ID: {self.packet_id})")
        # Schedule next publication in 1 second
        self.root.after(1000, self.publish_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = Publisher(root)
    root.mainloop()