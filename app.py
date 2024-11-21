from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime, date
project=mysql.connector.connect(
    host="localhost",
    user="root",
    password="qwerty123",
    database="dbms"
)

cursor=project.cursor()

app = Flask(__name__)
from datetime import date

def calculate_age(dob):
    if isinstance(dob, str):
        # Convert string to datetime.date
        dob = datetime.strptime(dob, "%Y-%m-%d").date()
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
def get_next_donor_id(cursor):
    cursor.execute("SELECT IFNULL(MAX(D_Id), 0) + 1 AS next_id FROM donor")
    result = cursor.fetchone()
    return result[0]
def get_next_region_id(cursor):
    cursor.execute("SELECT IFNULL(MAX(R_Id), 0) + 1 AS next_id FROM donor")
    result = cursor.fetchone()
    return result[0]

def get_next_patient_id(cursor):
    cursor.execute("SELECT IFNULL(MAX(P_Id), 0) + 1 AS next_id FROM patient")
    result = cursor.fetchone()
    return result[0]

def get_next_manager_id(cursor):
    cursor.execute("SELECT IFNULL(MAX(M_Id), 0) + 1 AS next_id FROM patient")
    result = cursor.fetchone()
    return result[0]
def ensure_manager_exists(cursor, manager_id):
    # Check if the manager ID already exists
    cursor.execute("SELECT COUNT(*) FROM manager WHERE M_Id = %s", (manager_id,))
    result = cursor.fetchone()

    # If not, insert a new manager record
    if result[0] == 0:
        cursor.execute("INSERT INTO manager (M_Id) VALUES (%s)", (manager_id,))
def ensure_rec_staff_exists(cursor, region_id):
    # Check if the region ID already exists in rec_staff table
    cursor.execute("SELECT COUNT(*) FROM rec_staff WHERE R_Id = %s", (region_id,))
    result = cursor.fetchone()

    # If the region ID doesn't exist, insert it into rec_staff table
    if result[0] == 0:
        cursor.execute("INSERT INTO rec_staff (R_Id) VALUES (%s)", (region_id,))
def ensure_city_exists(cursor, city_id):
    cursor.execute("SELECT COUNT(*) FROM city WHERE City_Id = %s", (city_id,))
    result = cursor.fetchone()
    if result[0] == 0:
        cursor.execute("INSERT INTO city (City_Id) VALUES (%s)", (city_id,))
def get_next_hospital_id(cursor):
    cursor.execute("SELECT IFNULL(MAX(Hosp_Id), 0) + 1 AS next_id FROM hospital")
    result = cursor.fetchone()
    return result[0]
def get_next_staff_id(cursor):
    cursor.execute("SELECT IFNULL(MAX(R_Id), 0) + 1 AS next_id FROM rec_staff")
    result = cursor.fetchone()
    return result[0]

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/')
def index1():
    # Fetch the count for Total Donors, Total Patients, Hospitals, and Staff Members

    # For Total Donors
    cursor.execute("SELECT COUNT(*) FROM donor")
    total_donors = cursor.fetchone()[0] if cursor.fetchone()[0] else 25

    # For Total Patients
    cursor.execute("SELECT COUNT(*) FROM patient")
    total_patients = cursor.fetchone()[0] if cursor.fetchone()[0] else 25

    # For Total Hospitals
    cursor.execute("SELECT COUNT(*) FROM hospital")
    total_hospitals = cursor.fetchone()[0] if cursor.fetchone()[0] else 25

    # For Total Staff Members
    cursor.execute("SELECT COUNT(*) FROM rec_staff")
    total_staff = cursor.fetchone()[0] if cursor.fetchone()[0] else 25

    # Pass the values to the template
    return render_template('index1.html', total_donors=total_donors, 
                           total_patients=total_patients, 
                           total_hospitals=total_hospitals, 
                           total_staff=total_staff)



@app.route('/donors', methods=['GET', 'POST'])
def donors():
    if request.method == 'POST':
        # Handle donor registration (existing functionality)
        f_name = request.form.get('d-fname')
        l_name = request.form.get('d-lname')
        sex = request.form.get('d-sex')
        dob = request.form.get('d-dob')
        bg = request.form.get('d-blood')
        hla = request.form.get('d-hla')
        phone = request.form.get('d-phone')
        city_id = request.form.get('d-city')
        age = calculate_age(dob)

        next_id = get_next_donor_id(cursor)
        next_region_id = get_next_region_id(cursor)

        ensure_city_exists(cursor, city_id)
        ensure_rec_staff_exists(cursor, next_region_id)

        try:
            cursor.execute('''
                INSERT INTO donor(D_Id, Fname, Lname, Sex, DOB, Age, B_group, D_Phno, HLA, City_Id, R_Id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (next_id, f_name, l_name, sex, dob, age, bg, phone, hla, city_id, next_region_id))
            project.commit()
            message = "Donor registered successfully!"
        except Exception as e:
            print(f"Error inserting donor: {e}")
            message = "Failed to register donor. Please check the inputs."

        return render_template('donors.html', message=message)

    # Handle sorting and filtering (GET request)
    filter_bg = request.args.get('filter_bg', '')  # Blood Group filter
    filter_hla = request.args.get('filter_hla', '')  # HLA filter
    sort_by = request.args.get('sort_by', 'D_Id')  # Default sorting column
    sort_order = request.args.get('sort_order', 'ASC')  # Default sorting order

    # Construct SQL query with dynamic filters and sorting
    query = "SELECT * FROM donor WHERE 1=1"
    params = []

    if filter_bg:
        query += " AND B_group = %s"
        params.append(filter_bg)
    if filter_hla:
        query += " AND HLA LIKE %s"
        params.append(f"%{filter_hla}%")

    query += f" ORDER BY {sort_by} {sort_order}"

    # Execute the query
    cursor.execute(query, params)
    donors = cursor.fetchall()

    return render_template('donors.html', donors=donors)


@app.route('/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'POST':
        # Handle patient registration (existing functionality)
        f_name = request.form.get('p-fname')
        l_name = request.form.get('p-lname')
        sex = request.form.get('p-sex')
        dob = request.form.get('p-dob')
        bg = request.form.get('p-blood')
        hla = request.form.get('p-hla')
        phone = request.form.get('p-phone')
        city_id = request.form.get('p-city')  # Optional field
        region_id = request.form.get('p-region')  # Optional field

        # Calculate age from date of birth
        age = calculate_age(dob)

        # Generate IDs
        next_patient_id = get_next_patient_id(cursor)
        next_manager_id = get_next_manager_id(cursor)  # Generate Manager ID if needed

        # Ensure the region (R_Id) exists in rec_staff table
        ensure_rec_staff_exists(cursor, region_id)

        # Ensure manager exists in the manager table
        ensure_manager_exists(cursor, next_manager_id)

        # Insert patient into the database
        try:
            cursor.execute('''
                INSERT INTO patient(P_Id, Fname, Lname, Sex, DOB, Age, B_group, HLA, Phno, City_Id, R_Id, M_Id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (next_patient_id, f_name, l_name, sex, dob, age, bg, hla, phone, city_id, region_id, next_manager_id))
            project.commit()
            message = "Patient registered successfully!"
        except Exception as e:
            print(f"Error inserting patient: {e}")
            message = "Failed to register patient. Please check the inputs."

        return render_template('patients.html', message=message)

    # Handle filtering and sorting (GET request)
    filter_bg = request.args.get('filter_bg', '')  # Blood Group filter
    filter_hla = request.args.get('filter_hla', '')  # HLA filter
    sort_by = request.args.get('sort_by', 'P_Id')  # Default sorting column
    sort_order = request.args.get('sort_order', 'ASC')  # Default sorting order

    # Construct SQL query with dynamic filters and sorting
    query = "SELECT * FROM patient WHERE 1=1"
    params = []

    if filter_bg:
        query += " AND B_group = %s"
        params.append(filter_bg)
    if filter_hla:
        query += " AND HLA LIKE %s"
        params.append(f"%{filter_hla}%")

    query += f" ORDER BY {sort_by} {sort_order}"

    # Execute the query
    cursor.execute(query, params)
    patients = cursor.fetchall()

    return render_template('patients.html', patients=patients)


@app.route('/hospitals', methods=['GET', 'POST'])
def hospitals():
    if request.method == 'POST':
        # Get form data
        h_name = request.form.get('h-name')
        h_phone = request.form.get('h-phone')
        city_id = request.form.get('h-city')  # City ID
        manager_id = request.form.get('h-manager')  # Manager ID

        # Ensure the manager (M_Id) exists in the manager table
        ensure_manager_exists(cursor, manager_id)

        # Ensure the city (City_Id) exists in the city table (if applicable)
        ensure_city_exists(cursor, city_id)

        # Generate the next Hospital ID (assuming auto-incremented by DB)
        next_hospital_id = get_next_hospital_id(cursor)

        # Insert hospital data into the database
        cursor.execute('''
            INSERT INTO hospital(Hosp_Id, Hosp_name, Hosp_Phno, City_Id, M_Id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (next_hospital_id, h_name, h_phone, city_id, manager_id))
        project.commit()

        # Debugging output
        print(f"Hospital Name: {h_name}")
        print(f"Manager ID: {manager_id}")
        print(f"City ID: {city_id}")

        # Return success or failure message
        if not h_name:
            print("Form data not received!") 
            return render_template('hospital.html', message="Failed to register hospital.")

        return render_template('hospital.html', message="Hospital registered successfully!")

    # Render the hospital registration form
    return render_template('hospital.html')


@app.route('/staff', methods=['GET', 'POST'])
def staff():
    if request.method == 'POST':
        # Get form data
        r_name = request.form.get('r-name')
        r_phone = request.form.get('r-phone')

        # Generate the next Staff ID (assuming auto-increment by DB)
        next_staff_id = get_next_staff_id(cursor)

        # Insert staff data into the database
        cursor.execute('''
            INSERT INTO rec_staff(R_Id, R_Name, Ph_no)
            VALUES (%s, %s, %s)
        ''', (next_staff_id, r_name, r_phone))
        project.commit()

        # Debugging output
        print(f"Staff Name: {r_name}")
        print(f"Phone Number: {r_phone}")
        if not r_name:
            print("Form data not received!") 
            return render_template('staff.html', message="Failed to register staff.")

        return render_template('staff.html', message="Staff registered successfully!")

    # Render the staff registration form
    return render_template('staff.html')

if __name__ == '__main__':
    app.run(debug=True)