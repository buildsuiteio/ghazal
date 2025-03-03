frappe.ui.form.on('Payroll Entry', {
    onload: function(frm) {
        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'HR Policy',
            },
            callback: function(response) {
                if (response.message) {
                    let policy = response.message;
                    console.log(policy)
                    if (policy.custom_enable_incentive) {
                        if (policy.custom_enable_incentive) {
                            frm.set_value("custom_enable_sharing_incentive",1)
                            
                            frm.set_value('custom_incentive_salary_component', policy.custom_incentive_component);
                        }
                    } else {
                        // frm.toggle_display('custom_sharing__incentive', false);
                        frm.get_field('custom_sharing__incentive').tab.$wrapper.removeClass('hide-control'); // Show tab
                        // frm.get_field('custom_sharing__incentive').$wrapper.addClass('hide-control');
                    }
                }
            }
        });
    }
});