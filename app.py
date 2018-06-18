import tkinter as tk
from tkinter import filedialog
import os
import cleanxlsx as cleaner
root = tk.Tk()
filename = ''

selected_file_label = None
selected_file_name = None

get_file_label = None
get_file_btn = None

name_col_box = None
to_join = False
email_col_box = None
number_col_box = None
address_col_box = None


def clean_sheet():
    global filename
    global email_col_box
    global to_join
    global name_col_box
    global address_col_box

    print(email_col_box.get())
    print(name_col_box.get())

    process_label = tk.Label(root, text='Processing..')
    process_label.grid(row=7, column=1)

    result = cleaner.start_cleaning(filename, {
        'Name': name_col_box.get(),
        'Email': email_col_box.get(),
        'Number': number_col_box.get(),
        'Address': address_col_box.get(),
        'To_Join': to_join
    })

    if result['status']:
        srt_tos = 'Found: ' + str(result['email_verified']) +\
                  ', Bounced: ' + str(result['email_bounced']) +\
                  ', Error: ' + str(result['email_error'])
    else:
        srt_tos = 'Error: ' + str(result['error'])
    process_label.config(text=srt_tos)


def display_filename(f_name):
    global get_file_btn
    global get_file_label

    global selected_file_name
    global selected_file_label

    if get_file_btn is not None:
        print('ok')
        get_file_label.grid_forget()
        get_file_btn.grid_forget()
        get_file_label = None
        get_file_btn = None

    selected_file_label = tk.Label(root, text='Selected File:', anchor='w')
    selected_file_label.grid(row=1, column=1)

    selected_file_name = tk.Label(root, text=os.path.basename(f_name))
    selected_file_name.grid(row=1, column=2)


def add_select_file_btn():
    global get_file_btn
    global get_file_label

    global selected_file_label
    global selected_file_name

    if selected_file_name is not None:
        selected_file_name.grid_forget()
        selected_file_label.grid_forget()
        selected_file_name = None
        selected_file_label = None

    get_file_label = tk.Label(root, text='Select File:', anchor='w')
    get_file_label.grid(row=1, column=1)
    get_file_btn = tk.Button(root, text='Select File', command=select_file_dialog)
    get_file_btn.grid(row=1, column=2)


def add_blank_row(row):
    blank_label_to_add = tk.Label(root, text='')
    blank_label_to_add.grid(row=row, column=1, columnspan=2)


def select_file_dialog():
    global filename
    filename = tk.filedialog.askopenfilename(title="Select File")
    if not filename == '':
        display_filename(filename)


def toggle_check():
    print('Toogle')
    global to_join

    to_join = not to_join


def show_ui():
    global name_col_box
    global join_check
    global email_col_box
    global number_col_box
    global address_col_box

    # Select file btn
    add_select_file_btn()

    # Name Column
    name_col_label = tk.Label(root, text='Name Column:', anchor='w')
    name_col_label.grid(row=2, column=1)

    name_col_box = tk.Entry(root)
    name_col_box.grid(row=2, column=2)
    name_col_box.insert(0, 'Name')

    # checkbox
    join_check = tk.Checkbutton(root, text="Join Cols", command=toggle_check)
    join_check.grid(row=3, column=1)

    # Email Column
    email_col_label = tk.Label(root, text='Email Column:', anchor='w')
    email_col_label.grid(row=4, column=1)

    email_col_box = tk.Entry(root)
    email_col_box.grid(row=4, column=2)
    email_col_box.insert(0, 'Email')

    # Number Column
    number_col_label = tk.Label(root, text='Number Column:', anchor='w')
    number_col_label.grid(row=5, column=1)

    number_col_box = tk.Entry(root)
    number_col_box.grid(row=5, column=2)
    number_col_box.insert(0, 'Number')

    # Address Column
    address_col_label = tk.Label(root, text='Address Column:', anchor='w')
    address_col_label.grid(row=6, column=1)

    address_col_box = tk.Entry(root)
    address_col_box.grid(row=6, column=2)
    address_col_box.insert(0, 'Address')

    add_blank_row(7)

    # Reset btn
    reset_btn = tk.Button(root, text='Reset All', command=show_ui)
    reset_btn.grid(row=8, column=1)

    # Get Verified Emails btn
    get_verified_btn = tk.Button(root, text='Clean Sheet', command=clean_sheet)
    get_verified_btn.grid(row=8, column=2)


show_ui()

root.mainloop()
