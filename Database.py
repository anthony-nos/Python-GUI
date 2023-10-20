import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

def connect_to_db():
    global db
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Gains!1803",
        database="cbm005"
    )
  


def add_record():
    cursor = db.cursor()
    data = (entry_name.get(), entry_age.get())
    cursor.execute("Insert Into table_name (name, age) Values (%s, %s)", data)
    db.commit()
    cursor.close()
    messagebox.showinfo("Info", "Record added successfully")
    view_records()

def view_records():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM table_name")
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
root.title("Database GUI")

label_subject = Label(root, text="Subject")
label_course = Label(root, text="Course")
label_crn = Label(root, text="CRN")

entry_subject = Entry(root)
entry_course = Entry(root)
entry_crn = Entry(root)

button_add = Button(root, text="Add Record", command=add_record)
button_view = Button(root, text="View Records", command=view_records)

label_subject.grid(row=0, column=0, sticky="w")
label_course.grid(row=1, column=0, sticky="w")
label_crn.grid(row=2, column=0, sticky="w")

entry_subject.grid(row=0, column=1, sticky="w")
entry_course.grid(row=1, column=1, sticky="w")
entry_crn.grid(row=2, column=1, sticky="w")

button_add.grid(row=3, column=0, sitcky="w")
button_view.grid(row=3, column=1, sticky="w")

treeview = ttk.Treeview(root, columns=("Subject", "Course", "CRN"), show="headings")
treeview.heading("Subject", text="Subject")
treeview.heading("Course", text="Course")
treeview.heading("CRN", text="CRN")
treeview.grid(row=4, column=0, columnspan=2, sticky="nsew")

root.columnconfigure(1, weight=1)
root.rowconfigure(4, weight=1)

connect_to_db()
root.mainloop()




#def click():
    #print("You are searching for a course")
#def submit():
    #Course_Number = entry.get()
    #print("Example")

#window = Tk() 

#entry = Entry(window,
              #font=("Times New Roman",50))
#entry.place(x=375,y=400)

#submit_button = Button(window,text="Search",command=submit)
#submit_button.place(x=300,y=425)

#window.geometry("1000x1000")
#window.title("Database GUI")


#window.config(background="black")
#button = Button(window,
#                text="Search",
#                comman=click,
#                font=("Times New Roman",30),
#                fg="gold",
#                bg='black',
#                activeforeground='gold',
#                activebackground='black',
#                state=ACTIVE)
#button.place(x=725,y=750)


#label = Label(window,text="Hello User",
#              font=('Times New Roman',40,'bold'),
#              fg='gold',
#              bg='black',
#              relief=RAISED,
#              bd=10,
#              padx=20,
#              pady=20)
#label.pack()

#window.mainloop()
