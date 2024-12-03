import ttkbootstrap as ttk
import mysql.connector
from ttkbootstrap.constants import *
from mysql.connector import Error
from tkinter import messagebox

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

def populate_table(table, data, columns):
    """Populate a Treeview widget with data."""
    for column in columns:
        table.heading(column, text=column)
        table.column(column, anchor='center')
    for row in data:
        table.insert("", "end", values=row)

def create_table_frame(parent, query, columns):
    """Create a frame containing a table displaying data from the database."""
    frame = ttk.Frame(parent)
    
    # Table widget
    table = ttk.Treeview(frame, columns=columns, show="headings", bootstyle=INFO)
    table.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Fetch and populate data
    data = fetch_data(query)
    populate_table(table, data, columns)
    
    return frame

def switch_frame(parent, frame):
    """Switch the displayed frame."""
    for child in parent.winfo_children():
        child.pack_forget()  # Hide all frames
    frame.pack(expand=True, fill="both")  # Show the selected frame

# Main application window
def main():
    # Create a ttkbootstrap window
    root = ttk.Window(themename="darkly")
    root.title("Electrical Safety Audit")
    root.geometry("800x600")  # Set a larger window size for better usability
    
    # Main container for frames
    container = ttk.Frame(root)
    container.pack(expand=True, fill="both")

    # Create frames for each table
    location_frame = create_table_frame(
        container,
        "SELECT * FROM location",
        ["ID", "Business", "Address", "Contact", "Building", "Floor", "Room #", "Property Type"]
    )
    
    components_frame = create_table_frame(
        container,
        "SELECT * FROM components",
        ["ID", "Component", "Status", "Condition", "Location", "Last Inspection", "Notes"]
    )
    
    inspection_frame = create_table_frame(
        container,
        "SELECT * FROM inspection",
        ["ID", "Component", "Type", "Inspector", "Date", "Issue", "Solution", "Status", "Upcoming"]
    )

    # Create a button panel for switching frames
    button_panel = ttk.Frame(root, bootstyle=PRIMARY)
    button_panel.pack(fill="x")

    ttk.Button(button_panel, text="Location", bootstyle=INFO, command=lambda: switch_frame(container, location_frame)).pack(side="left", padx=5, pady=5)
    ttk.Button(button_panel, text="Components", bootstyle=INFO, command=lambda: switch_frame(container, components_frame)).pack(side="left", padx=5, pady=5)
    ttk.Button(button_panel, text="Inspection", bootstyle=INFO, command=lambda: switch_frame(container, inspection_frame)).pack(side="left", padx=5, pady=5)
    
    # Start with the first frame displayed
    switch_frame(container, location_frame)
    
    root.mainloop()

if __name__ == "__main__":
    main()