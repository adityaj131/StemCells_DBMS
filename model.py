from app import db

# Model for Donors
class Donor(db.Model):
    __tablename__ = 'donor'  # Matches your database table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    hla_type = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return f"<Donor {self.first_name} {self.last_name}>"

# Model for Patients
class Patient(db.Model):
    __tablename__ = 'patient'  # Matches your database table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    hla_type = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"

# Example Model for Hospitals (Optional)
class Hospital(db.Model):
    __tablename__ = 'hospital'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f"<Hospital {self.name} in {self.city}>"

# Example Model for Staff (Optional)
class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # E.g., Doctor, Nurse
    department = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Staff {self.first_name} {self.last_name}>"
