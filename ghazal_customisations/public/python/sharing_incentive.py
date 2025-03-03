import frappe
from frappe.model.document import Document

def sharing_incentive(doc, method):
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
