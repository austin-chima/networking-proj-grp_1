import tkinter as tk
from tkinter import messagebox
import json
import paho.mqtt.client as mqtt
from queue import Queue
import threading

class Subscriber:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Subscriber")
        self.client = mqtt.Client()
        self.message_queue = Queue()
        self.expected_id = None
        self.received_count = 0
        self.missing_count = 0
        self.erroneous_count = 0
        self.min_value = 0.0  # Hardcoded thresholds
        self.max_value = 40.0

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

        self.connect_button = tk.Button(root, text="Connect", command=self.connect)
        self.connect_button.grid(row=3, column=0, columnspan=2)

        self.text_display = tk.Text(root, height=10, width=50)
        self.text_display.grid(row=4, column=0, columnspan=2)
        self.text_display.tag_config("error", foreground="red")

        self.stats_label = tk.Label(root, text="Received: 0, Missing: 0, Erroneous: 0")
        self.stats_label.grid(row=5, column=0, columnspan=2)

        # MQTT Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        try:
            self.client.connect(self.host_entry.get(), int(self.port_entry.get()))
            self.client.loop_start()
            self.connect_button.config(state="disabled")
            self.root.after(100, self.process_queue)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.client.subscribe(self.topic_entry.get())
        else:
            messagebox.showerror("Error", "Connection failed")

    def on_message(self, client, userdata, msg):
        self.message_queue.put(msg.payload.decode())

    def process_queue(self):
        while not self.message_queue.empty():
            payload = self.message_queue.get()
            packet = json.loads(payload)
            packet_id = packet["packet_id"]
            value = packet["value"]
            timestamp = packet["timestamp"]

            # Initialize expected_id with first packet
            if self.expected_id is None:
                self.expected_id = packet_id + 1
                self.received_count += 1
                self.display_packet(packet_id, timestamp, value)
            else:
                # Check for missing packets
                if packet_id > self.expected_id:
                    missing_ids = range(self.expected_id, packet_id)
                    self.missing_count += len(missing_ids)
                    self.text_display.insert(tk.END, f"Missing packets: IDs {self.expected_id} to {packet_id - 1}\n")
                self.expected_id = packet_id + 1
                self.received_count += 1
                self.display_packet(packet_id, timestamp, value)

            self.update_stats()
        self.root.after(100, self.process_queue)

    def display_packet(self, packet_id, timestamp, value):
        if value < self.min_value or value > self.max_value:
            self.erroneous_count += 1
            self.text_display.insert(tk.END, f"Erroneous: ID {packet_id}, Time {timestamp}, Value {value}\n", "error")
        else:
            self.text_display.insert(tk.END, f"Received: ID {packet_id}, Time {timestamp}, Value {value:.2f}\n")
        self.text_display.see(tk.END)

    def update_stats(self):
        self.stats_label.config(text=f"Received: {self.received_count}, Missing: {self.missing_count}, Erroneous: {self.erroneous_count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Subscriber(root)
    root.mainloop()