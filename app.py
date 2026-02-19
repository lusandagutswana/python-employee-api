from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, init_db
from models import Employee

app = Flask(__name__)
CORS(app)

init_db(app)


def error_response(message, status_code):
    return jsonify({'error': message}), status_code


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'Employee API'})


# Create a new employee
@app.route('/api/employees', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return error_response(f'{field} is required', 400)

        # Check if email already exists
        if Employee.query.filter_by(email=data['email']).first():
            return error_response('Email already exists', 400)

        # Create new employee
        employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            department=data.get('department'),
            position=data.get('position'),
            salary=data.get('salary')
        )

        db.session.add(employee)
        db.session.commit()

        return jsonify({
            'message': 'Employee created successfully',
            'employee': employee.to_dict()
        }), 201

    except Exception as e:
        return error_response(str(e), 500)


# Get all employees
@app.route('/api/employees', methods=['GET'])
def get_all_employees():
    try:
        employees = Employee.query.all()
        return jsonify({
            'count': len(employees),
            'employees': [emp.to_dict() for emp in employees]
        })
    except Exception as e:
        return error_response(str(e), 500)


# Get a single employee by ID
@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return error_response('Employee not found', 404)

        return jsonify(employee.to_dict())
    except Exception as e:
        return error_response(str(e), 500)


# Update an employee
@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return error_response('Employee not found', 404)

        data = request.get_json()

        # Update fields if provided
        if 'first_name' in data:
            employee.first_name = data['first_name']
        if 'last_name' in data:
            employee.last_name = data['last_name']
        if 'email' in data and data['email'] != employee.email:
            # Check if new email already exists
            if Employee.query.filter_by(email=data['email']).first():
                return error_response('Email already exists', 400)
            employee.email = data['email']
        if 'department' in data:
            employee.department = data['department']
        if 'position' in data:
            employee.position = data['position']
        if 'salary' in data:
            employee.salary = data['salary']

        db.session.commit()

        return jsonify({
            'message': 'Employee updated successfully',
            'employee': employee.to_dict()
        })

    except Exception as e:
        return error_response(str(e), 500)


# Delete an employee
@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return error_response('Employee not found', 404)

        db.session.delete(employee)
        db.session.commit()

        return jsonify({
            'message': 'Employee deleted successfully'
        })
    except Exception as e:
        return error_response(str(e), 500)


# Search employees by department
@app.route('/api/employees/search', methods=['GET'])
def search_employees():
    try:
        department = request.args.get('department')
        position = request.args.get('position')

        query = Employee.query

        if department:
            query = query.filter(Employee.department.ilike(f'%{department}%'))
        if position:
            query = query.filter(Employee.position.ilike(f'%{position}%'))

        employees = query.all()

        return jsonify({
            'count': len(employees),
            'employees': [emp.to_dict() for emp in employees]
        })
    except Exception as e:
        return error_response(str(e), 500)

    app.run(debug=True, host='0.0.0.0', port=5000)
