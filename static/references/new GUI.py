import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import csv

from matplotlib.colors import Normalize

numPoints = 10
data = [0]
update_flag = False  # Global flag to control updating

def show_error_popup(message):
    messagebox.showerror("Error", message)

def connect_to_arduino():
    global ser
    selected_baudrate = baudrate_var.get()
    connectPort = 'COM3'  # Replace this with your logic to find Arduino port
    if selected_baudrate != '':
        if connectPort != 'None':
            ser = serial.Serial(connectPort, baudrate=selected_baudrate, timeout=1)
            print('Connected to ' + connectPort)
            connect_button.config(bg='green', fg='white', text='Connected')
        else:
            show_error_popup('Connection Issue!')
    else:
        show_error_popup('Please select baudrate')

def save_to_csv():
    file_path = filedialog.asksaveasfilename(
        initialdir="/", title="Save CSV file", filetypes=[("CSV Files", "*.csv")])

    if file_path:
        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for value in data:
                csv_writer.writerow([value])

def read_data():
    data_list = []
    while True:
        line = ser.readline().decode().strip()
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

def send_request():
    ser.write(b'r')

def read_data_from_arduino():
    send_request()
    global data
    data = read_data()
    print("Received Data List:", data)
    print("Length of Data List:", len(data))

def update_plot():
    global data, update_flag
    if update_flag:
        send_request()
        new_data = read_data()
        data = new_data

        if len(data) >= 3:
            # Define your desired x-axis range
            wavelength_range = np.linspace(300, 900, len(data))

            # Normalize the data to the range [0, 1.0]
            norm = Normalize(vmin=min(data), vmax=max(data))
            normalized_data = norm(data)

            # Clear the plot
            subplot.clear()

            # Create the new plot
            subplot.plot(wavelength_range, normalized_data, linestyle='dotted', label='Intensity')
            subplot.set_xlabel('Wavelength')
            subplot.set_ylabel('Intensity')
            subplot.set_title('AI-powered spectrometer spectrum graph')

            # Set x-axis ticks
            subplot.set_xticks(np.linspace(300, 900, 7))

            # Automatically scale y-axis to the range [0, 1.0]
            subplot.set_ylim(0, 1.1)

            subplot.legend()
            canvas.draw()
        else:
            show_error_popup("Not enough data points for plotting.")

        # Schedule the function to be called again after a delay (e.g., 1000 ms = 1 second)
        root.after(5, update_plot)

def clear_plot():
    global data
    data = [0]  # Clear the data
    subplot.clear()
    canvas.draw()

def toggle_plot():
    global update_flag
    update_flag = not update_flag
    if update_flag:
        update_plot()
    else:
        clear_plot()

root = tk.Tk()
root.title("AI Powered Spectrometer")
root.geometry("480x320")

control_frame = ttk.Frame(root)
control_frame.pack(pady=5, padx=5)

baudrate_var = tk.StringVar()
baudrate_label = ttk.Label(control_frame, text="Baud Rate:")
baudrate_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

baudrate_checklist = ttk.Combobox(control_frame, textvariable=baudrate_var, width=10)
baudrate_checklist['values'] = ['9600', '115200', '230400', '2000000']
baudrate_checklist.grid(row=0, column=1, padx=5, pady=5, sticky='w')

connect_button = tk.Button(control_frame, text="Connect", command=connect_to_arduino, width=10)
connect_button.grid(row=0, column=2, padx=5, pady=5)

read_data_button = tk.Button(control_frame, text="Read Data", command=read_data_from_arduino, width=10)
read_data_button.grid(row=0, column=3, padx=5, pady=5)

toggle_plot_button = tk.Button(control_frame, text="Toggle Plot", command=toggle_plot, width=10)
toggle_plot_button.grid(row=1, column=0, padx=5, pady=5)

clear_plot_button = tk.Button(control_frame, text="Clear Plot", command=clear_plot, width=10)
clear_plot_button.grid(row=1, column=1, padx=5, pady=5)

save_button = tk.Button(control_frame, text="Save to CSV", command=save_to_csv, width=10)
save_button.grid(row=1, column=2, padx=5, pady=5)

plot_frame = ttk.Frame(root)
plot_frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

figure, subplot = plt.subplots(figsize=(4, 2.5), dpi=100)
canvas = FigureCanvasTkAgg(figure, master=plot_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.mainloop()
