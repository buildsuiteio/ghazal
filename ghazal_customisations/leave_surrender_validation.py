import frappe
from frappe.model.document import Document

def validate_salary_slip(doc, method):
    # Check if employee has taken Casual Leave within the salary slip date range
    leave_exists = frappe.db.exists(
        "Attendance",
        {
            "employee": doc.employee,
            "attendance_date": ["between", [doc.start_date, doc.end_date]],
            "status": "On Leave",
            "leave_type": "Casual Leave",
            "docstatus": 1
        }
    )
    
    if not leave_exists:
        total_earning = 0
        total_working_days = doc.total_working_days or 1  # Avoid division by zero
        leave_encashment_exists = False

        # Fetch salary structure linked to the salary slip
        if doc.salary_structure:
            salary_structure = frappe.get_doc("Salary Structure", doc.salary_structure)
            
            # Sum all amounts in the earnings table of salary structure
            for earning in salary_structure.earnings:
                total_earning += earning.amount

        # Check if Leave Encashment already exists in the salary slip
        for earning in doc.earnings:
            if earning.salary_component == "Leave Encashment":
                leave_encashment_exists = True
                break

        # If Leave Encashment doesn't exist, add a new row
        if not leave_encashment_exists:
            leave_encashment_amount = total_earning / total_working_days
            doc.append("earnings", {
                "salary_component": "Leave Encashment",
                "amount": leave_encashment_amount
            })
