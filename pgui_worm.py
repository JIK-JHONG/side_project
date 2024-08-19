import tkinter as tk
from tkinter import filedialog, messagebox, Menu , ttk, Text
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time


def keyword_filter_set(keywords):
    if len(keywords)>0:
        use_filter = True 
        print(f"啟動關鍵字搜尋：{keywords}")
    else:
        use_filter = False
    return use_filter

def initialize_function(input_id,input_set):
    if input_id == 'deep_analysis':
        print(f"文章關鍵字搜尋：{input_set}")
    elif input_id == 'push_filter':
         print(f"推文排除：{input_set}")
    elif input_id == 'target_ptt':
         print(f"看板：{input_set}")
    elif input_id == 'output_csv':
         print(f"建立 csv ：{input_set}")
    elif input_id == 'output_xlsx':
         print(f"建立 xlsx ：{input_set}")


def get_titles_from_page(url, session, deep_analysis, push_filter, output_csv, output_xlsx,page_count, use_filter=False, keywords=None):
    global total_data_count  # 使用 global 關鍵字聲明全局變量
    global start_time
    global data
   

    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all('div', class_='title')
        titles_detail = soup.find_all('div', class_='meta')
        titles_rank = soup.find_all('div', class_='nrec')
        
        for title, detail, rank in zip(titles, titles_detail, titles_rank):
            a_tag = title.find('a')
            if rank.span:
                main_rank = rank.span.text
            else:
                main_rank = "-"
            
            
            #print(main_rank)
            if a_tag:
                main_title = a_tag.text.strip()
                main_link = a_tag['href']
               
                main_time = detail.find('div', class_='date')
                
                if main_time:
                    time_str = main_time.text.strip()
                    try:
                        time_obj = datetime.strptime(time_str, '%m/%d')
                        time_formatted = time_obj.strftime('%m-%d')
                    except ValueError:
                        time_formatted = 'Unknown'
                else:
                    time_formatted = 'Unknown'

                # 格式化輸出，固定每行顯示的格式
                #print(f"{main_title:<40} @ {time_formatted:<30}")




                # 獲取文章內容
                if deep_analysis:
                    article_url = 'https://www.ptt.cc' + main_link
                    article_response = session.get(article_url)
                    if article_response.status_code == 200:
                        article_soup = BeautifulSoup(article_response.text, 'html.parser')
                        article_content = article_soup.find('div', id='main-content').text
                        
                        # 檢查文章是否為主題文章（不包含回文、推文等）
                        if push_filter:
                            if is_main_post(article_soup):
                                # 檢查文章內容是否包含關鍵字
                                contains_keyword = any(keyword in article_content for keyword in keywords)
                                if use_filter and not contains_keyword:
                                    continue  # 如果文章不包含任何關鍵字，跳過此項目

                                # 格式化輸出，固定每行顯示的格式
                                print(f"[{total_data_count:3^}] [{main_rank:^4}] {main_title:<40} @ {time_formatted:>30}")
                                data.append([main_title, 'https://www.ptt.cc' + main_link, time_formatted, main_rank])
                                total_data_count += 1  # 每成功抓取一筆資料，計數器加一
                        else:
                            # 檢查文章內容是否包含關鍵字
                            contains_keyword = any(keyword in article_content for keyword in keywords)
                            if use_filter and not contains_keyword:
                                continue  # 如果文章不包含任何關鍵字，跳過此項目

                            # 格式化輸出，固定每行顯示的格式
                            print(f"[{total_data_count:3^}] [{main_rank:^4}] {main_title:<40} @ {time_formatted:>30}")
                            data.append([main_title, 'https://www.ptt.cc' + main_link, time_formatted, main_rank])
                            total_data_count += 1  # 每成功抓取一筆資料，計數器加一

                else:
                    # 過濾功能
                    if use_filter and keywords:
                        if not any(keyword in main_title for keyword in keywords):        
                                            
                            continue  # 如果標題不包含任何關鍵字，跳過此項目
                        else:
                            print(f"[{total_data_count:3^}] [{main_rank:^4}] {main_title:<40} @ {time_formatted:>30}")
                    else:
                        print(f"[{total_data_count:3^}] [{main_rank:^4}] {main_title:<40} @ {time_formatted:>30}")
                    data.append([main_title, 'https://www.ptt.cc' + main_link, time_formatted, main_rank])
                    total_data_count += 1  # 每成功抓取一筆資料，計數器加一
                
        # 找到 "上一頁" 的連結
        next_page = soup.find('a', string='‹ 上頁')
        if next_page:
            return next_page['href']
    return None

def is_main_post(article_soup):
    """判斷文章是否為主題文章（非回文、推文等）"""
    # 這裡可以根據PTT文章的HTML結構來判斷是否為主題文章
    # 例如，檢查是否有特定的標籤或類別來區分主題文章和回文、推文等
    # 以下是一個示例，請根據實際情況修改
    article_meta = article_soup.find('div', class_='push')
    if article_meta:
        return True
    else:
        return False
# 目標URL

def switch_to_basic_output(frame_id):
    notebook.select(frame_id)  # 切換到 basic_output 標籤頁


def on_item_click(event):
    """處理 Treeview 行的點擊事件，複製網址到剪貼板"""
    selected_item = result_box_content.selection()[0]  # 獲取選中的項目
    url = result_box_content.item(selected_item, 'values')[2]  # 獲取網址列的值
    if url:
        root.clipboard_clear()  # 清空剪貼板
        root.clipboard_append(url)  # 將網址複製到剪貼板
        root.update()  # 更新剪貼板
        print(f"複製到剪貼板: {url}")


def close_msg_box():
    version_box.destroy()
def version_dialog():
    global version_box
    version_box = tk.Tk()
    version_box.title('軟體版本資訊')
    #version_box.geometry('500x250')
    version_box_title = tk.Frame(version_box, pady=10, padx=10)
    version_box_title.pack(fill=tk.X)
    version_box_msg_0 = tk.Label(version_box_title, text=f"PTT 爬蟲囉！",font=('Arial',20,'bold'), pady=10, padx=0)
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


def run_rip():
    global result_time
    global result_data
    global result_key
    global result_df

    print("Running run_rip...")

    start_time = time.time()
    deep_analysis = var_deep_analysis.get()
    push_filter = var_push_filter.get()
    result_time.set("處理中，請稍後...")
    result_data.set("處理中，請稍後...")
    result_key.set("處理中，請稍後...")

    keywords = []
    if board_title.get():
        keywords.append(board_title.get())
    if board_title2.get():
        keywords.append(board_title2.get())
    if board_title3.get():
        keywords.append(board_title3.get())

    output_csv = var_output_csv.get()
    output_xlsx = var_output_xlsx.get()
    page_count = int(var_page_set_range.get())  
    board_select = var_board_select.get()

    use_filter = keyword_filter_set(keywords)

    initialize_function('deep_analysis', deep_analysis)
    if deep_analysis:    
        initialize_function('push_filter', push_filter)
    initialize_function('target_ptt', board_select)
    initialize_function('output_csv', output_csv)
    initialize_function('output_xlsx', output_xlsx)

    base_url = 'https://www.ptt.cc'
    start_url = f'{base_url}/bbs/{board_select}/index.html'

    session = requests.Session()
    session.cookies.set('over18', '1')

    current_url = start_url
    global total_data_count
    total_data_count = 0  # Reset the counter
    
    # 清空現有的數據
    result_box_content.delete(*result_box_content.get_children())
    
    data.clear()  # 清空數據
    for _ in range(page_count):
        next_page = get_titles_from_page(current_url, session, deep_analysis, push_filter, output_csv, output_xlsx, page_count, use_filter, keywords)
        if next_page:
            current_url = base_url + next_page
        else:
            break

    # 將資料轉換成 DataFrame
    if (output_csv or output_xlsx):
        date_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        df = pd.DataFrame(data, columns=['標題', '網址', '時間', '人氣'])
        if output_csv:
            df.to_csv(f'ptt_{board_select}_{date_time}_news.csv', index=False, encoding='utf-8')
            print(f"資料已儲存成 ptt_{board_select}_{date_time}_news.csv")
        if output_xlsx:
            df.to_excel(f'ptt_{board_select}_{date_time}_news.xlsx', index=False)
            print(f"資料已儲存成 ptt_{board_select}_{date_time}_news.xlsx")
    
    result_df = pd.DataFrame(data, columns=['標題', '網址', '時間', '人氣'])
    # print(f"DataFrame content: {result_df.head()}")

    # 設定 Treeview 的列
    result_box_content["columns"] = ('序列', '標題', '網址', '時間', '人氣')

    result_box_content.heading('序列', text='序列')
    result_box_content.heading('標題', text='標題')
    result_box_content.heading('網址', text='網址')
    result_box_content.heading('時間', text='時間')
    result_box_content.heading('人氣', text='人氣')

    result_box_content.column('#0', width=0)
    result_box_content.column('序列', width=50, anchor='center')
    result_box_content.column('標題', width=400, anchor='w')
    result_box_content.column('網址', width=100, anchor='w')
    result_box_content.column('時間', width=80, anchor='center')
    result_box_content.column('人氣', width=50, anchor='center')

    # 插入 DataFrame 中的數據到 Treeview
    for index, row in result_df.iterrows():
        result_box_content.insert('', 'end', values=(index + 1, row['標題'], row['網址'], row['時間'], row['人氣']))
    switch_to_basic_output(basic_result)
    
    end_time = time.time()
    execution_time = end_time - start_time
    result_time.set(f"{execution_time:.2f}秒")
    result_data.set(f"{total_data_count} 筆 資料 / 共計爬 {page_count} 頁")
    result_key.set(f"{[keywords[i] for i in range(len(keywords))]}")
    print(f"page_count = {page_count:>10} pages")
    print(f"total_data_collect = {total_data_count:>10} datas")
    print(f"Execution time = {execution_time:>6.2f} sec")



gui_version = '1.0.0'
relase_date = '2024/08/19'


result_df = []
data = []
total_data_count = 0  # 用來計算總共抓取的資料量
width_range = 20
width_range_tail = 10
width_text = 50
width_title = 20

root = tk.Tk()
root.title(f"PTT 爬蟲囉！")

menu = Menu(root)
root.config(menu=menu)
submenu2 = Menu()
menu.add_cascade(label="About", menu=submenu2)
submenu2.add_command(label="Version", command=version_dialog)


style = ttk.Style()
style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 12))
notebook = ttk.Notebook(root, style='TNotebook')
notebook.pack(expand=True, fill='both')

basic_frame = ttk.Frame(notebook)
basic_output = ttk.Frame(notebook)
basic_result = ttk.Frame(notebook)
notebook.add(basic_frame, text='基礎設定')
notebook.add(basic_output, text='輸出設定')
notebook.add(basic_result, text='爬蟲結果')

frame_title = tk.Frame(basic_frame, pady=10, padx=10)
frame_title.pack(fill=tk.X)

output_setting = tk.Frame(basic_output, pady=10, padx=10)
output_setting.pack(fill=tk.X)

output_result = tk.Frame(basic_result, pady=10, padx=10)
output_result.pack(fill=tk.X)

output_result_msg = tk.Frame(basic_result, pady=10, padx=10)
output_result_msg.pack(fill=tk.X)

frame_main = tk.Frame(basic_frame, pady=10, padx=10)
frame_main.pack(fill=tk.X)

frame_label = tk.Frame(basic_frame, pady=10, padx=10)
frame_label.pack(fill=tk.X)

label_title = tk.Label(frame_title, text=f"PTT爬蟲應用程式", font=('Arial', 14, 'bold'), pady=10, padx=0, width=width_title*3, anchor="w", justify="left")
label_title.grid(row=0, column=0, columnspan=2, sticky=tk.NW)

root.resizable(False, True)

tk.Label(frame_main, text="關鍵字:", width=width_title, anchor="w").grid(row=1, column=0, sticky=tk.NW, rowspan=3)
board_title = tk.Entry(frame_main, width=width_text)
board_title.grid(row=1, column=1, columnspan=3, sticky=tk.NW)
board_title.insert(0, "")
board_title2 = tk.Entry(frame_main, width=width_text)
board_title2.grid(row=2, column=1, columnspan=3, sticky=tk.NW)
board_title2.insert(0, "")
board_title3 = tk.Entry(frame_main, width=width_text)
board_title3.grid(row=3, column=1, columnspan=3, sticky=tk.NW)
board_title3.insert(0, "")

list_id_set = 1 


var_deep_analysis = tk.BooleanVar(value=False)
tk.Label(frame_main, text="文章內容", width=width_title, anchor="w").grid(row=3+list_id_set, column=0, sticky=tk.NW)
tk.Checkbutton(frame_main, text="啟用", variable=var_deep_analysis).grid(row=3+list_id_set, column=1, columnspan=3, sticky=tk.NW)

var_push_filter = tk.BooleanVar(value=False)
tk.Label(frame_main, text="推文內容", width=width_title, anchor="w").grid(row=4+list_id_set, column=0, sticky=tk.NW)
tk.Checkbutton(frame_main, text="啟用", variable=var_push_filter).grid(row=4+list_id_set, column=1, columnspan=3, sticky=tk.NW)


board_list = ['Gossiping','Stock','iOS','MAC','CVS','LCD','Lifeismoney','Tech_Job','NSwitch','PlayStation','C_Chat']
tk.Label(frame_main, text="看板選擇", width=width_title, anchor="w").grid(row=5+list_id_set, column=0, sticky=tk.NW)
var_board_select = ttk.Combobox(frame_main, values=[board_list[i] for i in range(len(board_list))], )
var_board_select.grid(row=5+list_id_set, column=1, columnspan=3, sticky=tk.NW)
var_board_select.set('Gossiping')


tk.Label(frame_main, text="爬蟲深度（頁面）設定", width=width_title, anchor="w").grid(row=6+list_id_set, column=0, sticky=tk.NW)
var_page_set_range = tk.Spinbox(frame_main, from_=1, to=10, width=width_range)
var_page_set_range.grid(row=6+list_id_set, column=1, sticky=tk.NW)
var_page_set_range.delete(0, 'end')
var_page_set_range.insert(0, 2)



tk.Button(frame_label, pady=2, padx=20, width=width_range, height=2, text="開始爬蟲", command=run_rip).grid(row=10, column=0, sticky=tk.W)


var_output_csv = tk.BooleanVar(value=False)
tk.Label(output_setting, text="輸出為.csv", width=width_title, anchor="w").grid(row=1, column=0, sticky=tk.NW)
tk.Checkbutton(output_setting, text="啟用", variable=var_output_csv).grid(row=1, column=1, columnspan=3, sticky=tk.NW)

var_output_xlsx = tk.BooleanVar(value=False)
tk.Label(output_setting, text="輸出為.xlsx", width=width_title, anchor="w").grid(row=2, column=0, sticky=tk.NW)
tk.Checkbutton(output_setting, text="啟用", variable=var_output_xlsx).grid(row=2, column=1, columnspan=3, sticky=tk.NW)

result_box_content = ttk.Treeview(output_result)
result_box_content.bind('<ButtonRelease-1>', on_item_click)

result_box_content.pack(fill=tk.BOTH, expand=True)

result_key = tk.StringVar()  # Changed from string to StringVar
result_key.set("目前無任務")
tk.Label(output_result_msg, text="關鍵字", font=('Arial', 12) , width=width_title, anchor="w").grid(row=9, column=0, sticky=tk.NW)
tk.Label(output_result_msg, textvariable=result_key, font=('Arial', 12), width=width_title, anchor="w").grid(row=9, column=2, sticky=tk.NW)

result_data = tk.StringVar()  # Changed from string to StringVar
result_data.set("目前無任務")
tk.Label(output_result_msg, text="本次爬蟲數量", font=('Arial', 12) , width=width_title, anchor="w").grid(row=10, column=0, sticky=tk.NW)
tk.Label(output_result_msg, textvariable=result_data, font=('Arial', 12), width=width_title, anchor="w").grid(row=10, column=2, sticky=tk.NW)

result_time = tk.StringVar()  # Changed from string to StringVar
result_time.set("目前無任務")

tk.Label(output_result_msg, text="本次爬蟲處理時間", font=('Arial', 12) , width=width_title, anchor="w").grid(row=11, column=0, sticky=tk.NW)
tk.Label(output_result_msg, textvariable=result_time, font=('Arial', 12), width=width_title, anchor="w").grid(row=11, column=2, sticky=tk.NW)



root.mainloop()