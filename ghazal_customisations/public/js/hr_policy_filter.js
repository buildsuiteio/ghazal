frappe.ui.form.on("HR Policy", "onload", function(frm) {
    frm.set_query("leave_salary_component", function() {
        return {
            "filters": {
                "type": "Earning"
            }
        };
    });
});
frappe.ui.form.on("HR Policy", "onload", function(frm) {
    frm.set_query("custom_incentive_salary_component", function() {
        return {
            "filters": {
                "type": "Earning"
            }
        };
    });
});