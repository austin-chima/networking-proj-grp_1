import tkinter as tk
from tkinter import ttk, messagebox
import json
import paho.mqtt.client as mqtt
from queue import Queue
import threading

class Subscriber:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Subscriber")
        self.root.geometry('600x700')
        self.root.configure(bg='#f0f0f0')
        
        self.client = mqtt.Client()
        self.message_queue = Queue()
        self.expected_id = None
        self.received_count = 0
        self.missing_count = 0
        self.erroneous_count = 0
        self.min_value = 0.0
        self.max_value = 40.0

        # Configure style
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', padding=5)
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), background='#f0f0f0', padding=10)

        # Main container with padding
        main = ttk.Frame(root, padding="10")
        main.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Header
        ttk.Label(main, text="MQTT Subscriber", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=10)

        # Connection Settings
        conn_frame = ttk.LabelFrame(main, text="Connection Settings", padding="5")
        conn_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(conn_frame, text="Broker Host:").grid(row=0, column=0, sticky=tk.W)
        self.host_entry = ttk.Entry(conn_frame)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(conn_frame, text="Broker Port:").grid(row=1, column=0, sticky=tk.W)
        self.port_entry = ttk.Entry(conn_frame)
        self.port_entry.insert(0, "1883")
        self.port_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(conn_frame, text="Topic:").grid(row=2, column=0, sticky=tk.W)
        self.topic_entry = ttk.Entry(conn_frame)
        self.topic_entry.insert(0, "iot/data")
        self.topic_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)

        # Connect button
        self.connect_button = ttk.Button(conn_frame, text="🔌 Connect", command=self.connect)
        self.connect_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Status Frame
        status_frame = ttk.LabelFrame(main, text="Status", padding="5")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Status: Disconnected")
        self.status_label.grid(row=0, column=0, columnspan=2)

        # Statistics Frame
        stats_frame = ttk.LabelFrame(main, text="Statistics", padding="5")
        stats_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.stats_label = ttk.Label(stats_frame, 
                                   text="📊 Received: 0 | ⚠️ Missing: 0 | ❌ Erroneous: 0")
        self.stats_label.grid(row=0, column=0, columnspan=2)

        # Message Display Frame
        display_frame = ttk.LabelFrame(main, text="Messages", padding="5")
        display_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)

        # Text display with scrollbar
        self.text_display = tk.Text(display_frame, height=15, width=50)
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.text_display.yview)
        self.text_display.configure(yscrollcommand=scrollbar.set)
        
        self.text_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 2))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.text_display.tag_configure("error", foreground="red")
        self.text_display.tag_configure("warning", foreground="orange")
        self.text_display.tag_configure("success", foreground="green")

        # Configure grid weights
        main.columnconfigure(0, weight=1)
        main.rowconfigure(4, weight=1)  # Make message display expandable
        for frame in [conn_frame, status_frame, stats_frame]:
            frame.columnconfigure(1, weight=1)

        # MQTT Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def connect(self):
        try:
            host = self.host_entry.get()
            port = int(self.port_entry.get())
            
            self.status_label.config(text="Status: Connecting...", foreground="orange")
            self.connect_button.config(state="disabled")
            self.root.update()
            
            self.client.connect(host, port)
            self.client.loop_start()
            
            self.root.after(100, self.process_queue)
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter a valid port number")
            self.status_label.config(text="Status: Connection Failed", foreground="red")
            self.connect_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            self.status_label.config(text="Status: Connection Failed", foreground="red")
            self.connect_button.config(state="normal")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            topic = self.topic_entry.get()
            self.client.subscribe(topic)
            self.status_label.config(text=f"Status: Connected to {topic}", foreground="green")
        else:
            error_messages = {
                1: "Connection refused - incorrect protocol version",
                2: "Connection refused - invalid client identifier",
                3: "Connection refused - server unavailable",
                4: "Connection refused - bad username or password",
                5: "Connection refused - not authorized"
            }
            error_msg = error_messages.get(rc, f"Connection failed with code {rc}")
            messagebox.showerror("Connection Error", error_msg)
            self.status_label.config(text=f"Status: {error_msg}", foreground="red")
            self.connect_button.config(state="normal")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.status_label.config(text="Status: Unexpected Disconnection", foreground="red")
        else:
            self.status_label.config(text="Status: Disconnected", foreground="black")
        self.connect_button.config(state="normal")

    def on_message(self, client, userdata, msg):
        self.message_queue.put(msg.payload.decode())

    def process_queue(self):
        while not self.message_queue.empty():
            try:
                payload = self.message_queue.get()
                packet = json.loads(payload)
                packet_id = packet["packet_id"]
                value = packet["value"]
                timestamp = packet["timestamp"]

                if self.expected_id is None:
                    self.expected_id = packet_id + 1
                    self.received_count += 1
                    self.display_packet(packet_id, timestamp, value)
                else:
                    if packet_id > self.expected_id:
                        missing_ids = range(self.expected_id, packet_id)
                        self.missing_count += len(missing_ids)
                        self.text_display.insert(tk.END, 
                                              f"⚠️ Missing packets: IDs {self.expected_id} to {packet_id - 1}\n",
                                              "warning")
                    self.expected_id = packet_id + 1
                    self.received_count += 1
                    self.display_packet(packet_id, timestamp, value)

                self.update_stats()
                
            except json.JSONDecodeError:
                self.text_display.insert(tk.END, "❌ Invalid JSON format\n", "error")
            except KeyError as e:
                self.text_display.insert(tk.END, f"❌ Missing required field: {e}\n", "error")
            except Exception as e:
                self.text_display.insert(tk.END, f"❌ Error processing message: {str(e)}\n", "error")
        
        self.root.after(100, self.process_queue)

    def display_packet(self, packet_id, timestamp, value):
        if not isinstance(value, (int, float)):
            self.erroneous_count += 1
            self.text_display.insert(tk.END, 
                                   f"❌ Invalid value type: ID {packet_id}, Time {timestamp}, Value {value}\n",
                                   "error")
        elif value < self.min_value or value > self.max_value:
            self.erroneous_count += 1
            self.text_display.insert(tk.END, 
                                   f"❌ Out of range: ID {packet_id}, Time {timestamp}, Value {value}\n",
                                   "error")
        else:
            self.text_display.insert(tk.END, 
                                   f"✅ Received: ID {packet_id}, Time {timestamp}, Value {value:.2f}\n",
                                   "success")
        self.text_display.see(tk.END)

    def update_stats(self):
        self.stats_label.config(text=f"📊 Received: {self.received_count} | "
                                   f"⚠️ Missing: {self.missing_count} | "
                                   f"❌ Erroneous: {self.erroneous_count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Subscriber(root)
    root.mainloop()