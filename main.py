import ttkbootstrap as ttk
import mysql.connector
from ttkbootstrap.constants import *

from mysql.connector import Error
from tkinter import messagebox, StringVar


def fetch_data(query):
    """Fetch data from the database based on the given query."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="THippo3120!",
            database="audit"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except Error as err:
        messagebox.showerror("Database error", f"Error: {err}")
        return []


def execute_query(query, params=()):
    """Execute a query on the database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="THippo3120!",
            database="audit"
        )
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Entry added successfully.")
    except Error as err:
        messagebox.showerror("Database error", f"Error: {err}")


def populate_table(table, data, columns):
    """Populate a Treeview widget with data."""
    for column in columns:
        table.heading(column, text=column)
        table.column(column, anchor='center')
    for row in data:
        table.insert("", "end", values=row)

# Creating Table
def create_table_frame(parent, query, columns):
    """Create a frame containing a table displaying data from the database."""
    frame = ttk.Frame(parent)
    
    # Table widget
    table = ttk.Treeview(frame, columns=columns, show="headings", bootstyle=INFO)
    table.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Fetch and populate data
    data = fetch_data(query)
    populate_table(table, data, columns)
    
    return frame, table

# Switching between pages
def switch_frame(parent, frame):
    """Switch the displayed frame."""
    for child in parent.winfo_children():
        child.pack_forget()  # Hide all frames
    frame.pack(expand=True, fill="both")  # Show the selected frame

# Creating add entry form for location table
def create_add_entry_frame(parent, table_frame, container, main_menu):
    """Create a frame for adding a new entry to the location table."""
    frame = ttk.Frame(parent)

    # Form fields
    entries = {}
    labels = ["Business", "Address", "Contact", "Building", "Floor", "Room", "Property Type"]
    db_columns = ["business_Name", "address_Name", "contact_info", "building_Name", "floor_Num", "room_Num", "property_Type"]

    for i, label in enumerate(labels):
        ttk.Label(frame, text=label, bootstyle=INFO).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry_var = StringVar()
        ttk.Entry(frame, textvariable=entry_var, bootstyle=INFO).grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entries[db_columns[i]] = entry_var

    # Submit button
    def submit_entry():
        values = [entries[col].get() for col in db_columns]
        if any(value.strip() == "" for value in values):
            messagebox.showwarning("Validation Error", "All fields are required.")
            return
        query = """
            INSERT INTO location (business_Name, address_Name, contact_info, building_Name, floor_Num, room_Num, property_Type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(query, tuple(values))
        data = fetch_data("SELECT * FROM location")
        table_frame.delete(*table_frame.get_children())  # Clear existing rows
        for row in data:
            table_frame.insert("", "end", values=row)
        switch_frame(parent, container)

    ttk.Button(frame, text="Submit", bootstyle=SUCCESS, command=submit_entry).grid(row=len(labels), column=0, columnspan=2, pady=10)

    # Back button
    ttk.Button(frame, text="Back to Table", bootstyle=SECONDARY, command=lambda: switch_frame(parent, container)).grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

    return frame

# Creating add entry form for components table
def create_add_entry_frame_components(parent, table_frame, container, main_menu):
    """Create a frame for adding a new entry to the components table."""
    frame = ttk.Frame(parent)

    # Variables for form fields
    component_var = StringVar()
    status_var = StringVar()
    condition_var = StringVar()
    location_var = StringVar()
    last_inspected_var = StringVar()
    notes_var = StringVar()

    # Row counter
    row = 0

    # Component Name
    ttk.Label(frame, text="Component", bootstyle=INFO).grid(row=row, column=0, padx=10, pady=5, sticky="e")
    ttk.Entry(frame, textvariable=component_var, bootstyle=INFO).grid(row=row, column=1, padx=10, pady=5, sticky="w")
    row += 1

    # Status (Radio Buttons)
    ttk.Label(frame, text="Status", bootstyle=INFO).grid(row=row, column=0, padx=10, pady=5, sticky="e")
    status_options = ["Open", "In Progress", "Closed"]
    status_var.set(status_options[0])  # Default value
    for idx, option in enumerate(status_options):
        ttk.Radiobutton(frame, text=option, variable=status_var, value=option, bootstyle=INFO).grid(row=row, column=1+idx, padx=5, pady=5, sticky="w")
    row += 1

    # Condition (Radio Buttons)
    ttk.Label(frame, text="Condition", bootstyle=INFO).grid(row=row, column=0, padx=10, pady=5, sticky="e")
    condition_options = ["Bad", "Fair", "Good", "Excellent"]
    condition_var.set(condition_options[0])  # Default value
    for idx, option in enumerate(condition_options):
        ttk.Radiobutton(frame, text=option, variable=condition_var, value=option, bootstyle=INFO).grid(row=row, column=1+idx, padx=5, pady=5, sticky="w")
    row += 1

    # Location (Combobox)
    ttk.Label(frame, text="Location", bootstyle=INFO).grid(row=row, column=0, padx=10, pady=5, sticky="e")
    locations = fetch_data("SELECT location_ID, business_Name FROM location")
    location_options = [f"{loc[0]} - {loc[1]}" for loc in locations]
    location_var.set(location_options[0] if location_options else "")
    ttk.Combobox(frame, textvariable=location_var, values=location_options, bootstyle=INFO).grid(row=row, column=1, padx=10, pady=5, sticky="w")
    row += 1

    # Last Inspected
    ttk.Label(frame, text="Last Inspected", bootstyle=INFO).grid(row=row, column=0, padx=10, pady=5, sticky="e")
    ttk.Entry(frame, textvariable=last_inspected_var, bootstyle=INFO).grid(row=row, column=1, padx=10, pady=5, sticky="w")
    row += 1

    # Notes
    ttk.Label(frame, text="Notes", bootstyle=INFO).grid(row=row, column=0, padx=10, pady=5, sticky="e")
    ttk.Entry(frame, textvariable=notes_var, bootstyle=INFO).grid(row=row, column=1, padx=10, pady=5, sticky="w")
    row += 1

    # Submit button
    def submit_entry():
        component = component_var.get()
        status = status_var.get()
        condition = condition_var.get()
        location_selection = location_var.get()
        last_inspected = last_inspected_var.get()
        notes = notes_var.get()

        # Extract location_ID from location selection
        if location_selection:
            location_ID = location_selection.split(" - ")[0]
        else:
            location_ID = None

        # Validate required fields
        if not all([component.strip(), status.strip(), condition.strip(), location_ID, last_inspected.strip()]):
            messagebox.showwarning("Validation Error", "All fields except 'Notes' are required.")
            return

        # Prepare and execute the INSERT query
        query = """
            INSERT INTO components (component_Name, component_Status, component_Condition, location_ID, last_Inspected, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (component, status, condition, location_ID, last_inspected, notes)

        execute_query(query, params)

        # Update the components table display
        data = fetch_data("SELECT * FROM components")
        table_frame.delete(*table_frame.get_children())  # Clear existing rows
        for row_data in data:
            table_frame.insert("", "end", values=row_data)

        # Switch back to the table view
        switch_frame(parent, container)

    ttk.Button(frame, text="Submit", bootstyle=SUCCESS, command=submit_entry).grid(row=row, column=0, columnspan=2, pady=10)
    row += 1

    # Back button
    ttk.Button(frame, text="Back to Table", bootstyle=SECONDARY, command=lambda: switch_frame(parent, container)).grid(row=row, column=0, columnspan=2, pady=10)

    return frame


def main():
    root = ttk.Window(themename="darkly")
    root.title("Electrical Safety Audit")
    root.geometry("800x600")

    container = ttk.Frame(root)
    container.pack(expand=True, fill="both")

    main_menu = ttk.Frame(container)
    main_menu.pack(expand=True, fill="both")

    # Location
    location_frame, location_table = create_table_frame(
        container,
        "SELECT * FROM location",
        ["ID", "Business", "Address", "Contact", "Building", "Floor", "Room #", "Property Type"]
    )

    add_entry_frame = create_add_entry_frame(
        container,
        location_table,
        location_frame,
        main_menu
    )

    # Components
    components_frame, components_table = create_table_frame(
        container,
        "SELECT * FROM components",
        ["ID", "Component", "Status", "Condition", "Location", "Last Inspected", "Notes"]
    )

    add_entry_frame_components = create_add_entry_frame_components(
        container,
        components_table,
        components_frame,
        main_menu
    )

    # Inspection
    inspection_frame, _ = create_table_frame(
        container,
        "SELECT * FROM inspection",
        ["ID", "Component", "Type", "Inspector", "Date", "Issue", "Solution", "Status", "Upcoming"]
    )

    # Create a custom style for orange button
    orange_style = ttk.Style()
    orange_style.configure(
        "Custom.Orange.TButton",
        background="#FF7A00",  # Orange color
        foreground="white",    # Text color
        font=("Helvetica", 14),  # Adjust font size
        borderwidth=5,
        relief="solid"
    )

    # Custom Title styling
    label_style = ttk.Style()
    label_style.configure(
        "Custom.TLabel",
        foreground="#ff7a00",  # Set label text color to #ff7a00
        font=("Helvetica", 12)
    )

    # Hover effects
    orange_style.map(
        "Custom.Orange.TButton",
        background=[("active", "#B65700")],
        foreground=[("active", "white")],
        bordercolor=[("!disabled", "#000")]
    )

    # Title
    ttk.Label(
        main_menu,
        text="Select a Table to View",
        style="Custom.TLabel",
        font=("Helvetica", 18),
        bootstyle=INFO
    ).pack(pady=100)

    # Location button
    ttk.Button(
        main_menu,
        text="Location",
        style="Custom.Orange.TButton",
        command=lambda: switch_frame(container, location_frame)
    ).pack(pady=10)

    # Add Entry button Location Frame
    ttk.Button(
        location_frame,
        text="Add Entry",
        bootstyle=SUCCESS,
        command=lambda: switch_frame(container, add_entry_frame)
    ).pack(side="left", padx=10, pady=10)

    # Components button
    ttk.Button(
        main_menu,
        text="Components",
        style="Custom.Orange.TButton",
        command=lambda: switch_frame(container, components_frame)
    ).pack(pady=10)

    # Add "Add Entry" button to Components Frame
    ttk.Button(
        components_frame,
        text="Add Entry",
        bootstyle=SUCCESS,
        command=lambda: switch_frame(container, add_entry_frame_components)
    ).pack(side="left", padx=10, pady=10)

    # Inspection button
    ttk.Button(
        main_menu,
        text="Inspection",
        style="Custom.Orange.TButton",
        command=lambda: switch_frame(container, inspection_frame)
    ).pack(pady=10)

    for frame, _ in [(location_frame, location_table), (components_frame, None), (inspection_frame, None)]:
        ttk.Button(
            frame,
            text="Back to Main Menu",
            bootstyle=SECONDARY,
            command=lambda: switch_frame(container, main_menu)
        ).pack(pady=10)

    switch_frame(container, main_menu)

    root.mainloop()

if __name__ == "__main__":
    main()