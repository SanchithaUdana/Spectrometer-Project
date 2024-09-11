import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.colors import Normalize
from datetime import datetime


class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Splash Screen")
        self.geometry("480x320")

        # Load the background image
        self.background_image = ImageTk.PhotoImage(Image.open("background.png"))

        # Create a canvas widget
        self.canvas = tk.Canvas(self, width=480, height=320)
        self.canvas.pack(fill="both", expand=True)

        # Set the background image on the canvas
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        self.after(5000, self.destroy)  # Destroy splash screen after 5 seconds


class SpectrometerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Powered Spectrometer")
        self.root.geometry("480x320")

        self.numPoints = 10
        self.data = [0]
        self.update_flag = False
        self.ser = None
        self.graph_window = None

        self.create_status_bar()
        self.create_splash_screen()
        self.root.after(3000, self.show_home_screen)  # Show home screen after 3 seconds

    def create_status_bar(self):
        status_frame = tk.Frame(self.root, bg="#2E4053", height=200)
        status_frame.pack(side=tk.TOP, fill=tk.X)

        self.status_label = ttk.Label(status_frame, text="Status: Disconnected", relief=tk.SUNKEN, anchor=tk.W,
                                      background="#2E4053", foreground="#FDFEFE")
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.date_time_label = ttk.Label(status_frame, relief=tk.SUNKEN, anchor=tk.W, background="#2E4053",
                                         foreground="#FDFEFE")
        self.date_time_label.pack(side=tk.LEFT, padx=10)

        self.update_date_time()

    def update_date_time(self):
        now = datetime.now()
        self.date_time_label.config(text=now.strftime("%A %d-%m-%Y %H:%M:%S"))
        self.root.after(1000, self.update_date_time)  # Update every second

    def create_splash_screen(self):
        self.splash = SplashScreen(self.root)
        self.root.withdraw()

    def show_home_screen(self):
        self.root.deiconify()
        self.splash.destroy()

        home_frame = ttk.Frame(self.root)
        home_frame.pack(expand=True)

        welcome_label = ttk.Label(home_frame, text="Welcome to AI Powered Spectrometer", font=("Helvetica", 18))
        welcome_label.pack(pady=20)

        start_button = ttk.Button(home_frame, text="Start Application", command=self.setup_ui)
        start_button.pack()

    def setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_status_bar()

        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=5, padx=5)

        baudrate_label = ttk.Label(control_frame, text="Baud Rate:")
        baudrate_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.baudrate_var = tk.StringVar()
        self.baudrate_checklist = ttk.Combobox(control_frame, textvariable=self.baudrate_var, width=10)
        self.baudrate_checklist['values'] = ['9600', '115200', '230400', '2000000']
        self.baudrate_checklist.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.connect_button = tk.Button(control_frame, text="Connect", command=self.connect_to_arduino, width=10)
        self.connect_button.grid(row=0, column=2, padx=5, pady=5)

        read_data_button = tk.Button(control_frame, text="Read Data", command=self.read_data_from_arduino, width=10)
        read_data_button.grid(row=1, column=1, padx=5, pady=5)

        graph_window_button = tk.Button(control_frame, text="Open Graph", command=self.open_graph_window, width=10)
        graph_window_button.grid(row=1, column=2, padx=5, pady=5)

    def show_error_popup(self, message):
        messagebox.showerror("Error", message)

    def connect_to_arduino(self):
        selected_baudrate = self.baudrate_var.get()
        connectPort = '/dev/ttyUSB0'  # Replace this with your logic to find Arduino port
        if selected_baudrate != '':
            if connectPort != 'None':
                try:
                    self.ser = serial.Serial(connectPort, baudrate=selected_baudrate, timeout=1)
                    print('Connected to ' + connectPort)
                    self.connect_button.config(bg='green', fg='white', text='Connected')
                    self.update_status("Connected")
                except Exception as e:
                    self.show_error_popup(f'Connection failed: {str(e)}')
                    self.update_status("Connection failed")
            else:
                self.show_error_popup('Connection Issue!')
                self.update_status("Connection Issue")
        else:
            self.show_error_popup('Please select baudrate')
            self.update_status("Select Baudrate")

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")

    def save_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            initialdir="/", title="Save CSV file", filetypes=[("CSV Files", "*.csv")])

        if file_path:
            with open(file_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                for value in self.data:
                    csv_writer.writerow([value])

    def read_data(self):
        data_list = []
        while True:
            line = self.ser.readline().decode().strip()
            if not line:
                continue
            elif line == 's':
                continue
            elif line == 'f':
                break
            else:
                data_list.append(int(line))

        if data_list:
            data_list.pop()

        return data_list

    def send_request(self):
        self.ser.write(b'r')

    def read_data_from_arduino(self):
        self.send_request()
        self.data = self.read_data()
        print("Received Data List:", self.data)
        print("Length of Data List:", len(self.data))

    def open_graph_window(self):
        if self.graph_window is None or not tk.Toplevel.winfo_exists(self.graph_window):
            self.graph_window = GraphWindow(self)
        else:
            self.graph_window.lift()

    def clear_plot(self):
        if self.graph_window:
            self.graph_window.clear_plot()


class GraphWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.title("Graph Window")
        self.geometry("480x320")

        self.update_flag = False
        self.mode = 'wavelength'  # Default mode
        self.average_points = 10  # Initialize average_points with a default value

        control_frame = ttk.Frame(self)
        control_frame.pack(pady=5, padx=5)

        toggle_plot_button = tk.Button(control_frame, text="Toggle Plot", command=self.toggle_plot, width=10)
        toggle_plot_button.grid(row=0, column=0, padx=5, pady=5)

        clear_plot_button = tk.Button(control_frame, text="Clear Plot", command=self.clear_plot, width=10)
        clear_plot_button.grid(row=0, column=1, padx=5, pady=5)

        save_button = tk.Button(control_frame, text="Save to CSV", command=self.app.save_to_csv, width=10)
        save_button.grid(row=0, column=2, padx=5, pady=5)

        mode_button = tk.Button(control_frame, text="Switch to Frequency", command=self.switch_mode, width=20)
        mode_button.grid(row=1, column=0, padx=5, pady=5)
        self.mode_button = mode_button

        average_label = ttk.Label(control_frame, text="Window Average:")
        average_label.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.average_var = tk.IntVar(value=10)
        self.average_dropdown = ttk.Combobox(control_frame, textvariable=self.average_var, width=10)
        self.average_dropdown['values'] = [10, 20, 30, 40, 50, 60, 70, 80, 100]
        self.average_dropdown.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.average_dropdown.bind("<<ComboboxSelected>>", self.update_average)

        plot_frame = ttk.Frame(self)
        plot_frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        self.figure, self.subplot = plt.subplots(figsize=(7, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def switch_mode(self):
        if self.mode == 'wavelength':
            self.mode = 'frequency'
            self.mode_button.config(text="Switch to Wavelength")
        else:
            self.mode = 'wavelength'
            self.mode_button.config(text="Switch to Frequency")
        if self.update_flag:
            self.update_plot()

    def toggle_plot(self):
        self.update_flag = not self.update_flag
        if self.update_flag:
            self.update_plot()
        else:
            self.clear_plot()

    def update_average(self, event=None):
        self.average_points = self.average_var.get()
        if self.update_flag:
            self.update_plot()

    def update_plot(self):
        if self.update_flag:
            self.app.send_request()
            new_data = self.app.read_data()
            self.app.data = new_data

            if len(self.app.data) >= 3:
                averaged_data = np.array([np.mean(self.app.data[i:i + self.average_points])
                                          for i in range(0, len(self.app.data), self.average_points)])

                if self.mode == 'wavelength':
                    x_data = np.linspace(300, 900, len(averaged_data))
                    x_label = 'Wavelength (nm)'
                else:
                    x_data = 3e8 / (np.linspace(300, 900, len(averaged_data)) * 1e-9) / 1e12
                    x_label = 'Frequency (THz)'

                norm = Normalize(vmin=min(averaged_data), vmax=max(averaged_data))
                normalized_data = norm(averaged_data)
                inverted_data = 1 - normalized_data

                self.subplot.clear()
                self.subplot.plot(x_data, inverted_data, linestyle='solid', label='Intensity')
                self.subplot.set_xlabel(x_label)
                self.subplot.set_ylabel('Intensity')
                self.subplot.set_title('AI-powered spectrometer spectrum graph')

                if self.mode == 'wavelength':
                    self.subplot.set_xticks(np.linspace(300, 900, 7))
                else:
                    self.subplot.set_xticks(np.linspace(min(x_data), max(x_data), 7))
                self.subplot.set_ylim(0, 1.1)

                max_value = max(inverted_data)
                max_x = x_data[np.argmax(inverted_data)]
                self.subplot.annotate(f'Peak: {max_x:.1f} {x_label.split()[1]}', xy=(max_x, max_value),
                                      xytext=(max_x + 50, max_value - 0.1),
                                      arrowprops=dict(facecolor='black', shrink=0.05))

                self.subplot.legend()
                self.canvas.draw()
            else:
                self.app.show_error_popup("Not enough data points for plotting.")

            self.after(10, self.update_plot)

    def clear_plot(self):
        self.app.data = [0]
        self.subplot.clear()
        self.canvas.draw()
        self.update_flag = False



if __name__ == "__main__":
    root = tk.Tk()
    app = SpectrometerApp(root)
    root.mainloop()
