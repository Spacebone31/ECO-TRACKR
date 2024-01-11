import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from tkcalendar import DateEntry

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="pollution"
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def execute_query(self, query, data=None):
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False

    def fetch_data(self, query, data=None):
        self.cursor.execute(query, data)
        return self.cursor.fetchall()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Pollution Database App")
        self.root.geometry("800x400")

        self.db = Database()
        self.current_user_id = None

        self.login_frame = tk.Frame(self.root, padx=20, pady=20)
        self.login_frame.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.show_login)
        self.login_button.grid(row=0, column=0, padx=10)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.show_register)
        self.register_button.grid(row=0, column=1, padx=10)

        # Action buttons created here
        self.view_button = tk.Button(self.root, text="View Data", command=self.view_data)
        self.add_button = tk.Button(self.root, text="Add Data", command=self.add_data)
        self.delete_button = tk.Button(self.root, text="Delete Data", command=self.delete_data)
        self.change_button = tk.Button(self.root, text="Change Data", command=self.change_data)
        self.logout_button = tk.Button(self.root, text="Logout", command=self.show_main_page)

    def show_login(self):
        self.register_button.grid_remove()  # Remove the register button
        self.login_frame.destroy()

        login_frame = tk.Frame(self.root, padx=20, pady=20)
        login_frame.pack()

        username_label = tk.Label(login_frame, text="Username:")
        username_label.grid(row=0, column=0, sticky="e")

        username_entry = tk.Entry(login_frame)
        username_entry.grid(row=0, column=1)

        password_label = tk.Label(login_frame, text="Password:")
        password_label.grid(row=1, column=0, sticky="e")

        password_entry = tk.Entry(login_frame, show="*")
        password_entry.grid(row=1, column=1)

        login_button = tk.Button(login_frame, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.grid(row=2, column=1, pady=10)
        
        back_button = tk.Button(login_frame, text="Back", command=self.show_main_page)
        back_button.grid(row=3, column=1, pady=10)

    def show_register(self):
        self.login_button.grid_remove()  # Remove the login button
        self.login_frame.destroy()

        register_frame = tk.Frame(self.root, padx=20, pady=20)
        register_frame.pack()

        username_label = tk.Label(register_frame, text="Username:")
        username_label.grid(row=0, column=0, sticky="e")

        username_entry = tk.Entry(register_frame)
        username_entry.grid(row=0, column=1)

        password_label = tk.Label(register_frame, text="Password:")
        password_label.grid(row=1, column=0, sticky="e")

        password_entry = tk.Entry(register_frame, show="*")
        password_entry.grid(row=1, column=1)

        fullname_label = tk.Label(register_frame, text="Full Name:")
        fullname_label.grid(row=2, column=0, sticky="e")

        fullname_entry = tk.Entry(register_frame)
        fullname_entry.grid(row=2, column=1)

        email_label = tk.Label(register_frame, text="Email:")
        email_label.grid(row=3, column=0, sticky="e")

        email_entry = tk.Entry(register_frame)
        email_entry.grid(row=3, column=1)

        register_button = tk.Button(register_frame, text="Register", command=lambda: self.register(username_entry.get(), password_entry.get(), fullname_entry.get(), email_entry.get()))
        register_button.grid(row=4, column=1, pady=10)
        
        back_button = tk.Button(register_frame, text="Back", command=self.show_main_page)
        back_button.grid(row=5, column=1, pady=10)

    def login(self, username, password):
        # Add authentication logic here
        # Check if the username and password match a record in the database
        query = "SELECT * FROM user WHERE username = %s AND password = %s"
        data = (username, password)
        result = self.db.fetch_data(query, data)

        if result:
            messagebox.showinfo("Success", "Login successful!")
            self.current_user_id = result[0][0]
            self.show_main_app()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self, username, password, fullname, email):
        # Add registration logic here
        # Insert the new user data into the database
        query = "INSERT INTO user (username, password, fullName, email) VALUES (%s, %s, %s, %s)"
        data = (username, password, fullname, email)

        if self.db.execute_query(query, data):
            messagebox.showinfo("Success", "Registration successful!")

            # Fetch the user_id for the newly registered user
            user_query = "SELECT user_id FROM user WHERE username = %s"
            user_data = (username,)
            result = self.db.fetch_data(user_query, user_data)

            if result:
                self.current_user_id = result[0][0]

                # After successful registration and setting current_user_id, show the main app
                self.show_main_app()
            else:
                messagebox.showerror("Error", "Failed to fetch user_id after registration")
        else:
            messagebox.showerror("Error", "Registration failed")

    def create_action_buttons(self):
        # Additional buttons for actions (View, Add, Delete, Change)
        self.view_button.pack(side="top", pady=10)
        self.add_button.pack(side="top", pady=10)
        self.delete_button.pack(side="top", pady=10)
        self.change_button.pack(side="top", pady=10)
        self.logout_button.pack(side="top", pady=10)

    def view_data(self):
        # Fetch data from the database using the provided query
        query = """
            SELECT `user`.`fullName`, `user`.`email`, `source`.`pollutionType`, `source`.`pollutantName`, 
            `source`.`description`, `location`.`country`, `location`.`city`, `event`.`date`, `event`.`severityLevel`, 
            `event`.`description`, `mitigationstrategy`.`name`, `mitigationstrategy`.`effectiveness`, 
            `mitigationstrategy`.`description`
            FROM `user` 
            LEFT JOIN `source` ON `source`.`user_id` = `user`.`user_id` 
            LEFT JOIN `location` ON `location`.`source_id` = `source`.`source_id` 
            LEFT JOIN `event` ON `event`.`source_id` = `source`.`source_id` 
            LEFT JOIN `mitigationstrategy` ON `mitigationstrategy`.`event_id` = `event`.`event_id`
            ORDER BY `user`.`fullName`;
        """
        result = self.db.fetch_data(query)

        # Create a new window for displaying data
        view_window = tk.Toplevel(self.root)
        view_window.title("View Data")

        # Display data in a new frame with a horizontal scrollable table
        data_frame = tk.Frame(view_window, padx=20, pady=20)
        data_frame.pack()

        columns = [
            "Full Name", "Email", "Pollution Type", "Pollutant Name",
            "Pollution Description", "Country", "City", "Date", "Severity Level",
            "Pollution Activity Description", "Mitigation Strategy Name",
            "Effectiveness", "Mitigation Strategy Description"
        ]

        tree = ttk.Treeview(data_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        # Calculate the column widths based on the maximum length of data in each column
        for i, col in enumerate(columns):
            max_len = max(len(str(row[i])) for row in result)
            col_width = max(max_len, len(col))
            tree.column(col, width=col_width * 10)  # Adjust the multiplier based on your preference

        for row in result:
            tree.insert("", "end", values=row)

        # Add a horizontal scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side="bottom", fill="x")

        tree.pack(side="top", fill="both", expand=True)

    def add_data(self):
        # Create a new window for adding data
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Data")

        # Display input fields for adding data
        add_frame = tk.Frame(add_window, padx=20, pady=20)
        add_frame.pack()

        # Input fields for source table
        pollution_type_label = tk.Label(add_frame, text="Pollution Type:")
        pollution_type_label.grid(row=0, column=0, sticky="e")
        pollution_type_entry = tk.Entry(add_frame, width=30)
        pollution_type_entry.grid(row=0, column=1)

        pollutant_name_label = tk.Label(add_frame, text="Pollutant Name (pesticides, monoxide, etc):")
        pollutant_name_label.grid(row=1, column=0, sticky="e")
        pollutant_name_entry = tk.Entry(add_frame, width=30)
        pollutant_name_entry.grid(row=1, column=1)

        description_label = tk.Label(add_frame, text="Description:")
        description_label.grid(row=2, column=0, sticky="e")
        description_entry = tk.Entry(add_frame, width=30)
        description_entry.grid(row=2, column=1)

        # Input fields for location table
        country_label = tk.Label(add_frame, text="Country:")
        country_label.grid(row=3, column=0, sticky="e")
        country_entry = tk.Entry(add_frame, width=30)
        country_entry.grid(row=3, column=1)

        city_label = tk.Label(add_frame, text="City:")
        city_label.grid(row=4, column=0, sticky="e")
        city_entry = tk.Entry(add_frame, width=30)
        city_entry.grid(row=4, column=1)

        # Input fields for event table
        date_label = tk.Label(add_frame, text="Date:")
        date_label.grid(row=5, column=0, sticky="e")
        date_entry = DateEntry(add_frame, date_pattern='yyyy-mm-dd', width=25)
        date_entry.grid(row=5, column=1)

        severity_level_label = tk.Label(add_frame, text="Severity Level:")
        severity_level_label.grid(row=6, column=0, sticky="e")
        severity_level_entry = tk.Entry(add_frame, width=30)
        severity_level_entry.grid(row=6, column=1)

        event_description_label = tk.Label(add_frame, text="Pollution Activity Description:")
        event_description_label.grid(row=7, column=0, sticky="e")
        event_description_entry = tk.Entry(add_frame, width=30)
        event_description_entry.grid(row=7, column=1)

        # Input fields for mitigationstrategy table
        strategy_name_label = tk.Label(add_frame, text="Mitigation Strategy Name:")
        strategy_name_label.grid(row=8, column=0, sticky="e")
        strategy_name_entry = tk.Entry(add_frame, width=30)
        strategy_name_entry.grid(row=8, column=1)

        effectiveness_label = tk.Label(add_frame, text="Effectiveness:")
        effectiveness_label.grid(row=9, column=0, sticky="e")
        effectiveness_entry = tk.Entry(add_frame, width=30)
        effectiveness_entry.grid(row=9, column=1)

        strategy_description_label = tk.Label(add_frame, text="Strategy Description:")
        strategy_description_label.grid(row=10, column=0, sticky="e")
        strategy_description_entry = tk.Entry(add_frame, width=30)
        strategy_description_entry.grid(row=10, column=1)

        # Button to submit the data
        submit_button = tk.Button(add_frame, text="Submit", command=lambda: self.submit_data(
            pollution_type_entry.get(), pollutant_name_entry.get(), description_entry.get(),
            country_entry.get(), city_entry.get(), date_entry.get(), severity_level_entry.get(),
            event_description_entry.get(), strategy_name_entry.get(), effectiveness_entry.get(),
            strategy_description_entry.get(), add_window
        ))
        submit_button.grid(row=11, column=1, pady=10)

    def submit_data(self, pollution_type, pollutant_name, description, country, city, date, severity_level,
                    event_description, strategy_name, effectiveness, strategy_description, add_window):
        try:
            # Insert data into the tables and maintain foreign key relationships
            # Use the current_user_id as the foreign key for the user table

            # Insert into source table
            source_query = "INSERT INTO source (user_id, pollutionType, pollutantName, description) VALUES (%s, %s, %s, %s)"
            source_data = (self.current_user_id, pollution_type, pollutant_name, description)
            self.db.execute_query(source_query, source_data)

            # Retrieve the source_id of the inserted source record
            source_id = self.db.cursor.lastrowid

            # Insert into location table
            location_query = "INSERT INTO location (source_id, country, city) VALUES (%s, %s, %s)"
            location_data = (source_id, country, city)
            self.db.execute_query(location_query, location_data)

            # Retrieve the location_id of the inserted location record
            location_id = self.db.cursor.lastrowid

            # Insert into event table
            event_query = "INSERT INTO event (source_id, date, severityLevel, description) VALUES (%s, %s, %s, %s)"
            event_data = (source_id, date, severity_level, event_description)
            self.db.execute_query(event_query, event_data)

            # Retrieve the event_id of the inserted event record
            event_id = self.db.cursor.lastrowid

            # Insert into mitigationstrategy table
            strategy_query = "INSERT INTO mitigationstrategy (event_id, name, effectiveness, description) VALUES (%s, %s, %s, %s)"
            strategy_data = (event_id, strategy_name, effectiveness, strategy_description)
            self.db.execute_query(strategy_query, strategy_data)

            # Commit changes to the database
            self.db.connection.commit()

            # Close the add window
            add_window.destroy()

            # Optionally, show a success message
            messagebox.showinfo("Success", "Data added successfully!")

        except Exception as e:
            # Display detailed error information
            messagebox.showerror("Error", f"Failed to add data. Error: {str(e)}")

    def delete_data(self):
        # Fetch data from the database using the provided query
        query = """
            SELECT `user`.`user_id`, `user`.`fullName`, `user`.`email`, `source`.`source_id`, `source`.`pollutionType`, 
            `source`.`pollutantName`, `source`.`description`, `location`.`country`, `location`.`city`, `event`.`date`, 
            `event`.`severityLevel`, `event`.`description`, `mitigationstrategy`.`name`, `mitigationstrategy`.`effectiveness`, 
            `mitigationstrategy`.`description`
            FROM `user` 
            LEFT JOIN `source` ON `source`.`user_id` = `user`.`user_id` 
            LEFT JOIN `location` ON `location`.`source_id` = `source`.`source_id` 
            LEFT JOIN `event` ON `event`.`source_id` = `source`.`source_id` 
            LEFT JOIN `mitigationstrategy` ON `mitigationstrategy`.`event_id` = `event`.`event_id`
            ORDER BY `user`.`fullName`;
        """
        result = self.db.fetch_data(query)

        # Create a new window for displaying data
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Data")

        # Display data in a new frame with a vertical scrollable table
        data_frame = tk.Frame(delete_window, padx=20, pady=20)
        data_frame.pack()

        columns = [
            "User ID", "Full Name", "Email", "Source ID", "Pollution Type", "Pollutant Name",
            "Pollution Description", "Country", "City", "Date", "Severity Level",
            "Pollution Activity Description", "Mitigation Strategy Name",
            "Effectiveness", "Mitigation Strategy Description"
        ]

        tree = ttk.Treeview(data_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        for row in result:
            tree.insert("", "end", values=row)

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(side="left", fill="both", expand=True)
        
        # Add a horizontal scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side="bottom", fill="x")

        tree.pack(side="top", fill="both", expand=True)

        # Button to delete the selected row
        delete_button = tk.Button(delete_window, text="Delete Selected Row", command=lambda: self.confirm_delete(tree, delete_window))
        delete_button.pack(pady=10)

    def confirm_delete(self, tree, delete_window):
        selected_item = tree.selection()
        if selected_item:
            confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
            if confirmation:
                # Get the source_id from the selected row
                source_id = tree.item(selected_item, 'values')[3]

                # Delete data from the tables based on the source_id
                source_query = "DELETE FROM source WHERE source_id = %s"
                location_query = "DELETE FROM location WHERE source_id = %s"
                event_query = "DELETE FROM event WHERE source_id = %s"
                strategy_query = "DELETE FROM mitigationstrategy WHERE event_id IN (SELECT event_id FROM event WHERE source_id = %s)"

                self.db.execute_query(source_query, (source_id,))
                self.db.execute_query(location_query, (source_id,))
                self.db.execute_query(event_query, (source_id,))
                self.db.execute_query(strategy_query, (source_id,))

                # Commit changes to the database
                self.db.connection.commit()

                # Reload the view_data window to reflect changes
                self.view_data()

                # Close the delete window
                delete_window.destroy()
        else:
            messagebox.showwarning("No Selection", "Please select a row to delete.")

    def fetch_columns(self):
        return [
            "User ID", "Full Name", "Email", "Source ID", "Pollution Type", "Pollutant Name",
            "Pollution Description", "Country", "City", "Date", "Severity Level",
            "Pollution Activity Description", "Mitigation Strategy Name",
            "Effectiveness", "Mitigation Strategy Description"
        ]
    
    def change_data(self):
        # Fetch data from the database using the provided query
        query = """
            SELECT `user`.`user_id`, `user`.`fullName`, `user`.`email`, `source`.`source_id`, `source`.`pollutionType`, 
            `source`.`pollutantName`, `source`.`description`, `location`.`country`, `location`.`city`, `event`.`date`, 
            `event`.`severityLevel`, `event`.`description`, `mitigationstrategy`.`name`, `mitigationstrategy`.`effectiveness`, 
            `mitigationstrategy`.`description`
            FROM `user` 
            LEFT JOIN `source` ON `source`.`user_id` = `user`.`user_id` 
            LEFT JOIN `location` ON `location`.`source_id` = `source`.`source_id` 
            LEFT JOIN `event` ON `event`.`source_id` = `source`.`source_id` 
            LEFT JOIN `mitigationstrategy` ON `mitigationstrategy`.`event_id` = `event`.`event_id`
            ORDER BY `user`.`fullName`;
        """
        result = self.db.fetch_data(query)

        # Create a new window for displaying data
        change_window = tk.Toplevel(self.root)
        change_window.title("Change Data")

        # Display data in a new frame with a vertical scrollable table
        data_frame = tk.Frame(change_window, padx=20, pady=20)
        data_frame.pack()

        columns = self.fetch_columns()  # Fetch columns

        tree = ttk.Treeview(data_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        for row in result:
            tree.insert("", "end", values=row)

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(side="left", fill="both", expand=True)
        
        # Add a horizontal scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side="bottom", fill="x")

        tree.pack(side="top", fill="both", expand=True)

        # Button to edit the selected row
        edit_button = tk.Button(change_window, text="Edit Selected Row", command=lambda: self.edit_data(tree, change_window, columns))  # Pass columns
        edit_button.pack(pady=10)

    def edit_data(self, tree, edit_window, columns):
        selected_item = tree.selection()
        if selected_item:
            # Get the values of the selected row
            row_values = tree.item(selected_item, 'values')

            # Create a new window for editing data
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Data")

            # Display input fields for editing data
            edit_frame = tk.Frame(edit_window, padx=20, pady=20)
            edit_frame.pack()

            # Populate input fields with the values from the selected row
            entry_fields = []
            for i, col in enumerate(columns):
                label = tk.Label(edit_frame, text=f"{col}:")
                label.grid(row=i, column=0, sticky="e")

                entry = tk.Entry(edit_frame)
                entry.grid(row=i, column=1)
                entry.insert(0, row_values[i])  # Set default value from the selected row

                entry_fields.append(entry)

            # Button to submit the edited data
            submit_button = tk.Button(edit_frame, text="Submit Edit", command=lambda: self.submit_edit(entry_fields, tree, selected_item, edit_window))
            submit_button.grid(row=len(columns), column=1, pady=10)

        else:
            messagebox.showwarning("No Selection", "Please select a row to edit.")

    def submit_edit(self, entry_fields, tree, selected_item, edit_window):
        try:
            # Get the source_id from the selected row
            source_id = tree.item(selected_item, 'values')[3]

            # Update data in the source table
            source_query = "UPDATE source SET pollutionType = %s, pollutantName = %s, description = %s WHERE source_id = %s"
            source_data = (entry_fields[4].get(), entry_fields[5].get(), entry_fields[6].get(), source_id)
            self.db.execute_query(source_query, source_data)

            # Update data in the location table
            location_query = "UPDATE location SET country = %s, city = %s WHERE source_id = %s"
            location_data = (entry_fields[7].get(), entry_fields[8].get(), source_id)
            self.db.execute_query(location_query, location_data)

            # Update data in the event table
            event_query = "UPDATE event SET date = %s, severityLevel = %s, description = %s WHERE source_id = %s"
            event_data = (entry_fields[9].get(), entry_fields[10].get(), entry_fields[11].get(), source_id)
            self.db.execute_query(event_query, event_data)

            # Update data in the mitigationstrategy table
            strategy_query = "UPDATE mitigationstrategy SET name = %s, effectiveness = %s, description = %s WHERE event_id IN (SELECT event_id FROM event WHERE source_id = %s)"
            strategy_data = (entry_fields[12].get(), entry_fields[13].get(), entry_fields[14].get(), source_id)
            self.db.execute_query(strategy_query, strategy_data)

            # Commit changes to the database
            self.db.connection.commit()

            # Reload the view_data window to reflect changes
            self.view_data()

            # Close the edit window
            edit_window.destroy()

            # Optionally, show a success message
            messagebox.showinfo("Success", "Data edited successfully!")

        except Exception as e:
            # Display detailed error information
            messagebox.showerror("Error", f"Failed to edit data. Error: {str(e)}")

    def show_main_app(self):
        # Destroy existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a new frame for the action buttons
        action_frame = tk.Frame(self.root, padx=20, pady=20)
        action_frame.pack()

        # Display action buttons
        view_button = tk.Button(action_frame, text="View Data", command=self.view_data)
        add_button = tk.Button(action_frame, text="Add Data", command=self.add_data)
        delete_button = tk.Button(action_frame, text="Delete Data", command=self.delete_data)
        change_button = tk.Button(action_frame, text="Change Data", command=self.change_data)
        logout_button = tk.Button(action_frame, text="Logout", command=self.show_main_page)

        view_button.pack(side="top", pady=10)
        add_button.pack(side="top", pady=10)
        delete_button.pack(side="top", pady=10)
        change_button.pack(side="top", pady=10)
        logout_button.pack(side="top", pady=10)

    def show_main_page(self):
        self.root.destroy()
        self.__init__(tk.Tk())
        self.run()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.run()