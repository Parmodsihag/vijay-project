import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
import mydatabse
# from mydatabase import insert_data


db_file = 'my_database.db'  # Replace with your database file name
conn = mydatabse.create_connection(db_file)
if conn is not None:
    current_month_year = datetime.now().strftime('%B_%Y')  # Get current month and year as text
    mydatabse.create_table(conn, current_month_year)


def add_details():
    # Fetching data from the entry boxes
    date_val = entry_date.get()
    details_val = entry_details.get()
    p_s_val = combo_p_s.get()
    amount_val = entry_amount.get()

    # Check if the entered date is not today's date
    if date_val != date.today().strftime('%Y-%m-%d'):
        # Check if the entered date is in the same month as today
        entered_month_year = datetime.strptime(date_val, '%Y-%m-%d').strftime('%B_%Y')
        current_month_year = datetime.now().strftime('%B_%Y')
        
        if entered_month_year != current_month_year:
            # Check if the table exists for the entered month_year, if not, create it
            if entered_month_year not in mydatabse.get_available_tables('my_database.db'):
                mydatabse.create_table(conn, entered_month_year)

            # Inserting data into the respective month_year table
            mydatabse.insert_data(conn, entered_month_year, date_val, details_val, p_s_val, amount_val)
        else:
            # Insert data into the current_month_year table
            mydatabse.insert_data(conn, current_month_year, date_val, details_val, p_s_val, amount_val)
    else:
        # Insert data into the current_month_year table as it's today's date
        current_month_year = datetime.now().strftime('%B_%Y')
        mydatabse.insert_data(conn, current_month_year, date_val, details_val, p_s_val, amount_val)


# Function to update the lower frame
def update_lower_frame():
    selected_table = combo_tables.get()

    # Fetching data based on the selected table
    rows = mydatabse.fetch_data('my_database.db', selected_table)

    # Update table content
    table.delete(*table.get_children())  # Clear previous content
    if rows:
        c = 1
        for row in rows:
            if c%2:
                tag = 'even'
            else:
                tag = 'odd'
            table.insert("", "end", values=row, tags=tag)
            c += 1
        table.tag_configure('odd', foreground='#434343', background='#aaaaaa')
        table.tag_configure('even', foreground='#aaaaaa', background='#434343')

    # Calculate purchase and sales total
    purchase_total = sum(row[4] for row in rows if row[3] == 'p')
    sales_total = sum(row[4] for row in rows if row[3] == 's')
    total_label.config(text=f"Total Purchase {purchase_total} - Sales {sales_total} = {purchase_total - sales_total}")


# Setting up the main window
root = tk.Tk()
root.title("Database UI")
root.state('zoomed')
root.configure(bg="#333333")  # Dark theme background color

style=ttk.Style()
style.theme_create('mytheme', parent='alt', 
                        settings={
                            'TCombobox':
                            {
                                'configure':
                                {
                                'selectbackground': "#4EC5F1",
                                'fieldbackground': "white",
                                'foreground': "green",
                                'arrowsize': 18,
                                'font':"Consolas 14"
                                }
                            },
                            'Treeview':{
                                'configure':
                                {
                                    'rowheight': 30,
                                    'fieldbackground': "#333333",
                                    'font': 'Ubantu 10'
                                }
                            }
                        }
                    )
style.theme_use('mytheme')
style.configure("Treeview.Heading", foreground='#a0dad0', background="#3f3f3f", font='Consolas 12')
        
c = "#333333"
f = 'consolas 14'

vijay_name = tk.Label(root, text='VISHNU ENTERPRISES', font='Consolas 22 bold', bg='#c8e6a4', fg='#371a5b')
vijay_name.pack(padx=20, pady=(20,0),fill='x', expand=1)

# Upper section layout

upper_frame = tk.Frame(root, bg="#333333")
upper_frame.pack(padx=20, pady=20)

# Label for Date Entry
date_label = tk.Label(upper_frame, text="Date:", bg=c, font=f)
date_label.grid(row=0, column=0, padx=5, pady=5)

# Date Entry
today_date = date.today().strftime('%Y-%m-%d')
entry_date = tk.Entry(upper_frame, font=f)
entry_date.insert(0, today_date)
entry_date.grid(row=0, column=1, padx=5, pady=5)

# Label for Details Entry
details_label = tk.Label(upper_frame, text="Details:", bg=c, font=f)
details_label.grid(row=0, column=2, padx=5, pady=5)

# Details Entry
entry_details = tk.Entry(upper_frame, font=f)
entry_details.grid(row=0, column=3, padx=5, pady=5)

# Label for P/S Combo Box
ps_label = tk.Label(upper_frame, text="P/S:", bg=c, font=f)
ps_label.grid(row=0, column=4, padx=5, pady=5)

# P/S Combo Box
combo_p_s = ttk.Combobox(upper_frame, values=["p", "s"], font=f)
combo_p_s.grid(row=0, column=5, padx=5, pady=5)

# Label for Amount Entry
amount_label = tk.Label(upper_frame, text="Amount:", bg=c, font=f)
amount_label.grid(row=0, column=6, padx=5, pady=5)

# Amount Entry
entry_amount = tk.Entry(upper_frame, font=f)
entry_amount.grid(row=0, column=7, padx=5, pady=5)

# Add Details Button
add_button = tk.Button(upper_frame, text="Add", command=add_details, font=f)
add_button.grid(row=0, column=8, padx=5, pady=10)

# Lower section layout (frame placeholder)
lower_frame = tk.Frame(root, bg="#434343")
lower_frame.pack(padx=20, pady=20)


# ComboBox for selecting tables
combo_tables = ttk.Combobox(lower_frame, state="readonly", font=f)
combo_tables.grid(row=0, column=0, padx=5, pady=5)
combo_tables.bind("<Enter>", lambda e: combo_tables.config(values = mydatabse.get_available_tables('my_database.db')))
# Populate the ComboBox with available tables (You may fetch this dynamically from your database)
combo_tables['values'] = mydatabse.get_available_tables('my_database.db') # Replace with actual table names

# Label to display purchase and sales total
total_label = tk.Label(lower_frame, text="", fg="white", bg="#333333", font=("times now", 18))
total_label.grid(row=0, column=1, padx=5, pady=5)

# Table to display selected table content
table = ttk.Treeview(lower_frame, columns=('UID', 'Date', 'Details', 'P/S', 'Amount'))
table.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
# table.heading('#0', text='UID')
table.heading('UID', text='UID')
table.heading('Date', text='Date')
table.heading('Details', text='Details')
table.heading('P/S', text='P/S')
table.heading('Amount', text='Amount')

# Button to trigger data update
update_button = tk.Button(lower_frame, text="Update", command=update_lower_frame, font=f)
update_button.grid(row=2, column=0, columnspan=2, pady=10)


# Run the Tkinter main loop
root.mainloop()
