import frappe
from frappe.model.document import Document


def before_save_hooks(doc,event):
    validate_leave_salary_slip(doc,event)
    sharing_incentive(doc,event)

def sharing_incentive(doc, event):
    if doc.payroll_entry:
        frappe.log_error("Payroll entry created")
        payroll_entry = frappe.get_doc("Payroll Entry", doc.payroll_entry)

        if payroll_entry.custom_enable_sharing_incentive:
            incentive_component = payroll_entry.custom_incentive_salary_component
            incentive_amount = payroll_entry.custom_amount

            # Check if the component already exists in earnings
            if not any(earning.salary_component == incentive_component for earning in doc.earnings):
                doc.append("earnings", {
                    "salary_component": incentive_component,
                    "amount": incentive_amount
                })



def validate_leave_salary_slip(doc, event):
    # Check if employee has taken Casual Leave within the salary slip date range
    hr_policy = frappe.get_doc("HR Policy")
    if hr_policy.enable_leave_surrender:
        leave_exists = frappe.db.exists(
            "Attendance",
            {
                "employee": doc.employee,
                "attendance_date": ["between", [doc.start_date, doc.end_date]],
                "status": "On Leave",
                "leave_type": hr_policy.surrender_leave_type,
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
                    if earning.salary_component in ["Basic","House Rent Allowance"]:
                        total_earning += earning.amount

            # Check if Leave Encashment already exists in the salary slip
            for earning in doc.earnings:
                if earning.salary_component == hr_policy.leave_salary_component:
                    leave_encashment_exists = True
                    break

            # If Leave Encashment doesn't exist, add a new row
            if not leave_encashment_exists:
                leave_encashment_amount = total_earning / total_working_days
                doc.append("earnings", {
                    "salary_component": hr_policy.leave_salary_component,
                    "amount": leave_encashment_amount
                })

