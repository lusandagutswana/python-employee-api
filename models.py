from database import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(50))
    position = db.Column(db.String(50))
    salary = db.Column(db.Float)
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'department': self.department,
            'position': self.position,
            'salary': self.salary,
            'hire_date': self.hire_date.strftime('%Y-%m-%d') if self.hire_date else None
        }

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'