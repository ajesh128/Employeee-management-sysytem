from io import StringIO
from flask import Blueprint, Response,jsonify, make_response
from flask import request
import pandas
from flask_jwt_extended import jwt_required

from apps.decorators import validate_request

DATABASE = "apps/database.db"
import sqlite3
from flask import g
test_module = Blueprint("employee_module", __name__, url_prefix="/employee")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@test_module.route("/insert", methods=["POST"])
@jwt_required()
@validate_request("name", "age","department","email")
def employee_insertion_api():
    """
    TO INSERT EMPLOYEE DETAILS TO EMPLOYEE TABLE

    Returns:
        str: message
    """
    try:
        db = get_db()
        cursor = db.cursor()
        name = request.json.get("name")
        age = request.json.get("age")
        department = request.json.get("department")
        email = request.json.get("email")
        try:
            # To insert in to employee
            cursor.execute("""
            INSERT INTO Employee (name, email, age, department)
            VALUES (?, ?, ?, ?)
        """, (name, email, age, department))
            db.commit()
            db.close()
        except sqlite3.IntegrityError as e:
            db.close()
            return jsonify(message = "email already exist")

        return jsonify(message = "inserted"),200
    except Exception as exc:
        print(f"error occure in inserting function {exc}")
        db.close()

@test_module.route("/get/employee", methods=["GET"])
@jwt_required()
def get_employee():
    """
    TO GET ALL THE EMPLOYEE DETAILS OR FOR THE SPECIFIC DEPARTMENT

    Returns:
        list: Containing information of employees
    """
    try:
        db = get_db()
        cursor = db.cursor()
        # SETTING THE LIMIT
        limit = 2
        offset = request.args.get("offset",0)
        if offset == 0:
            offset = 1
        # SETTING THE OFFSET VALUE
        offset = (int(offset) - 1) * limit
        department = request.args.get("department",None)
        # Query to fetch employee details
        cursor.execute("SELECT * FROM Employee WHERE(? is NULL OR department = ?) LIMIT ? OFFSET ?",(department,department,limit,offset))
        employee_data = cursor.fetchall()
        db.close()
        if employee_data:
            return jsonify(message = employee_data),200
        else:
            return jsonify(message = "Not found"),404
    except Exception as exc:
        print(f"error occured in get employee function {exc}")
        db.close()
    

@test_module.route("/update", methods=["PUT"])
@jwt_required()
def update_employee():
    """
    TO update the employee based on id

    Returns:
        string: updated,invalid id,or email already exist
    """
    try:
        db = get_db()
        cursor = db.cursor()
        id = request.args.get("id")
        if not request.is_json or not request.json or not id:
            db.close()
            return jsonify(message ="mandatory field required"),400
        new_name = request.json.get("name")
        updating_filed_list = []
        field_list = []
        email = request.json.get("email")
        department = request.json.get("department")
        # checking email
        if email:
            updating_filed_list.append(email)
            field_list.append("email = ?")
        # checking name
        if new_name:
            updating_filed_list.append(new_name)
            field_list.append("name = ?")
        # checking department
        if department:
            updating_filed_list.append(new_name)
            field_list.append("name = ?")
        if updating_filed_list:
            updating_filed_list.append(id)
            try:
                sql = f"UPDATE Employee SET {', '.join(field_list)} WHERE id = ?"
                cursor.execute(sql, updating_filed_list)
                db.commit()
                db.close()
            except sqlite3.IntegrityError as e:
                db.close()
                return jsonify(message = "email already exist")
            if cursor.rowcount == 0:
                return jsonify(message = "invalid id"),404
            return jsonify(message = "updated"),200
    except Exception as exc:
        print("error occured in update_employee")
        db.close()


@test_module.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_employe():
    """
    TO DELETE AN EMPLOYEE

    Returns:
        string: deleted or invalid id
    """
    try:
        db = get_db()
        cursor = db.cursor()
        id = request.args.get("id")
        if not id:
            return jsonify (message = "mandatory field required"),400
        # deleting employee
        cursor.execute("DELETE FROM Employee where id = ?",(id,))
        if cursor.rowcount == 0:
            return jsonify(message = "invalid id"),404
        db.commit()
        db.close()
        return jsonify(message = "deleted"),200
    except Exception as exc:
        print(f'error occure in delete function {exc}')
        db.close()

@test_module.route("/csv", methods=["POST"])
@jwt_required()
def export_csv():
    """
    TO RETURN CSV RESPONSE WHICH IS FETCHED FROM Employee table

    Returns:
        file: csv
    """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Employee")
        employeed_data = cursor.fetchall()
        db.close()
        if employeed_data:
            csv_buffer = StringIO()
            # converting in to csv
            df = pandas.DataFrame(employeed_data, columns=['id', 'name', 'email', 'age', 'password'])
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()

            # make Flask response
            response = make_response(csv_data)
            response.headers["Content-Disposition"] = "attachment; filename=employee.csv"
            response.headers["Content-Type"] = "text/csv"
            return response
            
    except Exception as exc:
        print(f"error occured in export csv,{exc}")
        db.close()




