
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

employees = {}

TASKS = {
    "documents": "Document Collection",
    "verification": "Employee Verification",
    "it_setup": "IT Setup",
    "training": "Training"
}

print("HR Employee Onboarding System initialized successfully!")


# Agent 1: Document Collection
def document_agent(employee):
    return "Completed" if employee["documents"] else "Pending"


# Agent 2: Employee Verification
def verification_agent(employee):
    return "Completed" if employee["verification"] else "Pending"


# Agent 3: IT Setup
def it_setup_agent(employee):
    return "Completed" if employee["it_setup"] else "Pending"


# Agent 4: Training
def training_agent(employee):
    return "Completed" if employee["training"] else "Pending"


# Coordinator Agent
def coordinator_agent(employee):
    task_status = {
        "Document Collection": document_agent(employee),
        "Employee Verification": verification_agent(employee),
        "IT Setup": it_setup_agent(employee),
        "Training": training_agent(employee)
    }

    completed_tasks = 0

    for status in task_status.values():
        if status == "Completed":
            completed_tasks += 1

    progress = int(completed_tasks / len(task_status) * 100)

    overall_status = "Completed" if progress == 100 else "In Progress"

    return {
        "tasks": task_status,
        "progress": progress,
        "status": overall_status
    }


# Employee Registration Page
HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>HR Employee Onboarding</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; }

        body {
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            margin: 0;
            padding: 30px;
            color: #263445;
        }

        .container {
            max-width: 850px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 3px 12px #00000010;
        }

        h1, h2 { color: #243b64; }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 18px;
        }

        label {
            display: block;
            margin-bottom: 7px;
            font-weight: bold;
        }

        input, select {
            width: 100%;
            padding: 11px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
        }

        button, .button {
            display: inline-block;
            background: #3157a4;
            color: white;
            border: none;
            padding: 12px 18px;
            border-radius: 6px;
            cursor: pointer;
            text-decoration: none;
            margin-top: 22px;
        }

        .secondary {
            background: #e8eef9;
            color: #3157a4;
            margin-left: 8px;
        }

        .error {
            background: #ffe5e5;
            color: #a11;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 18px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Employee Onboarding</h1>
    <p>Enter the new employee's information below.</p>

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}

    <form action="/add" method="POST">
        <div class="form-grid">
            <div>
                <label>Employee ID</label>
                <input name="emp_id" required placeholder="EMP001">
            </div>

            <div>
                <label>Full Name</label>
                <input name="name" required>
            </div>

            <div>
                <label>Email</label>
                <input type="email" name="email" required>
            </div>

            <div>
                <label>Phone</label>
                <input type="tel" name="phone" required>
            </div>

            <div>
                <label>Department</label>
                <select name="department" required>
                    <option value="">Select department</option>
                    <option>Engineering</option>
                    <option>Human Resources</option>
                    <option>Finance</option>
                    <option>Marketing</option>
                    <option>Sales</option>
                    <option>Operations</option>
                </select>
            </div>

            <div>
                <label>Job Role</label>
                <input name="role" required>
            </div>

            <div>
                <label>Joining Date</label>
                <input type="date" name="joining_date" required>
            </div>

            <div>
                <label>Employment Type</label>
                <select name="employment_type" required>
                    <option value="">Select type</option>
                    <option>Full-time</option>
                    <option>Part-time</option>
                    <option>Intern</option>
                    <option>Contract</option>
                </select>
            </div>

            <div>
                <label>Reporting Manager</label>
                <input name="manager" required>
            </div>

            <div>
                <label>Work Location</label>
                <input name="location" required>
            </div>
        </div>

        <button type="submit">Register Employee</button>
        <a class="button secondary" href="/dashboard">View Dashboard</a>
    </form>
</div>
</body>
</html>
"""


# Add Employee
@app.route("/")
def home():
    return render_template_string(HOME_PAGE, error=None)


@app.route("/add", methods=["POST"])
def add_employee():
    emp_id = request.form.get("emp_id", "").strip().upper()

    if not emp_id:
        return render_template_string(
            HOME_PAGE, error="Employee ID is required."
        ), 400

    if emp_id in employees:
        return render_template_string(
            HOME_PAGE, error="Employee ID already exists. Use another ID."
        ), 400

    employees[emp_id] = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "department": request.form.get("department", ""),
        "role": request.form.get("role", "").strip(),
        "joining_date": request.form.get("joining_date", ""),
        "employment_type": request.form.get("employment_type", ""),
        "manager": request.form.get("manager", "").strip(),
        "location": request.form.get("location", "").strip(),
        "documents": False,
        "verification": False,
        "it_setup": False,
        "training": False
    }

    return redirect(url_for("dashboard"))


# Dashboard Page
DASHBOARD_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>HR Onboarding Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            padding: 30px;
            color: #263445;
        }

        .container { max-width: 1200px; margin: auto; }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        h1, h2 { color: #243b64; }

        .button {
            background: #3157a4;
            color: white;
            padding: 12px 16px;
            border-radius: 6px;
            text-decoration: none;
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-top: 25px;
            box-shadow: 0 3px 12px #00000010;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 850px;
        }

        th, td {
            padding: 13px;
            text-align: left;
            border-bottom: 1px solid #e5e9f0;
        }

        th { background: #edf2fa; }

        .progress {
            width: 100px;
            height: 10px;
            background: #e1e7ef;
            border-radius: 10px;
            overflow: hidden;
        }

        .bar { height: 10px; background: #28a879; }

        .status {
            padding: 6px 9px;
            border-radius: 12px;
            background: #fff0cf;
            color: #895c00;
            font-size: 12px;
        }

        .completed {
            background: #d8f5e7;
            color: #126b47;
        }

        .details {
            color: #3157a4;
            font-weight: bold;
            text-decoration: none;
        }

        .empty {
            text-align: center;
            padding: 25px;
            color: #68778b;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div>
            <h1>Employee Onboarding Dashboard</h1>
            <p>Manage employee details and onboarding progress.</p>
        </div>
        <a class="button" href="/">+ Register Employee</a>
    </div>

    <div class="card">
        <h2>Registered Employees</h2>
        <table>
            <tr>
                <th>Employee ID</th>
                <th>Name</th>
                <th>Department</th>
                <th>Role</th>
                <th>Joining Date</th>
                <th>Progress</th>
                <th>Status</th>
                <th>Details</th>
            </tr>

            {% for emp_id, emp in employees.items() %}
                {% set report = coordinator_agent(emp) %}
                <tr>
                    <td>{{ emp_id }}</td>
                    <td>{{ emp.name }}</td>
                    <td>{{ emp.department }}</td>
                    <td>{{ emp.role }}</td>
                    <td>{{ emp.joining_date }}</td>
                    <td>
                        <div class="progress">
                            <div class="bar"
                                 style="width: {{ report.progress }}%;"></div>
                        </div>
                        {{ report.progress }}%
                    </td>
                    <td>
                        <span class="status {% if report.status == 'Completed' %}completed{% endif %}">
                            {{ report.status }}
                        </span>
                    </td>
                    <td>
                        <a class="details"
                           href="{{ url_for('employee_details', emp_id=emp_id) }}">
                            View
                        </a>
                    </td>
                </tr>
            {% else %}
                <tr>
                    <td colspan="8" class="empty">
                        No employees registered yet.
                    </td>
                </tr>
            {% endfor %}
        </table>
    </div>
</div>
</body>
</html>
"""


@app.route("/dashboard")
def dashboard():
    return render_template_string(
        DASHBOARD_PAGE,
        employees=employees,
        coordinator_agent=coordinator_agent
    )


# Employee Details and Task Management Page
EMPLOYEE_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Employee Details</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            padding: 30px;
            color: #263445;
        }

        .container { max-width: 950px; margin: auto; }

        .card {
            background: white;
            padding: 25px;
            margin-top: 20px;
            border-radius: 12px;
            box-shadow: 0 3px 12px #00000010;
        }

        h1, h2 { color: #243b64; }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
        }

        .field {
            padding: 12px;
            background: #f7f9fc;
            border-radius: 7px;
            overflow-wrap: anywhere;
        }

        .label {
            color: #68778b;
            font-size: 13px;
            margin-bottom: 6px;
        }

        .value { font-weight: bold; }

        .task {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            padding: 15px 0;
            border-bottom: 1px solid #e5e9f0;
        }

        select {
            padding: 9px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
        }

        button {
            background: #3157a4;
            color: white;
            padding: 11px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }

        .back {
            display: inline-block;
            margin-bottom: 12px;
            color: #3157a4;
            text-decoration: none;
        }

        .progress {
            background: #e1e7ef;
            height: 12px;
            border-radius: 10px;
            overflow: hidden;
        }

        .bar { background: #28a879; height: 12px; }
    </style>
</head>
<body>
<div class="container">
    <a class="back" href="/dashboard">&larr; Back to Dashboard</a>

    <h1>Employee Onboarding Details</h1>
    <p>Employee ID: <strong>{{ emp_id }}</strong></p>

    <div class="card">
        <h2>Employee Information</h2>
        <div class="grid">
            {% for label, value in details.items() %}
                <div class="field">
                    <div class="label">{{ label }}</div>
                    <div class="value">{{ value }}</div>
                </div>
            {% endfor %}
        </div>
    </div>

    <div class="card">
        <h2>Onboarding Progress</h2>
        <p><strong>{{ report.progress }}%</strong> complete</p>
        <div class="progress">
            <div class="bar" style="width: {{ report.progress }}%;"></div>
        </div>
        <p>Overall Status: <strong>{{ report.status }}</strong></p>
    </div>

    <div class="card">
        <h2>Onboarding Tasks</h2>
        <p>Update a task when HR confirms it is complete.</p>

        <form method="POST"
              action="{{ url_for('update_employee', emp_id=emp_id) }}">
            {% for key, label in tasks.items() %}
                <div class="task">
                    <label for="{{ key }}">{{ label }}</label>
                    <select id="{{ key }}" name="{{ key }}">
                        <option value="pending"
                            {% if not employee[key] %}selected{% endif %}>
                            Pending
                        </option>
                        <option value="completed"
                            {% if employee[key] %}selected{% endif %}>
                            Completed
                        </option>
                    </select>
                </div>
            {% endfor %}
            <br>
            <button type="submit">Save Task Updates</button>
        </form>
    </div>
</div>
</body>
</html>
"""


@app.route("/employee/<emp_id>")
def employee_details(emp_id):
    employee = employees.get(emp_id)

    if employee is None:
        return "Employee not found.", 404

    report = coordinator_agent(employee)

    details = {
        "Full Name": employee["name"],
        "Email": employee["email"],
        "Phone": employee["phone"],
        "Department": employee["department"],
        "Job Role": employee["role"],
        "Joining Date": employee["joining_date"],
        "Employment Type": employee["employment_type"],
        "Reporting Manager": employee["manager"],
        "Work Location": employee["location"]
    }

    return render_template_string(
        EMPLOYEE_PAGE,
        emp_id=emp_id,
        employee=employee,
        details=details,
        report=report,
        tasks=TASKS
    )


# Update Employee Tasks
@app.route("/update/<emp_id>", methods=["POST"])
def update_employee(emp_id):
    employee = employees.get(emp_id)

    if employee is None:
        return "Employee not found.", 404

    for key in TASKS:
        employee[key] = request.form.get(key) == "completed"

    return redirect(url_for("employee_details", emp_id=emp_id))


# Start Flask Application
if __name__ == "__main__":
    print("Starting HR Employee Onboarding System...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(host="127.0.0.1", port=5000, debug=True)
