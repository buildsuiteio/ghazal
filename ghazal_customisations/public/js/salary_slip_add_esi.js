frappe.ui.form.on("Salary Slip", {
    refresh: function (frm) {
        if (frm.doc.docstatus === 0) { // Only show in Draft
            frm.add_custom_button(__('Add ESI'), function () {
                add_esi_deduction(frm);
            });
        }
    }
});

function add_esi_deduction(frm) {
    let esi_component_name = "ESI Employee"; // Component name to check
    let esi_percentage = 3; // ESI deduction percentage
    let net_pay = frm.doc.net_pay || 0;

    // Check if ESI Employee component is already added
    let exists = frm.doc.deductions.some(row => row.salary_component === esi_component_name);

    if (exists) {
        frappe.msgprint({
            title: __("Error"),
            message: __("ESI already applied"),
            indicator: "red"
        });
    } else {
        // Calculate ESI amount (3% of net pay)
        let esi_amount = (net_pay * esi_percentage) / 100;

        // Add new row to deductions table
        let new_row = frm.add_child("deductions");
        new_row.salary_component = esi_component_name;
        new_row.amount = esi_amount;

        frm.refresh_field("deductions"); // Refresh child table

        // Manually update total_deduction
        update_total_deduction(frm);
    }
}

function update_total_deduction(frm) {
    let total_deduction = 0;

    // Sum up all deduction amounts
    (frm.doc.deductions || []).forEach(row => {
        total_deduction += row.amount || 0;
    });

    // Update total_deduction field
    frm.set_value("total_deduction", total_deduction);
    frm.refresh_field("total_deduction"); // Ensure UI updates
}
