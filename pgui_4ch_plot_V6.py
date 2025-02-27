import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from scipy.signal import savgol_filter
import openpyxl
import csv
#import time
import tkinter as tk
from tkinter import filedialog, messagebox, Menu , ttk, Text

import os
def write_to_csv(filename, col_title, row_title, row_file, data, basic_data):
    rows = [[row_title[i]] + list(data[i]) + [row_file[i]] for i in range(len(row_title))]
    
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for item in basic_data:
            csvwriter.writerow([item])
        csvwriter.writerow([''] + col_title)
        csvwriter.writerows(rows)

def write_to_excel(filename, col_title, row_title, row_file,  data, basic_data):
    wb = openpyxl.Workbook()
    sheet = wb.active
    for item in basic_data:
        sheet.append([item])
    sheet.append([''] + col_title)
    for i in range(len(row_title)):
        sheet.append([row_title[i]]  + list(data[i]) + [row_file[i]])
    wb.save(filename)

def importfile(filepath):
    data = pd.read_csv(filepath, delimiter='\t', header=0, encoding='ISO-8859-1', skiprows=1)
    data = data.apply(pd.to_numeric, errors='coerce')
    return data.values

def process_data():
    try:
        row_file = []
        #filepath_prefix = entry_filepath_prefix.get()
        filepath_prefix = ""
        #filename = entry_filename.get().split(',')
        filenames = []
        for i in range(entry_filename.size()):
            filenames.append(entry_filename.get(i))
            row_file.append(os.path.basename(entry_filename.get(i)))
        #display_label = entry_display_label.get().split(',')
        #display_label = entry_display_label
        display_label = []        
        for i in range(len(entry_display_label)):
            display_label.append(entry_display_label[i].get())
        

        

        min_value_0 = int(entry_temp_range_0_min.get())
        max_value_0 = int(entry_temp_range_0_max.get())
        min_value_1 = int(entry_temp_range_1_min.get())
        max_value_1 = int(entry_temp_range_1_max.get())
        min_value_2 = int(entry_temp_range_2_min.get())
        max_value_2 = int(entry_temp_range_2_max.get())
        min_value_3 = int(entry_temp_range_3_min.get())
        max_value_3 = int(entry_temp_range_3_max.get())



        temperature_range_set = {
            0: [min_value_0,max_value_0],
            1: [min_value_1,max_value_1],
            2: [min_value_2,max_value_2],
            3: [min_value_3,max_value_3],
        }

        var_average_set_active = []
        var_average_set = {
            0: var_average_0,
            1: var_average_1,
            2: var_average_2,
            3: var_average_3
        }

        var_channel_select_set = {
            0: var_channel_select_1,
            1: var_channel_select_2,
            2: var_channel_select_3,
            3: var_channel_select_4
        }



        input_v = float(entry_input_v.get())
        input_a = float(entry_input_a.get())
        sample_start = int(entry_sample_start.get())
        sample_end = int(entry_sample_end.get())

        image_range_start = int(range_output_start.get())
        image_range_end = int(range_output_end.get())
        

        entry_get_column_set = []
        if(var_channel_select_1.get()):
            entry_get_column_set.append(1)
        if(var_channel_select_2.get()):
            entry_get_column_set.append(2)
        if(var_channel_select_3.get()):
            entry_get_column_set.append(3)
        if(var_channel_select_4.get()):
            entry_get_column_set.append(4)

        output_image = var_output_image.get()
        file_title = entry_file_title.get()
        img_title = entry_img_title.get()
        output_file_type = entry_output_file_type.get()
        func_smooth = var_func_smooth.get()
        func_smooth_para = 50
        gnuplot_support = var_gnuplot_support.get()
        shfit_to_zero = var_shfit_to_zero.get()
        output_csv = var_output_csv.get()
        output_excel = var_output_excel.get()
        output_title_power = var_output_title_power.get()
        output_result_box = var_output_result_box.get()
        output_time_set = var_output_time_set.get()
        textarea_input = vat_textarea_input.get("1.0", tk.END)
        basic_data = [
            f"Basic Info - auto generated log",
            f"Created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Experiment Output Date Set = {datetime.now().strftime('%Y-%m-%d')}",
            f"Heater Set V  = {input_v} V",
            f"Heater Set I  = {input_a} A",
            f"Heater Set P = {(input_v * input_a):>5.2f} W",
            f"Average Range = {sample_start} - {sample_end} sec",
            f"Shift to Zero = {shfit_to_zero}",
            f"Smooth Style = {func_smooth}",
            f"Note = {textarea_input}"
        ]

        # for i, value in var_channel_select_set.items():
        #     if(value):
        #         var_average_set_active.append(i)


        row_title = display_label

        col_title = entry_get_column_set
        T_tmp = np.zeros((len(display_label), len(entry_get_column_set)))
        if shfit_to_zero:
            T_tmp_inc = np.zeros((len(display_label), len(entry_get_column_set)))

        for channel_id in range(len(entry_get_column_set)):
            target_name = f"Sensor T{channel_id}"
            if output_title_power:
                title_name = f"Heater@{(input_v * input_a):>5.2f} W - {target_name}"
            else:
                title_name = f"Heater - {target_name}"
            
            get_column = entry_get_column_set[channel_id]
            output_filename = f"S{get_column}"
            output_filename_ccx = f"Gnuplot{get_column}_"
            output_filename_cc = datetime.now().strftime("%Y-%m-%d-")
            output_filename_out = f"{img_title}_{output_filename_cc}{output_filename}.{output_file_type}"

            input_file_set = len(filenames)
            nyc = np.zeros(input_file_set)

            for i in range(input_file_set):
                data = importfile(filepath_prefix + filenames[i])
                nyc[i] = data.shape[0]

            n = int(np.min(nyc))
            time_range_start = 0
            time_range_end = n
             

            output = np.zeros((n, input_file_set))
            output_rt = np.zeros((n, input_file_set))

            for i in range(input_file_set):
                print(filenames[i])
                print(channel_id)
                data = importfile(filepath_prefix + filenames[i])
                output[:, i] = data[:n, (get_column+2) - 1]
                T_tmp[i, channel_id] = np.nanmean(output[sample_start:sample_end, i])

            

            if func_smooth:
                for i in range(input_file_set):
                    #output[:, i] = savgol_filter(output[:, i], func_smooth_para, 3)
                    output[21:, i] = savgol_filter(output[21:, i], func_smooth_para, 5)
                    # for k in range(output.shape[0]):
                    #     if output[k, i]<0:
                    #         output[k, i] = 0


            if shfit_to_zero:
                for i in range(input_file_set):
                    output[:, i] = output[:, i] - np.nanmean(output[0:20, i])
                    output[0:21, i] = 0.0
                    T_tmp_inc[i, channel_id] = np.nanmean(output[sample_start:sample_end, i])
            # 設定輸出時間範圍
            if output_time_set:
                time_range_start = int(range_output_start.get())
                time_range_end = int(range_output_end.get())
            # for i in range(len(var_average_set_active)):
            #     var_average_set[var_average_set_active[i]].set(T_tmp[i, channel_id])

            
            x1 = np.arange(1, n + 1)
            ymatrix1 = output

            fig, ax = plt.subplots()
            if output_image:
                plt.ion()
            else:
                plt.ioff()

            temperature_range = temperature_range_set[channel_id]
            ax.set_xlim([time_range_start, time_range_end])
            ax.set_ylim(temperature_range)
            ax.grid(True)
            ax.set_xlabel("Time(sec)", fontweight="bold", fontsize=12)
            ax.set_ylabel("Increasing Temperature(°C)" if shfit_to_zero else "Temperature(°C)", fontweight="bold", fontsize=12)
            ax.set_title(title_name, fontweight="bold", fontsize=12)

            for i in range(input_file_set):
                ax.plot(x1, ymatrix1[:, i], label=display_label[i], linewidth=2)

            ax.legend()

            if output_image:
                plt.savefig(output_filename_out)
                print(f"The image is saved '{output_filename_out}'")
            plt.show()

            if gnuplot_support:
                output_gnuplot = f"{file_title}_{output_filename_ccx}{get_column}.dat"
                with open(output_gnuplot, "w") as f:
                    for i in range(n):
                        f.write(f"{x1[i]}\t" + "\t".join(f"{ymatrix1[i, j]}" for j in range(input_file_set)) + "\n")


        T_result = T_tmp
        if shfit_to_zero:
            T_result_inc = T_tmp_inc
        else:
            T_result_inc = T_tmp
        T_set = [T_result,T_result_inc] 
        Sample_range_set = [sample_start,sample_end]
        if output_result_box:
            result_box_dialog(display_label,T_set,Sample_range_set,shfit_to_zero)

        if output_csv or output_excel:
            filename = datetime.now().strftime("%Y-%m-%d")
            col_title.append('File_Name')
            if output_csv:
                write_to_csv(f"{file_title}_{filename}.csv", col_title, row_title, row_file, T_tmp, basic_data)
                if shfit_to_zero:
                    write_to_csv(f"{file_title}_{filename}_inc.csv", col_title, row_title, row_file, T_tmp_inc, basic_data)
            if output_excel:
                write_to_excel(f"{file_title}_{filename}.xlsx", col_title, row_title, row_file, T_tmp, basic_data)
                if shfit_to_zero:
                    write_to_excel(f"{file_title}_{filename}_inc.xlsx", col_title, row_title, row_file, T_tmp_inc, basic_data)
    except Exception as e:
        # 捕获任何异常，并打印异常信息
        #print(f"An error occurred: {str(e)}")
        error_dialog(str(e))


def select_files():
    filenames = filedialog.askopenfilenames(title="Select Files", filetypes=[("4ch files", "*.4ch")])
    if filenames:
        folder_path = os.path.dirname(filenames[0])
        entry_filepath_prefix.config(text = folder_path)
        # entry_filepath_prefix.delete(0, tk.END)
        # entry_filepath_prefix.insert(tk.END, folder_path)
        entry_filename.delete(0, tk.END)
        for filename in filenames:
            entry_filename.insert(tk.END, filename)
        update_file_count_label()
        add_label_edit_in_frame()

def remove_file(event=None):
    selected_items = entry_filename.curselection()
    for index in reversed(selected_items):
        entry_filename.delete(index)

    update_file_count_label()
    add_label_edit_in_frame()    

def update_file_count_label():
    input_count.set(entry_filename.size())
    label_file_input.config(text=f"File Input( {input_count.get()} ):")
    if input_count.get() == 0 :
        #entry_filepath_prefix.delete(0, tk.END)
        entry_filepath_prefix.config(text = "")

def show_hide_entry(id):
    if id == 0:
        if var_channel_select_1.get():
            label_temp_range_0.grid(row=14, column=0, sticky=tk.NW)
            label_temp_range_0_tail.grid(row=14, column=2, sticky=tk.NW)
            entry_temp_range_0_min.grid(row=14, column=1, sticky=tk.NW)
            entry_temp_range_0_max.grid(row=14, column=3, sticky=tk.NW)
        else:
            label_temp_range_0.grid_remove()
            label_temp_range_0_tail.grid_remove()
            entry_temp_range_0_min.grid_remove()
            entry_temp_range_0_max.grid_remove()
    elif id == 1:
        if var_channel_select_2.get():
            label_temp_range_1.grid(row=15, column=0, sticky=tk.NW)
            label_temp_range_1_tail.grid(row=15, column=2, sticky=tk.NW)
            entry_temp_range_1_min.grid(row=15, column=1, sticky=tk.NW)
            entry_temp_range_1_max.grid(row=15, column=3, sticky=tk.NW)
        else:
            label_temp_range_1.grid_remove()
            label_temp_range_1_tail.grid_remove()
            entry_temp_range_1_min.grid_remove()
            entry_temp_range_1_max.grid_remove()
    elif id == 2:
        if var_channel_select_3.get():
            label_temp_range_2.grid(row=16, column=0, sticky=tk.NW)
            label_temp_range_2_tail.grid(row=16, column=2, sticky=tk.NW)
            entry_temp_range_2_min.grid(row=16, column=1, sticky=tk.NW)
            entry_temp_range_2_max.grid(row=16, column=3, sticky=tk.NW)
        else:
            label_temp_range_2.grid_remove()
            label_temp_range_2_tail.grid_remove()
            entry_temp_range_2_min.grid_remove()
            entry_temp_range_2_max.grid_remove()
    elif id == 3:
        if var_channel_select_4.get():
            label_temp_range_3.grid(row=17, column=0, sticky=tk.NW)
            label_temp_range_3_tail.grid(row=17, column=2, sticky=tk.NW)
            entry_temp_range_3_min.grid(row=17, column=1, sticky=tk.NW)
            entry_temp_range_3_max.grid(row=17, column=3, sticky=tk.NW)
        else:
            label_temp_range_3.grid_remove()
            label_temp_range_3_tail.grid_remove()
            entry_temp_range_3_min.grid_remove()
            entry_temp_range_3_max.grid_remove()
def reset_hide_entry(id):
    if id == 0:
        label_temp_range_0.grid_remove()
        label_temp_range_0_tail.grid_remove()
        entry_temp_range_0_min.grid_remove()
        entry_temp_range_0_max.grid_remove()
    elif id == 1:
        label_temp_range_1.grid_remove()
        label_temp_range_1_tail.grid_remove()
        entry_temp_range_1_min.grid_remove()
        entry_temp_range_1_max.grid_remove()
    elif id == 2:
        label_temp_range_2.grid_remove()
        label_temp_range_2_tail.grid_remove()
        entry_temp_range_2_min.grid_remove()
        entry_temp_range_2_max.grid_remove()
    elif id == 3:
        label_temp_range_3.grid_remove()
        label_temp_range_3_tail.grid_remove()
        entry_temp_range_3_min.grid_remove()
        entry_temp_range_3_max.grid_remove()   
    else:
        label_temp_range_0.grid_remove()
        label_temp_range_0_tail.grid_remove()
        entry_temp_range_0_min.grid_remove()
        entry_temp_range_0_max.grid_remove()
        label_temp_range_1.grid_remove()
        label_temp_range_1_tail.grid_remove()
        entry_temp_range_1_min.grid_remove()
        entry_temp_range_1_max.grid_remove()
        label_temp_range_2.grid_remove()
        label_temp_range_2_tail.grid_remove()
        entry_temp_range_2_min.grid_remove()
        entry_temp_range_2_max.grid_remove()
        label_temp_range_3.grid_remove()
        label_temp_range_3_tail.grid_remove()
        entry_temp_range_3_min.grid_remove()
        entry_temp_range_3_max.grid_remove()    


def show_hide_time_range(id):
    if id == 0:
        if var_output_time_set.get():
            label_time_range.grid(row=23, column=0, sticky=tk.NW)
            range_output_tail.grid(row=23, column=2, sticky=tk.NW)
            range_output_start.grid(row=23, column=1, sticky=tk.NW)
            range_output_end.grid(row=23, column=3, sticky=tk.NW)
        else:
            label_time_range.grid_remove()
            range_output_tail.grid_remove()
            range_output_start.grid_remove()
            range_output_end.grid_remove()
   
def reset_hide_time_range(id):
    if id == 0:
        label_time_range.grid_remove()
        range_output_tail.grid_remove()
        range_output_start.grid_remove()
        range_output_end.grid_remove()   
    else:
        label_time_range.grid_remove()
        range_output_tail.grid_remove()
        range_output_start.grid_remove()
        range_output_end.grid_remove()      


def validate_spinbox(value, minval, maxval):
    try:
        value = int(value)
        if value < minval:
            return minval
        elif value > maxval:
            return maxval
        else:
            return value
    except ValueError:
        return minval

def on_spinbox_validate(minval, maxval):
    def validator(P):
        if P.isdigit():
            value = int(P)
            if minval <= value <= maxval:
                return True
            else:
                return False
        elif P == "":
            return True
        else:
            return False
    return validator  
# Function to handle drag-and-drop reordering
def on_drag_start(event):
    global drag_data
    selected_indices = entry_filename.curselection()
    if selected_indices:
        drag_data['index'] = selected_indices[0]
        drag_data['item'] = entry_filename.get(drag_data['index'])

def on_drag_motion(event):
    global drag_data, drag_active
    if 'index' in drag_data and drag_data['index'] is not None:
        current_index = entry_filename.nearest(event.y)
        if current_index != drag_data['index']:
            # Perform the reorder
            items = list(entry_filename.get(0, tk.END))
            items.remove(drag_data['item'])
            items.insert(current_index, drag_data['item'])
            # Delete all items from the Listbox
            entry_filename.delete(0, tk.END)
            # Insert items into the Listbox in the new order
            for item in items:
                entry_filename.insert(tk.END, item)
            # Update drag_data index and item
            drag_data['index'] = current_index
            drag_data['item'] = entry_filename.get(current_index)
            drag_active = 1 
            update_file_count_label()
            add_label_edit_in_frame()


def on_drag_end(event):
    global drag_active,drag_data
    # if(drag_active == 1):
    #     drag_data.clear()
    #     update_file_count_label()
    #     add_label_edit_in_frame()
    #     drag_active = 0 
# Dictionary to hold drag data




def add_label_edit_in_frame():
    # Clear previous widgets
    if(input_count.get() > 0  ):
        for widget in frame_label.winfo_children():
            widget.destroy()
        
        # Create new labels and entries based on selected filenames
        filenames = entry_filename.get(0, tk.END)
        
        tk.Label(frame_label, text="Display Label:", width=width_title,anchor="w").grid(row=0, column=0, sticky=tk.NW)
        entry_display_label.clear()
        for i, filename in enumerate(filenames):
            filename_only = os.path.basename(filename)  # Extract filename without path
            label_data_set = tk.Label(frame_label, text=f"[{i}] {filename_only}", width=width_range*2, anchor="w")
            label_data_set.grid(row=i, column=1, sticky=tk.NW, padx=0, pady=1)
            
            entry_display_label_tmp = tk.Entry(frame_label, width=width_range)
            entry_display_label_tmp.grid(row=i, column=2, columnspan=3, sticky=tk.NW, padx=0, pady=1)
            entry_display_label_tmp.insert(0,f'SAMPLE_{i}')
            entry_display_label.append(entry_display_label_tmp)
    else:
        tk.Label(frame_label, text="Display Label:", width=width_title, anchor="w").grid(row=0, column=0, sticky=tk.NW)
        entry_display_label.clear()
        for widget in frame_label.winfo_children():
            widget.destroy()
        entry_filepath_prefix.config(text="")  # Make sure to clear the content



def close_msg_box():
    version_box.destroy()
def version_dialog():
    global version_box, update_log
    version_box = tk.Tk()
    version_box.title('分析軟體版本資訊')
    #version_box.geometry('500x250')
    version_box_title = tk.Frame(version_box, pady=10, padx=10)
    version_box_title.pack(fill=tk.X)
    version_box_msg_0 = tk.Label(version_box_title, text=f"Data Analysis Tool",font=('Arial',20,'bold'), pady=10, padx=0)
    version_box_msg_0.grid(row=0, column=0, sticky=tk.NW)
    version_box_msg_0 = tk.Label(version_box_title, text=f"Version : {gui_version}")
    version_box_msg_0.grid(row=1, column=0, sticky=tk.NW)
    version_box_msg_1 = tk.Label(version_box_title, text=f"Relased on : {relase_date}")
    version_box_msg_1.grid(row=2, column=0, sticky=tk.NW)
    version_box_msg_2 = tk.Label(version_box_title, text=f"Author : JIK JHONG")
    version_box_msg_2.grid(row=3, column=0, sticky=tk.NW)   
    version_box_msg_3 = tk.Label(version_box_title, text=f"Email : jik.jhong@gmail.com")
    version_box_msg_3.grid(row=4, column=0, sticky=tk.NW)   
    version_box_btn = tk.Button(version_box_title, width=60, height=2 , text="Close", command=close_msg_box)
    version_box_btn.grid(row=5, column=0, sticky=tk.E , pady=10, padx=10)

    version_box_content = ttk.Treeview(version_box)
    version_box_content.pack(fill=tk.BOTH, expand=True)


    version_box_content['columns'] = ('event','version')
    version_box_content.column('event', width=300)
    version_box_content.column('version', width=100 ,anchor='center')
    version_box_content.heading("#0", text="Update")
    version_box_content.heading('event', text='Event')
    version_box_content.heading('version', text='Version')

    for i in range(len(update_log['event'])):
        update_log_msg = update_log['event'][i]
        print(update_log['event'][i])
        version_box_content.insert('','end',text=f'{update_log['upadte'][i]}',values=(update_log_msg,update_log['version'][i]))


    


   

    # version_box_msg_0 = tk.Label(version_box_title, text=f"Version : {gui_version}:")
    # version_box_msg_0.pack(anchor=tk.W)

    # version_box_msg_1 = tk.Label(version_box, text=f"Release on : {release_date}:")
    # version_box_msg_1.pack(anchor=tk.W)

def close_error_msg_box():
    error_box.destroy()
def error_dialog(msg):
    global error_box
    error_box = tk.Tk()
    error_box.title('Error')
    error_box_title = tk.Frame(error_box, pady=10, padx=10)
    error_box_title.pack(fill=tk.X)
    error_box_msg_0 = tk.Label(error_box_title, text="Error Info.", font=('Arial', 20, 'bold'), pady=10, padx=0)
    error_box_msg_0.grid(row=0, column=0, sticky=tk.NW)
    error_box_msg_1 = tk.Label(error_box_title, text=f"Message: {msg}")
    error_box_msg_1.grid(row=1, column=0, sticky=tk.NW)
    error_box_btn = tk.Button(error_box_title, height=2, text="Close", command=close_error_msg_box)
    error_box_btn.grid(row=2, column=0, sticky=tk.E, pady=10, padx=10)






def close_result_box():
    if result_box:
        result_box.destroy()
def result_box_dialog(Label_set,T_set,Range_set,option):
    global result_box
    result_box = tk.Tk()
    result_box.title('Summary')
    #result_box.geometry('500x450')
    
    """     
    image_path = 'path_to_your_image.png'  # 替換為你的圖片文件路徑
    image = Image.open(image_path)
    image = image.resize((200, 200), Image.ANTIALIAS)  # 調整圖片大小
    photo = ImageTk.PhotoImage(image)
    
    # 在視窗中顯示圖片
    label = tk.Label(result_box, image=photo)
    label.image = photo  # 保持對圖片的引用，防止圖片被垃圾回收
    label.pack(pady=10) 
    """

    result_box_title = tk.Frame(result_box, pady=10, padx=10)
    result_box_title.pack(fill=tk.X)

    version_box_msg_0 = tk.Label(result_box_title, text=f"Summary for Analysis", font=('Arial', 16, 'bold'), pady=10, padx=0)
    version_box_msg_0.grid(row=0, column=0, sticky=tk.W)

    version_box_msg_1 = tk.Label(result_box_title, text=f"Data Range : {Range_set[0]} - {Range_set[1]}")
    version_box_msg_1.grid(row=1, column=0, sticky=tk.W)
   
    result_box_content = ttk.Treeview(result_box)
    result_box_content.pack(fill=tk.BOTH, expand=True)

    if option:
        result_box_content['columns'] = ('tmp', 'tmp_inc')
        result_box_content.column('tmp', width=100, anchor='center')
        result_box_content.column('tmp_inc', width=100, anchor='center')
        result_box_content.heading("#0", text="Label")
        result_box_content.heading('tmp', text='Temperature (°C)')
        result_box_content.heading('tmp_inc', text='Temperature - Modified (°C)')

        for i in range(len(Label_set)):
            result_box_content.insert('','end',text=f'{Label_set[i]}',values=(T_set[0][i], T_set[1][i]))
    else:
        result_box_content['columns'] = ('tmp', 'tmp_inc')
        result_box_content.column('tmp', width=100, anchor='center')
        result_box_content.column('tmp_inc', width=100, anchor='center')
        result_box_content.heading("#0", text="Label")
        result_box_content.heading('tmp', text='Temperature (°C)')
        result_box_content.heading('tmp_inc', text='-')

        for i in range(len(Label_set)):
            result_box_content.insert('','end',text=f'{Label_set[i]}',values=(T_set[0][i],f'-'))       

    result_box_end = tk.Frame(result_box, pady=10, padx=10)
    result_box_end.pack(fill=tk.X)

    version_box_btn = tk.Button(result_box_end, width=60, height=2, text="Close", command=close_result_box)
    version_box_btn.grid(row=0, column=0, sticky=tk.E, pady=10, padx=10)
    

   

    # version_box_msg_0 = tk.Label(version_box_title, text=f"Version : {gui_version}:")
    # version_box_msg_0.pack(anchor=tk.W)

    # version_box_msg_1 = tk.Label(version_box, text=f"Release on : {release_date}:")
    # version_box_msg_1.pack(anchor=tk.W)


# GUI
# pardir = 'images'
# logoPath = os.path.join(pardir, 'btn_invoice_insert_sample.png')

#   V   0.1    First Version                            2024/06/28
#   V   0.2    Add the Summary Window for Analysis      2024/07/10
#   V   0.3    Add output range setting for time        2024/07/25

update_log = {'upadte': ['2024/07/25','2024/07/10','2024/06/28'],
              'event': ['Add output range setting for time','Add the Summary Window for Analysis','First Version'],
              'version':['0.3','0.2','0.1']
              }
gui_version = 0.3
relase_date = '2024/07/25'
drag_active = 0 

minval = 0 
maxval = 200
width_range = 20
width_range_tail = 10
width_text = 60
width_title = 20
width_text_reduse = width_text - width_range_tail
drag_data = {'index': None, 'item': None}

file_frames = []
entry_display_label = []
drag_data = {}




root = tk.Tk()

style = ttk.Style()
style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 12))
notebook = ttk.Notebook(root, style='TNotebook')

notebook.pack(expand=True, fill='both')

basic_frame = ttk.Frame(notebook)
output_setting_frame = ttk.Frame(notebook)
parameter_setting_frame = ttk.Frame(notebook)
note_frame = ttk.Frame(notebook)

notebook.add(basic_frame, text='Basic')
notebook.add(parameter_setting_frame, text='Parameter')
notebook.add(output_setting_frame, text='Output')
notebook.add(note_frame, text='Note')
#標題frame
frame_title = tk.Frame(basic_frame, pady=10, padx=10)
frame_title.pack(fill=tk.X)

#主要檔案選擇frame
frame = tk.Frame(basic_frame, pady=10, padx=10)
frame.pack(fill=tk.X)

#客製化（名稱）frame
frame_label = tk.Frame(basic_frame, pady=10, padx=10)
frame_label.pack(fill=tk.X)

#其餘功能frame
#frame_sub = tk.Frame(root, pady=10, padx=10, bg='#f90')
frame_sub = tk.Frame(parameter_setting_frame, pady=10, padx=10)
frame_sub.pack(fill=tk.X)

frame_option = tk.Frame(output_setting_frame, pady=10, padx=10)
frame_option.pack(fill=tk.X)


frame_option_time_range = tk.Frame(output_setting_frame, pady=10, padx=10)
frame_option_time_range.pack(fill=tk.X)

frame_note = tk.Frame(note_frame, pady=10, padx=10)
frame_note.pack(fill=tk.X)

#送出frame
frame_btn = tk.Frame(root, pady=10, padx=10)
frame_btn.pack()

root.resizable(False, True) 

input_count = tk.IntVar(value=0)

menu = Menu(root)
root.config(menu=menu)

# submenu1 = Menu(activebackground="black", activeborderwidth=10, borderwidth=20)
# menu.add_cascade(label="Option", menu=submenu1)

# submenu1.add_command(label="label1")
# submenu1.add_separator()
# submenu1.add_command(label="label2")

submenu2 = Menu()
menu.add_cascade(label="Analysis", menu=submenu2)
#submenu2.add_command(label="Run Process", command=process_data , accelerator="Command+R")
submenu2.add_command(label="Run Process", command=process_data)
#, command=process_data

submenu3 = Menu()
menu.add_cascade(label="About", menu=submenu3)
submenu3.add_command(label="Version", command=version_dialog)

#root.bind_all("<Command-r>", process_data)

#root.configure(bg='white')  # 設定視窗的背景顏色為藍色
root.title(f"Data Analysis Tool - V {gui_version}")

""" 
frame1 = tk.Frame(root, pady=10, padx=10, bg='#f90')   # 第一個 Frame 元件
frame2 = tk.Frame(root, pady=10, padx=10, bg='#09c')
frame1.grid(row=29, column=0,ipadx=10, sticky=tk.NW) """

label_title = tk.Label(frame_title, text=f"此程式為專們用來處理.4ch格式之資料格式，請於下方輸入相關必備的資訊\n程式版本編號：V{gui_version}\n編譯日期：{relase_date}",width=width_title*3, anchor="w", justify="left")
label_title.grid(row=0, column=0, columnspan=2, sticky=tk.NW)
tk.Button(frame_title,width=width_range, height=2, text="Process Data", command=process_data).grid(row=0, column=3 ,sticky=tk.E)


""" c """

""" label = tk.Label(frame, text="",width=width_title,anchor="w")
label.grid(row=2, column=0, ipadx=10, sticky=tk.NW)
# Configure background color after creating the Label
label.config(bg="lightblue")
#tk.Label(frame, text="",width=width_title,anchor="w").grid(row=2, column=0)  # This adds some space between sections
tk.Button(frame, text="Select Files", command=select_files).grid(row=2, column=3, columnspan=3, sticky=tk.NE)

 """



label_file_input = tk.Label(frame, text=f"File Input( {input_count.get()} ):", width=width_title, anchor="w")
label_file_input.grid(row=0, column=0, sticky=tk.NW)
entry_filename = tk.Listbox(frame, width=width_text, height=10)
entry_filename.grid(row=0, column=1, columnspan=3, sticky=tk.NW)


# Bind mouse events for drag-and-drop
entry_filename.bind('<ButtonPress-1>', on_drag_start)
entry_filename.bind('<B1-Motion>', on_drag_motion)
entry_filename.bind('<ButtonRelease-1>', on_drag_end)

# 绑定 Delete 键到 Listbox 的 remove_file 函数
entry_filename.bind('<Delete>', remove_file)
entry_filename.bind('<BackSpace>', remove_file)

# 添加文件按钮
button_select_file = tk.Button(frame, text="Select Files",width=width_range, command=select_files)
button_select_file.grid(row=1, column=3, columnspan=3, sticky=tk.NE , pady=10, padx=10)



label = tk.Label(frame, text="Filepath:", width=width_title,anchor="w")
label.grid(row=2, column=0, sticky=tk.NW)
# Configure background color after creating the Label
#label.config(bg="lightblue")
#tk.Label(frame, text="Filepath:").grid(row=0, column=0, sticky=tk.NW)
# entry_filepath_prefix = tk.Entry(frame, width=width_text)
# entry_filepath_prefix.grid(row=0, column=1, columnspan=3, sticky=tk.NW)

entry_filepath_prefix = tk.Label(frame, text="", width=width_text,anchor="w")
entry_filepath_prefix.grid(row=2, column=1, columnspan=3, sticky=tk.NW)


""" 
tk.Label(frame_label, text="Display Label:", width=width_title,anchor="w").grid(row=3, column=0, sticky=tk.NW)


label_data_set = tk.Label(frame_label, text="[0]Data_set", width=width_range,anchor="w")
label_data_set.grid(row=0, column=1, sticky=tk.NW)
entry_display_label = tk.Entry(frame_label, width=width_range*2)
entry_display_label.grid(row=0, column=2, columnspan=2, sticky=tk.NW)

 """
tk.Label(frame_sub, text="Input V:", width=width_title,anchor="w").grid(row=4, column=0, sticky=tk.NW)
# entry_input_v = tk.Entry(frame_sub, width=width_text)
# entry_input_v.grid(row=4, column=1, columnspan=3, sticky=tk.NW)
entry_input_v = tk.Spinbox(frame_sub, from_=0, to=20 , width=width_range, format='%6.2f', increment=0.01)
entry_input_v.grid(row=4, column=1, columnspan=3, sticky=tk.NW)
entry_input_v.delete(0, 'end')
entry_input_v.insert(0, 0.00)

tk.Label(frame_sub, text="Input A:", width=width_title,anchor="w").grid(row=5, column=0, sticky=tk.NW)
# entry_input_a = tk.Entry(frame_sub, width=width_text)
# entry_input_a.grid(row=5, column=1, columnspan=3, sticky=tk.NW)
entry_input_a = tk.Spinbox(frame_sub, from_=0, to=5 , width=width_range, format='%6.2f', increment=0.01)
entry_input_a.grid(row=5, column=1, columnspan=3, sticky=tk.NW)
entry_input_a.delete(0, 'end')
entry_input_a.insert(0, 0.00)

""" 
tk.Label(frame_sub, text="Average Start:", width=width_title,anchor="w").grid(row=6, column=0, sticky=tk.NW)

entry_sample_start = tk.Spinbox(frame_sub, from_=0, to=99999 , width=width_range)
entry_sample_start.grid(row=6, column=1, columnspan=3, sticky=tk.NW)
entry_sample_start.delete(0, 'end')
entry_sample_start.insert(0, 20)
# entry_sample_start = tk.Entry(frame_sub, width=width_text)
# entry_sample_start.grid(row=6, column=1, columnspan=3, sticky=tk.NW)


tk.Label(frame_sub, text="Average End:", width=width_title,anchor="w").grid(row=7, column=0, sticky=tk.NW)
entry_sample_end = tk.Spinbox(frame_sub, from_=0, to=99999 , width=width_range)
entry_sample_end.grid(row=7, column=1, columnspan=3, sticky=tk.NW)
entry_sample_end.delete(0, 'end')
entry_sample_end.insert(0, 100)
# entry_sample_end = tk.Entry(frame_sub, width=width_text)
# entry_sample_end.grid(row=7, column=1, columnspan=3, sticky=tk.NW)


 """

tk.Label(frame_sub, text="Average Range:", width=width_title,anchor="w").grid(row=6, column=0, sticky=tk.NW)
entry_sample_start = tk.Spinbox(frame_sub, from_=0, to=99999 , width=width_range)
entry_sample_start.grid(row=6, column=1,sticky=tk.NW)
entry_sample_average_tail = tk.Label(frame_sub, width=width_range_tail, text="~")
entry_sample_average_tail.grid(row=6, column=2, sticky=tk.NW)
entry_sample_end = tk.Spinbox(frame_sub, from_=0, to=99999 , width=width_range)
entry_sample_end.grid(row=6, column=3,  sticky=tk.NW)

entry_sample_start.delete(0, 'end')
entry_sample_start.insert(0, 20)
entry_sample_end.delete(0, 'end')
entry_sample_end.insert(0, 100)



tk.Label(frame_sub, text="Get Column Set:", width=width_title,anchor="w").grid(row=8, column=0, sticky=tk.NW)
tk.Label(frame_sub, text="Select the channel which you want to use:", width=width_text,anchor="w").grid(row=9, column=1, columnspan=3, sticky=tk.NW)

var_channel_select_1 = tk.BooleanVar(value=True)
var_channel_select_2 = tk.BooleanVar()
var_channel_select_3 = tk.BooleanVar()
var_channel_select_4 = tk.BooleanVar()

tk.Checkbutton(frame_sub, text="Channel 1", variable=var_channel_select_1, command=lambda: show_hide_entry(0)).grid(row=10, column=1, sticky=tk.NW)
tk.Checkbutton(frame_sub, text="Channel 2", variable=var_channel_select_2, command=lambda: show_hide_entry(1)).grid(row=11, column=1, sticky=tk.NW)
tk.Checkbutton(frame_sub, text="Channel 3", variable=var_channel_select_3, command=lambda: show_hide_entry(2)).grid(row=12, column=1, sticky=tk.NW)
tk.Checkbutton(frame_sub, text="Channel 4", variable=var_channel_select_4, command=lambda: show_hide_entry(3)).grid(row=13, column=1, sticky=tk.NW)

var_average_0 = tk.StringVar()
var_average_1 = tk.StringVar()
var_average_2 = tk.StringVar()
var_average_3 = tk.StringVar()

tk.Label(frame_sub, textvariable=var_average_0).grid(row=10, column=3, sticky=tk.NW)
tk.Label(frame_sub, textvariable=var_average_1).grid(row=11, column=3, sticky=tk.NW)
tk.Label(frame_sub, textvariable=var_average_2).grid(row=12, column=3, sticky=tk.NW)
tk.Label(frame_sub, textvariable=var_average_3).grid(row=13, column=3, sticky=tk.NW)

label_temp_range_0 = tk.Label(frame_sub, text="Temperature Range Channel 1:", width=width_title,anchor="w")
label_temp_range_1 = tk.Label(frame_sub, text="Temperature Range Channel 2:", width=width_title,anchor="w")
label_temp_range_2 = tk.Label(frame_sub, text="Temperature Range Channel 3:", width=width_title,anchor="w")
label_temp_range_3 = tk.Label(frame_sub, text="Temperature Range Channel 4:", width=width_title,anchor="w")

label_temp_range_0_tail = tk.Label(frame_sub, width=width_range_tail, text="~")
label_temp_range_1_tail = tk.Label(frame_sub, width=width_range_tail, text="~")
label_temp_range_2_tail = tk.Label(frame_sub, width=width_range_tail, text="~")
label_temp_range_3_tail = tk.Label(frame_sub, width=width_range_tail, text="~")

# label_temp_range_0_tail.config(bg="lightblue")
# label_temp_range_1_tail.config(bg="lightblue")
# label_temp_range_2_tail.config(bg="lightblue")
# label_temp_range_3_tail.config(bg="lightblue")

# entry_temp_range_0_min = tk.Entry(frame_sub, width=width_range)
# entry_temp_range_0_max = tk.Entry(frame_sub, width=width_range)
# entry_temp_range_1_min = tk.Entry(frame_sub, width=width_range)
# entry_temp_range_1_max = tk.Entry(frame_sub, width=width_range)
# entry_temp_range_2_min = tk.Entry(frame_sub, width=width_range)
# entry_temp_range_2_max = tk.Entry(frame_sub, width=width_range)
# entry_temp_range_3_min = tk.Entry(frame_sub, width=width_range)
# entry_temp_range_3_max = tk.Entry(frame_sub, width=width_range)

vcmd = (frame_sub.register(on_spinbox_validate(minval, maxval)), '%P')

entry_temp_range_0_min = tk.Spinbox(frame_sub, from_=minval, to=maxval, width=width_range, validate='key', validatecommand=vcmd)
entry_temp_range_0_max = tk.Spinbox(frame_sub, from_=minval, to=maxval, width=width_range, validate='key', validatecommand=vcmd)
entry_temp_range_1_min = tk.Spinbox(frame_sub, from_=minval, to=maxval, width=width_range, validate='key', validatecommand=vcmd)
entry_temp_range_1_max = tk.Spinbox(frame_sub, from_=minval, to=maxval, width=width_range, validate='key', validatecommand=vcmd)
entry_temp_range_2_min = tk.Spinbox(frame_sub, from_=minval, to=maxval, width=width_range, validate='key', validatecommand=vcmd)
entry_temp_range_2_max = tk.Spinbox(frame_sub, from_=minval, to=maxval, width=width_range, validate='key', validatecommand=vcmd)
entry_temp_range_3_min = tk.Spinbox(frame_sub, from_=minval, to=maxval, width=width_range, validate='key', validatecommand=vcmd)
entry_temp_range_3_max = tk.Spinbox(frame_sub, from_=minval, to=maxval, width=width_range, validate='key', validatecommand=vcmd)

entry_temp_range_0_min.delete(0, 'end')
entry_temp_range_0_min.insert(0, 0)
entry_temp_range_0_max.delete(0, 'end')
entry_temp_range_0_max.insert(0, 90)
entry_temp_range_1_min.delete(0, 'end')
entry_temp_range_1_min.insert(0, 0)
entry_temp_range_1_max.delete(0, 'end')
entry_temp_range_1_max.insert(0, 90)
entry_temp_range_2_min.delete(0, 'end')
entry_temp_range_2_min.insert(0, 0)
entry_temp_range_2_max.delete(0, 'end')
entry_temp_range_2_max.insert(0, 90)
entry_temp_range_3_min.delete(0, 'end')
entry_temp_range_3_min.insert(0, 0)
entry_temp_range_3_max.delete(0, 'end')
entry_temp_range_3_max.insert(0, 90)

entry_temp_range_0_min.grid(row=0, column=1)
entry_temp_range_0_max.grid(row=0, column=2)
entry_temp_range_1_min.grid(row=1, column=1)
entry_temp_range_1_max.grid(row=1, column=2)
entry_temp_range_2_min.grid(row=2, column=1)
entry_temp_range_2_max.grid(row=2, column=2)
entry_temp_range_3_min.grid(row=3, column=1)
entry_temp_range_3_max.grid(row=3, column=2)

tk.Label(frame_sub, text="File Title:", width=width_title,anchor="w").grid(row=20, column=0, sticky=tk.NW)
entry_file_title = tk.Entry(frame_sub, width=width_text)
entry_file_title.grid(row=20, column=1, columnspan=3,sticky=tk.NW)
entry_file_title.insert(0,"data")

tk.Label(frame_sub, text="Image Title:", width=width_title,anchor="w").grid(row=21, column=0, sticky=tk.NW)
entry_img_title = tk.Entry(frame_sub, width=width_text)
entry_img_title.grid(row=21, column=1, columnspan=3,sticky=tk.NW)
entry_img_title.insert(0,"img")


tk.Label(frame_sub, text="Output File Type:", width=width_title,anchor="w").grid(row=22, column=0, sticky=tk.NW)
entry_output_file_type = ttk.Combobox(frame_sub, values=['png','jpg'], )
entry_output_file_type.grid(row=22, column=1, columnspan=3,sticky=tk.NW)
entry_output_file_type.set('png')






var_output_image = tk.BooleanVar()
tk.Label(frame_option, text="Image Output Engine", width=width_title,anchor="w").grid(row=0, column=0, sticky=tk.NW)
tk.Checkbutton(frame_option, text="Active", variable=var_output_image).grid(row=0, column=1, sticky=tk.NW)

tk.Label(frame_option, text="", width=width_title,anchor="w").grid(row=0, column=2, sticky=tk.NW)
var_func_smooth = tk.BooleanVar()
tk.Label(frame_option, text="Smooth Function", width=width_title,anchor="w").grid(row=0, column=3, sticky=tk.NW)
tk.Checkbutton(frame_option, text="Active", variable=var_func_smooth).grid(row=0, column=4, sticky=tk.NW)

var_gnuplot_support = tk.BooleanVar()
tk.Label(frame_option, text="Gnuplot Support", width=width_title,anchor="w").grid(row=1, column=0, sticky=tk.NW)
tk.Checkbutton(frame_option, text="Active", variable=var_gnuplot_support).grid(row=1, column=1, sticky=tk.NW)

tk.Label(frame_option, text="", width=width_title,anchor="w").grid(row=1, column=2, sticky=tk.NW)
var_shfit_to_zero = tk.BooleanVar()
tk.Label(frame_option, text="Shift to Zero", width=width_title,anchor="w").grid(row=1, column=3, sticky=tk.NW)
tk.Checkbutton(frame_option, text="Active", variable=var_shfit_to_zero).grid(row=1, column=4, sticky=tk.NW)

var_output_csv = tk.BooleanVar()
tk.Label(frame_option, text="Output CSV", width=width_title,anchor="w").grid(row=2, column=0, sticky=tk.NW)
tk.Checkbutton(frame_option, text="Active", variable=var_output_csv).grid(row=2, column=1, sticky=tk.NW)

tk.Label(frame_option, text="", width=width_title,anchor="w").grid(row=2, column=2, sticky=tk.NW)
var_output_excel = tk.BooleanVar()
tk.Label(frame_option, text="Output Excel", width=width_title,anchor="w").grid(row=2, column=3, sticky=tk.NW)
tk.Checkbutton(frame_option, text="Active", variable=var_output_excel).grid(row=2, column=4, sticky=tk.NW)


var_output_result_box = tk.BooleanVar()
tk.Label(frame_option, text="Show Summary", width=width_title,anchor="w").grid(row=3, column=0, sticky=tk.NW)
tk.Checkbutton(frame_option, text="Active", variable=var_output_result_box).grid(row=3, column=1, sticky=tk.NW)


var_output_title_power = tk.BooleanVar()
tk.Label(frame_option, text="Image Title with Power", width=width_title,anchor="w").grid(row=3, column=3, sticky=tk.NW)
tk.Checkbutton(frame_option, text="Active", variable=var_output_title_power).grid(row=3, column=4, sticky=tk.NW)




var_output_time_set = tk.BooleanVar()
tk.Label(frame_option, text="Image Time Range", width=width_title,anchor="w").grid(row=22, column=0, sticky=tk.NW)
tk.Checkbutton(frame_option, text="Active", variable=var_output_time_set, command=lambda: show_hide_time_range(0)).grid(row=22, column=1, sticky=tk.NW)

label_time_range = tk.Label(frame_option_time_range, text="Image Output Range:", width=width_title,anchor="w")
range_output_start = tk.Spinbox(frame_option_time_range, from_=0, to=99999 , width=width_range)
range_output_start.grid(row=23, column=1,sticky=tk.NW)
range_output_tail = tk.Label(frame_option_time_range, width=width_range_tail, text="-")
range_output_tail.grid(row=23, column=2, sticky=tk.NW)
range_output_end = tk.Spinbox(frame_option_time_range, from_=0, to=99999 , width=width_range)
range_output_end.grid(row=23, column=3,  sticky=tk.NW)

range_output_start.delete(0, 'end')
range_output_start.insert(0, 00)
range_output_end.delete(0, 'end')
range_output_end.insert(0, 100)


tk.Label(frame_note, text="Note:", anchor="w", width=width_title*4).grid(row=0, column=0, sticky=tk.NW)
# 正確初始化 Text 小部件
vat_textarea_input = tk.Text(frame_note, height=20, width=width_title*4, bd=1)
vat_textarea_input.grid(row=1, column=0, sticky=tk.NW)
tk.Label(frame_note, text="You can write the experiment information here as note", font=('Arial',12,'italic') ,anchor="w" , width = width_title*4).grid(row=2, column=0, sticky=tk.NW)

# tk.Label(frame_option, text="", width=width_title,anchor="w").grid(row=0, column=2, sticky=tk.NW)
# var_func_smooth = tk.BooleanVar()
# tk.Label(frame_option, text="Smooth Function:", width=width_title,anchor="w").grid(row=0, column=3, sticky=tk.NW)
# tk.Checkbutton(frame_option, text="Active", variable=var_func_smooth).grid(row=0, column=4, sticky=tk.NW)

#tk.Button(frame_btn, text="Process Data", command=process_data).grid(row=0, column=0)



reset_hide_entry(-1)
reset_hide_time_range(-1)

show_hide_entry(0)
root.mainloop()
