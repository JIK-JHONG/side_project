import matplotlib.pyplot as plt
import tkinter as tk
from datetime import datetime
from tkinter import ttk

# Author : JIK JHONG
# This is the program for generating the step function

def run_plot():
    time_start = int(time_active_range_start.get())
    time_end = int(time_active_range_end.get())
    images_save = var_images_save.get()
    image_file_name = image_file_title.get()
    output_file_type = entry_output_file_type.get()
    output_filename_cc = datetime.now().strftime("%Y-%m-%d")
    if image_file_name:
        output_filename_out = f"img_{image_file_name}_{output_filename_cc}.{output_file_type}"
    else:
        output_filename_out = f"img_step_function_{output_filename_cc}.{output_file_type}"
    time = [0, time_start, time_start, time_end, time_end, (time_end + 20)]
    power = [0, 0, 1, 1, 0, 0]

    plt.figure()

    plt.plot(time, power, color='red', linewidth=4)

    # Title setting
    plt.title('Power Setting', fontsize=14, fontweight='bold')

    plt.xlabel('time (sec)', fontsize=16, fontweight='bold')
    plt.ylabel('Power On', fontsize=16, fontweight='bold')

    plt.xlim(-10, max(time))
    plt.ylim(-0.1, 1.1)

    # remove frame
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.tick_params(axis='both', which='major', labelsize=14) 

    # hide the y-axis value
    plt.gca().get_yaxis().set_ticks([])

    plt.grid(False)

    if images_save:
        plt.savefig(f'{output_filename_out}') 

    plt.show()


width_range = 20
width_range_tail = 10
width_text = 50
width_title = 20

root = tk.Tk()
root.title(f"Step Function Generator")
style = ttk.Style()
style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 12))
notebook = ttk.Notebook(root, style='TNotebook')

notebook.pack(expand=True, fill='both')

basic_frame = ttk.Frame(notebook)

notebook.add(basic_frame, text='Basic')


frame_title = tk.Frame(basic_frame, pady=10, padx=10)
frame_title.pack(fill=tk.X)

frame_range = tk.Frame(basic_frame, pady=10, padx=10)
frame_range.pack(fill=tk.X)


frame_main = tk.Frame(basic_frame, pady=10, padx=10)
frame_main.pack(fill=tk.X)


frame_label = tk.Frame(basic_frame, pady=10, padx=10)
frame_label.pack(fill=tk.X)


label_title = tk.Label(frame_title, text=f"This program is a program that generates STEP FUNCTION waveforms",font=('Arial',14,'bold'), pady=10, padx=0,width=width_title*3, anchor="w", justify="left")
label_title.grid(row=0, column=0, columnspan=2, sticky=tk.NW)

root.resizable(False, True)

tk.Label(frame_range, text="Step Function Setting:", width=width_title, anchor="w").grid(row=2, column=0, sticky=tk.NW)
time_active_range_start = tk.Spinbox(frame_range, from_=0, to=99999, width=width_range)
time_active_range_start.grid(row=2, column=1, sticky=tk.NW)
time_active_range_tail = tk.Label(frame_range, width=width_range_tail, text="~")
time_active_range_tail.grid(row=2, column=2, sticky=tk.NW)
time_active_range_end = tk.Spinbox(frame_range, from_=0, to=99999, width=width_range)
time_active_range_end.grid(row=2, column=3, sticky=tk.NW)

time_active_range_start.delete(0, 'end')
time_active_range_start.insert(0, 20)
time_active_range_end.delete(0, 'end')
time_active_range_end.insert(0, 100)
var_images_save = tk.BooleanVar(value=True)

tk.Label(frame_main, text="Image Output Engine", width=width_title,anchor="w").grid(row=3, column=0, sticky=tk.NW)
tk.Checkbutton(frame_main, text="Active", variable=var_images_save).grid(row=3, column=1, columnspan=3, sticky=tk.NW)

tk.Label(frame_main, text="Output File Type:", width=width_title,anchor="w").grid(row=4, column=0, sticky=tk.NW)
entry_output_file_type = ttk.Combobox(frame_main, values=['png','jpg'], )
entry_output_file_type.grid(row=4, column=1, columnspan=3,sticky=tk.NW)
entry_output_file_type.set('png')

tk.Label(frame_main, text="File Title:", width=width_title, anchor="w").grid(row=5, column=0, sticky=tk.NW)
image_file_title = tk.Entry(frame_main, width=width_text)
image_file_title.grid(row=5, column=1, columnspan=3, sticky=tk.NW)
image_file_title.insert(0, "step_function")

tk.Label(frame_main, text="Default file name : img_step_function_date.png / jpg",font=('Arial',12,'bold italic'), width=width_title*3, anchor="w").grid(row=6, column=1, sticky=tk.NW)

tk.Button(frame_label, pady=2, padx=20, width=width_range, height=2, text="Process Data", command=run_plot).grid(row=10, column=0, sticky=tk.W)

root.mainloop()
