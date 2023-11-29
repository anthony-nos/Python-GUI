import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog



def connect_to_db():
    global db
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Gains!1803",
        database="cbm005"
    )
  

def add_record():
    global db
    cursor = db.cursor()
    Record_Code = simpledialog.askinteger("Add Record", "Enter Record Code:")
    Institution_Code = simpledialog.askstring("Add Record", "Enter Institution Code:")
    Subject_P = simpledialog.askstring("Add Record", "Enter Subject P:")
    Course_Number = simpledialog.askstring("Add Record", "Enter Course Number:")
    Section_Number = simpledialog.askstring("Add Record", "Enter Section Number:")
    Unused = simpledialog.askstring("Add Record", "Enter Unused:")
    Building = simpledialog.askstring("Add Record", "Enter Building:")
    Room = simpledialog.askstring("Add Record", "Enter Room:")
    DoW = simpledialog.askstring("Add Record", "Enter Day of Week:")
    Start_T = simpledialog.askstring("Add Record", "Enter Start Time:")
    Duration = simpledialog.askstring("Add Record", "Enter Duration:")
    Semester = simpledialog.askstring("Add Record", "Enter Semester:")
    Yr = simpledialog.askstring("Add Record", "Enter Year:")
    Room_Type = simpledialog.askstring("Add Record", "Enter Room Type:")
    Enrollment1 = simpledialog.askstring("Add Record", "Enter Enrollment1:", initialvalue='default_value')
    Enrollment2 = simpledialog.askstring("Add Record", "Enter Enrollment2:", initialvalue='default_value')
    Enrollment3 = simpledialog.askstring("Add Record", "Enter Enrollment3:", initialvalue='default_value')
    Enrollment4 = simpledialog.askstring("Add Record", "Enter Enrollment4:", initialvalue='default_value')
    Enrollment5 = simpledialog.askstring("Add Record", "Enter Enrollment5:", initialvalue='default_value')

    data = (Record_Code, Institution_Code, Subject_P, Course_Number, Section_Number,
            Unused, Building, Room, DoW, Start_T, Duration, Semester, Yr, Room_Type,
            Enrollment1, Enrollment2, Enrollment3, Enrollment4, Enrollment5)
    
    cursor.execute('''
        INSERT INTO cbm005_table (
            Record_Code, Institution_Code, Subject_P, Course_Number, Section_Number,
            Unused, Building, Room, DoW, Start_T, Duration, Semester, Yr, Room_Type,
            Enrollment1, Enrollment2, Enrollment3, Enrollment4, Enrollment5
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', data)

    db.commit()
    cursor.close()
    messagebox.showinfo("Info", "Record added successfully")
    view_records()

def view_records():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM cbm005_table")
    records = cursor.fetchall()
    for record in treeview.get_children():
        treeview.delete(record)
    

    column_names = [desc[0] for desc in cursor.description]

    treeview["columns"] = column_names
    for col_name in column_names:
        treeview.heading(col_name, text=col_name)
        treeview.column(col_name, width=100)
    
    for record in records:
        treeview.insert("", "end", values=record)

   
    cursor.close()

def open_modify_window():
    subject = simpledialog.askstring("Modify Record", "Enter Subject:")
    old_value = simpledialog.askstring("Modify Record", "Enter Old Value:")
    new_value = simpledialog.askstring("Modify Record", "Enter New Value:")
    field_to_modify = simpledialog.askstring("Modify Record", "Choose Field to Modify (Building, Room, DoW, Start_T):")

    if subject and old_value and new_value and field_to_modify:
        modify_record(subject, field_to_modify,  old_value, new_value)
    else:
        messagebox.showwarning("Warning", "Please enter values for Subject, Old Course, New Course, and choose a Field to Modify.")

def modify_record(subject, field_to_modify, old_value, new_value):
    cursor = db.cursor()
    query = f"UPDATE cbm005_table SET {field_to_modify} = %s WHERE Subject_P = %s AND {field_to_modify} = %s"
    cursor.execute(query, (new_value, subject, old_value))
    db.commit()
    cursor.close()
    messagebox.showinfo("Info", f"{field_to_modify} modified successfully for {subject} from {old_value} to {new_value}")
    view_records()

def delete_record():
    crn_to_delete = entry_delete_crn.get()

    if not crn_to_delete:
        messagebox.showwarning("Warning", "Please enter a CRN to delete")
        return
    
    confirmation = messagebox.askokcancel("Confirm Deletion", f"Are you sure you want to delete this record with CRN {crn_to_delete}?")

    if confirmation:
        cursor = db.cursor()
        cursor.execute("DELETE FROM cbm005_table WHERE Course_Number = %s", (crn_to_delete,))
        db.commit()
        cursor.close()
        messagebox.showinfo("Info", f"Record with Course_Number {crn_to_delete} deleted successfully")
        view_records()

def search_records():
    cursor = db.cursor()
    search_query = entry_search.get()
    cursor.execute("SELECT * FROM cbm005_table WHERE Course_Number LIKE %s", (f"%{search_query}%",))
    records = cursor.fetchall()
    for record in treeview.get_children():
        treeview.delete(record)

    column_names = [desc[0] for desc in cursor.description]
    treeview["columns"] = column_names
    for col_name in column_names:
        treeview.heading(col_name, text=col_name)
        treeview.column(col_name, width=100)

    for record in records:
        treeview.insert("", "end", values=record)
    cursor.close()

root = Tk()


root.config(background="dark grey")

root.title("Database GUI")


entry_delete_crn = Entry(root, bg="white")
entry_search = Entry(root, bg="white")

button_add = Button(root, bg="#549C30", text="Add Record", command=add_record)
button_view = Button(root, bg="blue", text="View Records", command=view_records)
button_search = Button(root, bg="blue", text="Search", command=search_records)
button_delete = Button(root, bg="red", text="Delete", command=delete_record)
button_modify = Button(root, bg="gold", text="Modify", command=open_modify_window)

entry_search.grid(row=3, column=1, columnspan=2,sticky="w")
entry_delete_crn.grid(row=4, column=1, columnspan=2, sticky="w")

button_add.grid(row=5, column=0, sticky="w")
button_view.grid(row=5, column=2, sticky="w")
button_search.grid(row=3, column=0, columnspan=2, sticky="w")
button_delete.grid(row=4, column=0, columnspan=2, sticky="w")
button_modify.grid(row=5, column=1, sticky="w")

treeview = ttk.Treeview(root, columns=("Subject", "Course", "CRN"), show="headings")
treeview.heading("Subject", text="Subject")
treeview.heading("Course", text="Course")
treeview.heading("CRN", text="CRN")
treeview.grid(row=6, column=0, columnspan=10, sticky="nsew")

root.columnconfigure(1, weight=1)
root.rowconfigure(6, weight=1)


connect_to_db()
root.mainloop()