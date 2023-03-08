from copyreg import pickle
from tkinter import *
from tkinter import ttk
from PIL import *
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox

window = Tk()
window.title("Employee Database")
window.iconbitmap('db.ico')
window.geometry("1300x600")
window.resizable(False, False)


def checkCreateTables():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    employeesTable = """ CREATE TABLE IF NOT EXISTS employees (
        [employee_id] INTEGER PRIMARY KEY,
        [name] TEXT NOT NULL,
        [pay] INTEGER,
        [title] TEXT,
        [date_hired] TEXT,
        [description] TEXT,
        [portrait] BLOB)"""
    c.execute(employeesTable)
    conn.commit()
    conn.close()


checkCreateTables()


def donothing():
    pass


style = ttk.Style()

style.theme_use('default')

style.configure("Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3")

style.map("Treeview",
background=[('selected', "#347083")])

lf = LabelFrame(window, relief='raised')

leftFrame = Frame(lf, relief='raised')

tree_scroll = Scrollbar(leftFrame)
tree_scroll.configure(width=16)
tree_scroll.pack(side=RIGHT, fill=Y)

my_tree = ttk.Treeview(leftFrame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack(side=TOP, anchor=NW, fill=BOTH, expand=True)

tree_scroll.config(command=my_tree.yview)

my_tree['columns'] = (" id #", " Name", " Pay", " Title", " Date Hired D-M-Y")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column(" id #", anchor=W, width=35)
my_tree.column(" Name", anchor=W, width=140)
my_tree.column(" Pay", anchor=CENTER, width=85)
my_tree.column(" Title", anchor=CENTER, width=140)
my_tree.column(" Date Hired D-M-Y", anchor=CENTER, width=110)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading(" id #", text=" id #", anchor=W)
my_tree.heading(" Name", text=" Name", anchor=W)
my_tree.heading(" Pay", text=" Pay", anchor=W)
my_tree.heading(" Title", text=" Title", anchor=W)
my_tree.heading(" Date Hired D-M-Y", text=" Date Hired D-M-Y", anchor=W)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background = "white")
my_tree.tag_configure('evenrow', background = "lightblue")

#https://www.youtube.com/watch?v=G9seoA3Mv4Y&t=273s


def query_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM employees")
    data = c.fetchall()
    global count
    count = 0
    for record in data:
        if count % 2 == 0:
            my_tree.insert(parent="", index="end", iid=count, text="", values=(record[0], record[2], record[3], record[4], record[5]), tags = ('evenrow', 'even'))
        else:
            my_tree.insert(parent="", index="end", iid=count, text="", values=(record[0], record[2], record[3], record[4], record[5]), tags = ('oddrow', 'odd'))
        count += 1
    conn.commit()
    conn.close()


data_frame = Frame(lf)#, text="Record"

name_label = Label(data_frame, text=" Name")
name_label.grid(row=0, column=0, padx=10, pady=10)
name_entry = Entry(data_frame)
name_entry.grid(row=0, column=1, padx=10, pady=10)

pay_label = Label(data_frame, text=" Pay")
pay_label.grid(row=0, column=2, padx=10, pady=10)
pay_entry = Entry(data_frame)
pay_entry.grid(row=0, column=3, padx=10, pady=10)

portrait_location_label = Label(data_frame, text=" Portrait File Path")
portrait_location_label.grid(row=0, column=4, padx=10, pady=10)
portrait_location_entry = Entry(data_frame)
portrait_location_entry.grid(row=0, column=5, padx=10, pady=10)

title_label = Label(data_frame, text=" Title")
title_label.grid(row=1, column=0, padx=10, pady=10)
title_entry = Entry(data_frame)
title_entry.grid(row=1, column=1, padx=10, pady=10)

date_hired_label = Label(data_frame, text=" Date Hired D-M-Y")
date_hired_label.grid(row=1, column=2, padx=10, pady=10)
date_hired_entry = Entry(data_frame)
date_hired_entry.grid(row=1, column=3, padx=10, pady=10)

id_label = Label(data_frame, text=" id #")
id_label.grid(row=1, column=4, padx=10, pady=10)
id_entry = Entry(data_frame)
id_entry.grid(row=1, column=5, padx=10, pady=10)

rightFrame = LabelFrame(window, relief=RAISED)


def rf():
    global rightFrame, panel, description_entry
    rightFrame.destroy()
    conn =sqlite3.connect('test.db')
    c = conn.cursor()
    xx = c.execute("SELECT * FROM employees WHERE oid=" + id_entry.get())
    for i in xx:
        path = i[6]
        description = i[5]
        #print(path)
        rightFrame = LabelFrame(window, relief=RAISED)
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(rightFrame, image = img, relief=RAISED)
        description_entry = Entry(rightFrame, relief=RAISED)
        panel.pack(side=TOP, anchor=NW, padx=5, pady=5)
        description_entry.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand=NO, anchor=NW)
        description_entry.insert(0,description)
        rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES)
        window.mainloop()
    c.close()


# Select Record
def select_record(event): # event is the release of left click, bound near window.mainloop()
    # Clear entry boxes
    name_entry.delete(0, END)
    pay_entry.delete(0, END)
    portrait_location_entry.delete(0, END)
    title_entry.delete(0, END)
    date_hired_entry.delete(0, END)
    id_entry.delete(0, END)
    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')
    name_entry.insert(0, values[1])
    pay_entry.insert(0, values[2])
    #portrait_location_entry.insert(0, values[6])
    title_entry.insert(0, values[3])
    date_hired_entry.insert(0, values[4])
    id_entry.insert(0, values[0]) 
    # comments/description @ values[5]
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    xy = c.execute("SELECT * from employees WHERE oid=" + id_entry.get())
    for i in xy:
        print(i)
        path = i[6]
        portrait_location_entry.insert(0, path)
    conn.close()
    rf()


# Clear entry boxes
def clear_entry_boxes():
    # Clear entry boxes
    name_entry.delete(0, END)
    pay_entry.delete(0, END)
    portrait_location_entry.delete(0, END)
    title_entry.delete(0, END)
    date_hired_entry.delete(0, END)
    id_entry.delete(0, END)


def remove_selected():    
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("DELETE from employees WHERE oid=" + id_entry.get())
    conn.commit()
    conn.close()
    clear_entry_boxes()
    #clear treeview
    my_tree.delete(*my_tree.get_children())
    # put it back
    query_db()
    # messagebox
    messagebox.showinfo("Info Message", "Record has been succesfully deleted!")


def remove_all():
    response = messagebox.askyesno('WARNING', 'This will delete EVERYTHING from the database forever.\nAre you sure?')
    if response == 1:
        for record in my_tree.get_children():
            my_tree.delete(record)
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("DROP TABLE employees")
        conn.commit()
        conn.close()
    checkCreateTables()


def update_record():
    #selected = my_tree.focus()
    #my_tree.item(selected, text="", values=(id_entry.get(), name_entry.get(), pay_entry.get(), title_entry.get(), date_hired_entry.get(),))
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    # Update db
    c.execute("""UPDATE employees SET
              name = :name,
              pay = :pay,
              title = :title,
              date_hired = :date_hired,
              description = :description,
              portrait = :portrait
              
              WHERE oid =""" + id_entry.get(), 
              {
                  'name': name_entry.get(),
                  'pay': pay_entry.get(),
                  'title': title_entry.get(),
                  'date_hired': date_hired_entry.get(),
                  'description': description_entry.get(),
                  'portrait': portrait_location_entry.get(),
                  'oid': id_entry.get()
              }
              )
    conn.commit()
    conn.close()
    # Clear entry boxes
    name_entry.delete(0, END)
    pay_entry.delete(0, END)
    portrait_location_entry.delete(0, END)
    title_entry.delete(0, END)
    date_hired_entry.delete(0, END)
    id_entry.delete(0, END)
    #clear treeview
    my_tree.delete(*my_tree.get_children())
    # put it back
    query_db()


def add_record():
    if portrait_location_entry.get() == "":
        portrait_location_entry_variable = 'headshot.png'
    else:
        portrait_location_entry_variable = portrait_location_entry.get()
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT * from employees WHERE oid=" + id_entry.get())
    x = c.fetchall()
    u = 0
    for i in x:
        u += 1
    #print(u)
    if u == 0:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO employees VALUES (:id, :name, :pay, :title, :date_hired, :description, :portrait)",
              {
                  'id': id_entry.get(),
                  'name': name_entry.get(),
                  'pay': pay_entry.get(),
                  'title': title_entry.get(),
                  'date_hired': date_hired_entry.get(),
                  'description': "",
                  'portrait': portrait_location_entry_variable
              }
              )
        conn.commit()
        conn.close()
        # Clear entry boxes
        name_entry.delete(0, END)
        pay_entry.delete(0, END)
        title_entry.delete(0, END)
        date_hired_entry.delete(0, END)
        id_entry.delete(0, END)
        #clear treeview
        my_tree.delete(*my_tree.get_children())
        # put it back
        query_db()
    else:
        messagebox.showerror('Error:id', 'That employee id # is already in use.')
        conn.commit()
        conn.close()


button_frame = Frame(lf)
button_frame.config(width=650, borderwidth=7, relief='raised')

update_record_button = Button(button_frame, text="Update Record", command=update_record) # update record (change info)
update_record_button.grid(row=0, column=0, padx=26, pady=10)

add_record_button = Button(button_frame, text="Add Record", command=add_record) # add record (add new employee)
add_record_button.grid(row=0, column=1, padx=26, pady=10)

clear_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entry_boxes) # fill entry boxes with info from selected item in treeview
clear_button.grid(row=0, column=2, padx=26, pady=10)

remove_selected_button = Button(button_frame, text="Remove Selected Record", command=remove_selected) # remove selected record
remove_selected_button.grid(row=0, column=3, padx=26, pady=10)

remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all) # remove all records
remove_all_button.grid(row=0, column=4, padx=26, pady=10)

leftFrame.config(borderwidth=7, width=645)

data_frame.config(borderwidth=7, relief="raised")

leftFrame.pack(side=TOP, anchor=NW, fill=BOTH, expand=YES)

data_frame.pack(fill=X, expand=NO)

button_frame.pack(side=TOP, ancho=NW, fill=X, expand=NO)

lf.config(borderwidth=7, relief='ridge', bg='green')
lf.pack(side='left', fill=Y)

my_tree.bind("<ButtonRelease-1>", select_record)

query_db()

window.mainloop()
