from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
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
    except mysql.connector.Error as err:
        return {"error": str(err)}
    
@app.route('/')
def index():
    """Home page with navigation to different tables."""
    return render_template("index.html")

@app.route('/location')
def location():
    """Location table."""
    query = "SELECT * FROM location"
    data = fetch_data(query)
    columns = ["component_ID", "component_Name", "component_Status", 
               "component_Condition", "location_ID", "last_Inspected", "notes"]
    return render_template("components.html", data=data, columns=columns)

@app.route('/components')
def components():
    """Components table."""
    query = "SELECT * FROM components"
    data = fetch_data(query)
    columns = ["location_ID", "business_Name", "address_Name", "contact_Info", 
               "building_Name", "floor_Num", "room_Num", "property_Type"]
    return render_template("location.html", data=data, columns=columns)

@app.route('/inspection')
def inspection():
    """Inspection table."""
    query = "SELECT * FROM inspection"
    data = fetch_data(query)
    columns = ["inspection_ID", "component_ID", "inspection_type", 
               "inspection_Name", "inspection_Date", "issue_Description", 
               "resolution_Description", "inspection_Status", "next_Inspection"]
    return render_template("inspection.html", data=data, columns=columns)

if __name__ == '__main__':
    app.run(debug=True)