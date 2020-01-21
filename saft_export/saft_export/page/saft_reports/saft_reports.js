frappe.pages['saft-reports'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Saft Reports',
		single_column: true
	});

	new erpnext.SAFTReport(page);


	console.log(page.main)
	$main_section = $(`<div class="reconciliation page-main-content"></div>`).appendTo(page.main);
	// const empty_state = __("Upload a bank statement, link or reconcile a bank account");

	// $main_section.append(frappe.render_template("saft_reports"));
	// make_form($main_section);
	//
	// $main_section.append(`<div class="form-group frappe-control input-max-width col-md-2" data-fieldtype="Date"
	// data-fieldname="from_date" title="" data-original-title="From Date"><input type="date" autocomplete="off" class="input-with-feedback form-control bold input-sm" data-fieldtype="Date" data-fieldname="from_date" placeholder="From Date"></div>`)
	//
	// $main_section.append(`<div class="form-group frappe-control input-max-width col-md-2" data-fieldtype="Date"
	// data-fieldname="from_date" title="" data-original-title="To Date"><input type="date" autocomplete="off" class="input-with-feedback form-control bold input-sm" data-fieldtype="Date" data-fieldname="from_date" placeholder="To Date"></div>`)


}



erpnext.SAFTReport = class SAFTReport {
	constructor(page) {
		this.page = page;
		this.make_form();
	}

	make_form() {
		this.form = new frappe.ui.FieldGroup({
			fields: [
				{
					label: __('Company'),
					fieldname: 'company',
					fieldtype: 'Link',
					options: 'Company',
					reqd: '1',
					width: '60px',
					default: frappe.defaults.get_user_default("Company")
					// change: () => this.fetch_and_render()
				},
				{
					label: __('Report Type'),
					fieldname: 'report_type',
					fieldtype: 'Select',
					reqd : '1',
					width: '50px',
					options: ['I','C','F','R','S','A','Q'],
					// change: () => this.fetch_and_render()
				},

				{
					fieldtype: 'Column Break'
				},
				{
					label: __('From Date'),
					fieldname: 'start_date',
					fieldtype: 'Date',
					reqd : '1',
					width: '60px',
					// options: 'BOM',
					// change: () => this.fetch_and_render()
				},
				{
					label: __('To Date'),
					fieldname: 'end_date',
					fieldtype: 'Date',
					reqd : '1',
					width: '60px',
					// options: 'BOM',
					// change: () => this.fetch_and_render()
				},

				{
					fieldtype: 'Section Break'
				},
				{
					label: __('Generate Report'),
					fieldname: 'dummy',
					fieldtype: 'Button',
					click: () => this.generateSaftReport()
					// options: 'BOM',
					// change: () => this.fetch_and_render()
				},
			],
			body: this.page.body
		});
		this.form.make();
	}
	generateSaftReport(){
		console.log(this.form.get_values());
		frappe.call({
			method: "saft_export.saft_export.export.generate_report",
			args: this.form.get_values(),
			callback: function(r) {
				if (r.message) {
					console.log(r.message);
					// let fileName = 'sample.xml';
					// file=fopen(fileName,0);
					// fwrite(file, r.message);
					// var blob = new Blob([r.message], { type: 'text/xml' });
					// var file = new File([r.message], fileName, {type: 'text/xml'})
    			// var url = window.URL.createObjectURL(file);
					//
    			// // window.open(file);
					// console.log(url);

					var element = document.createElement('a');
				  element.setAttribute('href', 'data:text/xm;charset=utf-8,' + encodeURIComponent(r.message[0]));
				  element.setAttribute('download', r.message[1]);
				  element.style.display = 'none';
				  document.body.appendChild(element);
				  element.click();
				  document.body.removeChild(element);
					// Write data in 'Output.txt' .
					// fs.writeFile(fileName, r.message, (err) => {
					//
					//     // In case of a error throw err.
					//     if (err) throw err;
					// })
					// file_url = URL.createObjectURL(new File([r.message], fileName, {type: 'text/xml'}));
					// console.log(file_url);
				}
			}
		});
	}

}



function generateSaftReport(){
	console.log(this.form);
  var queryString = $('#saftReport').serialize();
    alert(queryString);
}
