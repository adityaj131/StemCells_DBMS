Project Overview
This project is a Donor, Patient, Hospital, and Staff Management System developed using Flask (Python web framework) and MySQL as the database management system (DBMS). The system allows users to register new donors, patients, hospitals, and staff members while keeping track of the current counts of each entity on the dashboard. The dashboard updates dynamically whenever a new entry is registered.

Features
Dashboard:
! Displays the count of total donors, patients, hospitals, and staff members.
! Initial count starts from 25, and the count updates dynamically after every registration.

Registration Forms:
! Donors: Allows users to register new donors by entering basic information (name, blood group, HLA type, etc.).
! Patients: Allows users to register new patients, including their details and associated manager/region information.
! Hospitals: Allows registration of hospital details with a manager ID and city.
! Staff Members: Allows registering staff members responsible for managing donors, patients, and hospitals.

Data Persistence:
! Uses MySQL to store donor, patient, hospital, and staff data.
! Supports basic CRUD (Create, Read, Update, Delete) operations through forms.

Prerequisites:
! Python 3.12.7
! Flask 2.0.1 (Prefer)
! MySQL Workbench
! MySQL Server (Database)
! MySQL Connector for Python
! Install MySQL Connector: pip install mysql-connector-python
! Bootstrap 5 (for front-end design)

DONE BY: 
Ashna, Aditya, Rishabh, Harshil, Pratosh