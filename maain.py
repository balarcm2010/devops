import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook


from datetime import datetime, timedelta
from datetime import date, timedelta


# Create the main window
root = tk.Tk()
root.title("Timesheet form")
root.geometry("1200x670")
root.resizable(False,False)
root.grid()


# Create the first tab
notebook = ttk.Notebook(root)
tab1 = Frame()
tab2 = Frame()
tab3 = Frame()
tree = Frame()

notebook.add(tab1,text="Time & Expense")
notebook.add(tab2,text="Documents")
notebook.pack(expand="False",fill="none")

# Function to get the list of weeks
def get_weeks():
    weeks = []
    today = datetime.strptime("2023-02-06", "%Y-%m-%d")  
    for i in range(-20,20):
        week_start = today + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)
        week_string = f"{week_start.strftime('%b %d, %Y')} - {week_end.strftime('%b %d, %Y')}"
        weeks.append(week_string)
    return weeks


# Function to update the dates in the tree view
def update_dates(*args):
    week = week_var.get()
    week_start = datetime.strptime(week.split(" - ")[0], '%b %d, %Y')
    week_start = week_start - timedelta(days=week_start.weekday())  # Updated line
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_text = day.strftime("%m/%d")
        column = ("Mon","Tue","Wed","Thu","Fri","Sat","Sun")[day.weekday()]
        tree.heading(column, text=f"{column} {day_text}")


# Create a dropdown for selecting the week
week_var = tk.StringVar(value=get_weeks()[0])
week_dropdown = ttk.Combobox(tab1, textvariable=week_var,values=get_weeks())
week_dropdown.place(x=950,y=50)
week_var.trace("w",update_dates)


Label1=tk.Label(tab1, text="Timesheet", font=("arial", 18), bd=50, fg="blue",justify="left").pack(anchor="w")
Label2=tk.Label(tab1, text="Pay bill bypass type:" ,font=("arial",14),bd=50,fg="blue",height=1).place(x=300,y=0)
#Label3=tk.Label(tab1, text="Calculated Time",font=("arial",14), bd=80, fg="blue",height=1).place(x=900,y=20)
tree=ttk.Treeview(tab1,columns=("Mon","Tue","Wed","Thu","Fri","Sat","Sun"),show="headings",height=15)
#Label3=tk.OptionMenu(tab1, week_var,*get_weeks(),command=selc).place(x=1000,y=40)
total_hours_label = ttk.Label(tab1, text="Total Hours:", font=("arial", 14),foreground="maroon").place(x=700, y=50)


def calculate_time():
    login_time = login_var.get()
    logout_time = logout_var.get()
    if login_time and logout_time:
        login_time = datetime.strptime(login_time, '%H:%M')
        logout_time = datetime.strptime(logout_time, '%H:%M')
        if logout_time > login_time:
            calculated_time = (logout_time - login_time).total_seconds() / 3600
            calculated_time_var.set('{:.2f}'.format(calculated_time))
        else:
           messagebox.showerror("Error", "Logout time must be later than login time")
    else:
        None#messagebox.showerror("Error", "Please enter both login and logout time")


# Create the frames for login and logout time
#style=ttk.Style(root)
login_frame = ttk.Frame(tab1)
login_frame.pack(pady=0)
logout_frame = ttk.Frame(tab1)
logout_frame.pack(pady=0)



# Create the login and logout labels and entry widgets
login_label = ttk.Label(login_frame, text="Login time (HH:MM):")
login_label.grid(row=0, column=0, padx=5)
login_var = tk.StringVar()
login_entry = ttk.Entry(login_frame, textvariable=login_var)
login_entry.grid(row=0, column=1, padx=5)
logout_label = ttk.Label(logout_frame, text="Logout time (HH:MM):")
logout_label.grid(row=0, column=0, padx=5)
logout_var = tk.StringVar()
logout_entry = ttk.Entry(logout_frame, textvariable=logout_var)
logout_entry.grid(row=0, column=1, padx=5)


# Create the calculate button and the calculated time label
calculate_button = ttk.Button(tab1, text="Calculate", command=calculate_time)
calculate_button.place(x=980,y=80)
calculated_time_var = tk.StringVar()
calculated_time_label = ttk.Label(tab1, textvariable=calculated_time_var,font=("arial",14)).place(x=800,y=50)
#calculated_time_label.pack()


# Create a tree view to display the dates and corresponding days of the week
#tree=ttk.Treeview(root, columns=("Mon","Tue","Wed","Thu","Fri","Sat","Sun"), show="headings", height=20)
tree["columns"] = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
tree.column("#0", width=100, minwidth=100, stretch=tk.YES)
for column in tree["columns"]:
    tree.column(column, width=160, minwidth=100)


tree.heading("Mon", text="Mon")
tree.heading("Tue", text="Tue")
tree.heading("Wed", text="Wed")
tree.heading("Thu", text="Thu")
tree.heading("Fri", text="Fri")
tree.heading("Sat", text="Sat")
tree.heading("Sun", text="Sun")
tree.pack(pady=10)


style=ttk.Style(root)
style.theme_use('clam')
style.configure("Horizontal.heading",columnspan=3,background='Powerblue',height=90,weight=0)


tree.pack()

#insert_get_weeks()

# Run the main loop
root.mainloop()
