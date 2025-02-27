CUSTOM_FIELD = {
    "HR Policy":[
        {
            "dt":"HR Policy",
            "default": "0",
            "fieldname": "enable_leave_surrender",
            "fieldtype": "Check",
            "label": "Enable Leave Surrender",
            "insert_after": "employee_salary_component_percentage",
        },
        {
            "dt":"HR Policy",
            "depends_on": "eval:doc.enable_leave_surrender;",
            "fieldname": "leave_salary_component",
            "fieldtype": "Link",
            "label": "Leave Salary Component",
            "mandatory_depends_on": "eval:doc.enable_leave_surrender;",
            "options": "Salary Component",
            "insert_after": "enable_leave_surrender",
        },
        {
            "dt":"HR Policy",
            "depends_on": "eval:doc.enable_leave_surrender;",
            "fieldname": "surrender_leave_type",
            "fieldtype": "Link",
            "label": "Surrender Leave Type",
            "mandatory_depends_on": "eval:doc.enable_leave_surrender;",
            "options": "Leave Type",
            "insert_after": "enable_leave_surrender",
        }
        
    ]
}