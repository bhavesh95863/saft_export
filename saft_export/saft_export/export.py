# header.clj
import frappe
import datetime

from erpnext.accounts.report.financial_statements import (get_period_list, get_columns, get_data)

global_products = []
global_tax_codes = []
company_obj = None
last_hash = None
current_company = ''


def self_address():

    return {
       "BuildingNumber": "HSNav",
       "StreetName": "rua",
       "AddressDetail": "República de AngolaCuneneXXXXX",
       "City": "Cunene",
       "PostalCode": "439611",
       "Province": "qnKsAaj3wH3zsElRtPVcbj4Zm",
       "Country": "K"
    }

def header(start_date, end_date):

    #company Pixel Infinito (SU) LDA


    start_date_year = datetime.datetime.strptime(start_date, '%Y-%m-%d').year

    json_obj = {
               "AuditFileVersion": "1.03_01",
               "CompanyID": "AGT",
               "TaxRegistrationNumber": "000000001",
               "TaxAccountingBasis": "C",
               "CompanyName": company_obj.name,
               "BusinessName": company_obj.company_name,
               "CompanyAddress": self_address(),
               "FiscalYear": start_date_year, ## TODO:  make it from start date
               "StartDate": start_date,
               "EndDate": end_date,
               "CurrencyCode": company_obj.default_currency,
               "DateCreated": datetime.date.today(),
               "TaxEntity": "Global",
               "ProductCompanyTaxID": "du00000001",
               "SoftwareValidationNumber": "001AGT20081992",
               "ProductID": "cOPETzQeWKfzkpUaI9pgi8VaW5y",
               "ProductVersion": "du00000001",
               "HeaderComment": "Ficheiro de demonstração para esclarecimento de eventuais dúvidas",
               "Telephone": company_obj.phone_no,
               "Fax": company_obj.fax,
               "Email": company_obj.email,
               "Website": company_obj.website
            }

    return json_obj
#
# account.clj	Add comments and tests for account model
# accounting_relevant_totals.clj	Add comments and tests for accounting relevant totals
def account_balance(start_date, end_date): #GeneralLedgerAccounts
    from erpnext.accounts.report.financial_statements import (get_period_list, get_columns, get_data)
    import datetime

    print('account_balance start')

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')

    starting_day_of_current_year = start_date.date().replace(month=1, day=1)
    ending_day_of_current_year = start_date.date().replace(month=12, day=31)

    opening_from_date = start_date.date() - datetime.timedelta(days=2)
    opening_to_date = start_date.date() - datetime.timedelta(days=1)

    period_list = [
    frappe._dict({'from_date': opening_from_date,
                    'to_date': opening_to_date,
                    'to_date_fiscal_year': '2019',
                    'from_date_fiscal_year_start_date': opening_from_date.replace(month=1, day=1),
                    'key': 'opening',
                    'label': 'Jan 19-Jun 19',
                    'year_start_date': starting_day_of_current_year,
                    'year_end_date': ending_day_of_current_year
                    }),

                    frappe._dict({'from_date': start_date.date(),
                    'to_date': datetime.datetime.strptime(end_date, '%Y-%m-%d').date(),
                    'to_date_fiscal_year': '2019',
                    'from_date_fiscal_year_start_date': starting_day_of_current_year,
                    'key': 'current',
                    'label': 'Jul 19-Dec 19',
                    'year_start_date': starting_day_of_current_year,
                    'year_end_date': ending_day_of_current_year
                    })
                    ]
    filters = frappe._dict({'company': company_obj.name,
            'from_fiscal_year': '2019',
            'to_fiscal_year': '2019',
            'periodicity': 'Half-Yearly',
            'cost_center': [],
            'accumulated_values': 1
            })


    asset = get_data(filters.company, "Asset", "Debit", period_list,
    only_current_fiscal_year=False, filters=filters,
    accumulated_values=filters.accumulated_values)

    liability = get_data(filters.company, "Liability", "Credit", period_list,
    only_current_fiscal_year=False, filters=filters,
    accumulated_values=filters.accumulated_values)

    print(frappe.as_json(asset))
    print(frappe.as_json(liability))

    json_obj =  {
              "AccountID": "AIDZAoMn61671353",
              "AccountDescription": "Caixa",
              "OpeningDebitBalance": '0.0', #all doubts
              "OpeningCreditBalance": '0.0',
              "ClosingDebitBalance": '0.0',
              "ClosingCreditBalance": '0.0',
              "GroupingCategory": "GR",
              "GroupingCode": []
           }

    for item in liability:

        if item and "Total Liability (Credit)" in item["account"]:
            print(item)
            json_obj["OpeningCreditBalance"] = item["opening"]
            json_obj["ClosingCreditBalance"] = item["current"]

    for item in asset:
        if item and "Total Asset (Debit)" in item["account"]:
            print(item)
            json_obj["OpeningDebitBalance"] = item["opening"]
            json_obj["ClosingDebitBalance"] = item["current"]

    print(frappe.as_json(json_obj))
    return json_obj

def address(customer_primary_address):

    if customer_primary_address:
        return {
               "BuildingNumber":customer_primary_address.address_title, #"tkawQFy",
               "StreetName":customer_primary_address.address_line1, #"yJ51azJInsA6OoIGF1Jv5EiVyx1B7j4B7e2LnZFBqtOujauGiUeflaLw6GmtNB7aH2n65tI84oK9W0VymAeJVr42jdXc4RNBdpD3",
               "AddressDetail":customer_primary_address.address_line2, #"AnhuiProvinceChinaCabindaXXXXX",
               "City":customer_primary_address.city, #"Cabinda",
               "PostalCode":customer_primary_address.pincode, #"317615",
               "Province":customer_primary_address.state, #"cUoW8bMQFQiGfRAhUbduZOceu",
               "Country":customer_primary_address.country, #"Ky3S2z"

            }
    return None

def address_small(address):
    import frappe

    if not address or address == "":
        return None
    else:
        address = frappe.get_doc("Address", address)

    return  {
       "Address": {
          "AddressDetail": address.address_line1, #"Morada do Cliente",
          "City": address.city, #"Luanda",
          "Country": address.country, #"AO"
       }
    }

# client.clj	Add docs/tests for client
def customer(customer):
    import frappe

    customer = frappe.get_doc('Customer', customer)

    return  {

               "CustomerID": customer.naming_series, ##customer.name,#"CUSzG1pk66799652",
               "AccountID": "Desconhecido", #acustomer.accounts
               "CustomerTaxID": customer.tax_id, #"CTID41987713",
               "CompanyName": customer.represents_company.name if customer.represents_company else customer.name,  #"Wobo)",
               "Contact": customer.customer_name, #"Hitachi",
               "BillingAddress": address(customer.customer_primary_address),
               "ShipToAddress": address(customer.customer_primary_address),
               "Telephone": customer.mobile_no,# "E5aTtj5MfG",
               "Fax": None,#"j2umKFDkit", # Not Available in ERPNext
               "Email": customer.email_id,# "HoY3hSCRefNYO22kuZ7dQZuSUIMIyTmk1X7ucB6Lf4Qc3iaFyM7lDEAaKjThFd7@CCNbzDiaiMI5zW8MzTS8ld5bLUyHHas2oKxJekFxtSDhd2pvfak2mOKKHyB.com",
               "Website": customer.website, #"www.bGHMfpVmCAvl1siXZdcxRf.com",
               "SelfBillingIndicator": "0" # Doubt
            }


def supplier(supplier_obj):
    import frappe

    supplier_obj = frappe.get_doc('Supplier', customer)

    json_obj =  { # same as customer
           "SupplierID": supplier_obj.name,#"ATIDdUTEP24806471",
           "AccountID": supplier_obj.default_bank_account if supplier_obj.default_bank_account else "Desconhecido",
           "SupplierTaxID": supplier_obj.tax_id, #"STID15495901",
           "CompanyName": supplier_obj.represents_company.name if supplier_obj.represents_company else supplier_obj.name,  #"China National Petroleum Corporation.",
           "Contact": supplier_obj.supplier_name, #"A general motors",
           }
        #    "BillingAddress": address(customer.supplier_address),
        #    # {
        #    #    "BuildingNumber": "cIpX9",
        #    #    "StreetName": "Qd1E10Ji2OKyNYd3gzYCRGrcwfuvrHVryaxafYl4bKtXPgwhg1252uMky8zAy1a594A9MWQt8bYmSBXGrnrZYnYplsb9P5UWiDD7",
        #    #    "AddressDetail": "AnhuiProvinceChinaCuneneXXXXX",
        #    #    "City": "Cunene",
        #    #    "PostalCode": "371253",
        #    #    "Province": "X1VpsjWjUUROXg6D83Jycp9Ny",
        #    #    "Country": "w"
        #    # },
        #    "ShipFromAddress": address(customer.shipping_address),
        #    # {
        #    #    "BuildingNumber": "Ih7ob",
        #    #    "Staddress_smallreetName": "Eq0k5c8T5sykaV7V0slZ3ilo7kAScmDffH05Tnw2bSu88kdX8ZeD2E6Bl1ziQekvjHtIYJ3D1XhUJYH9IE6wh3T5e8qmHNv6uHw0",
        #    #    "AddressDetail": "AnhuiProvinceChinaCabindaXXXXX",
        #    #    "City": "1MJU8GZLpnFAGxahw7hLBSZXS",
        #    #    "PostalCode": "075196",
        #    #    "Province": "tElVN3P5d9nggBCW6dxS2dLMH",
        #    #    "Country": "R"
        #    # },
        #    "Telephone": customer.contact_mobile,# "JVsBQ8KIjo",
        #    "Fax": "",#4rITj5w78m",
        #    "Email": customer.contact_email,#"LuSe6IS6dV0O9IlwGzNeMvAi4UcElMxUtkv0z774Fo99AUNLdrabeFctPTMesUh@3PoZHmtWkQ7jyztN3icVAaNzR1LLhMCqshZpMxNibsPVv74LzF6vnnvJx0Q.com",
        #    # "Website": customer.website,#"www.XJGcpbjQGekGctFU29S4Ot.com",
        #    "SelfBillingIndicator": "1"# Doubt
        # }

    return json_obj


# product.clj
def product(item): #Product
    import frappe

    item = frappe.get_doc('Item', item)

    json_obj =  {
       "ProductType": "P",
       "ProductCode": item.item_code, #"Art1"
       "ProductGroup": item.item_group, #"N/A",
       "ProductDescription": item.description, #"Artigo 1",
       "ProductNumberCode":item.item_code,# "Art1",
       "CustomsDetails": "vob",
       # "UNNumber": "Ky7" #Only for dangerous
    }

    return json_obj


# tax_table.clj
# <TaxTable>
# 				<TaxTableEntry>
# 					<TaxType>IVA</TaxType>
# 					<TaxCode>NOR</TaxCode>
# 					<Description>Normal</Description>
# 					<TaxPercentage>014.00</TaxPercentage>
# 				</TaxTableEntry>
# 				<TaxTableEntry>
# 					<TaxType>IVA</TaxType>
# 					<TaxCode>ISE</TaxCode>
# 					<Description>Isenta</Description>
# 					<TaxPercentage>0</TaxPercentage>
# 				</TaxTableEntry>
# 			</TaxTable>
def tax_table(): #TaxTable

    json_obj = []

    for tax_code in global_tax_codes:
        if tax_code == "NOR":
            json_obj.append({
               "TaxType": "IVA",
               "TaxCode": "NOR",
               "Description": "Normal",
               "TaxPercentage": "14.00"
            })
        elif tax_code == "ISE":
            json_obj.append({
               "TaxType": "IVA",
               "TaxCode": "ISE",
               "Description": "Isenta",
               "TaxPercentage": "0"
            })

    return json_obj

#MasterFiles End

#SourceDocuments start
def item_json(item, type='sales_invoice', tax_data=None, reference=''):
    import frappe

    # item = frappe.get_doc('Sales Invoice Item', item.name)

    # “VAT” - value added tax; “IS” - Stamp Duty.
    #
    # “NS” - ​​Not subject to VAT or IS

    #     (TaxType)
    #
    # = VAT, must be completed with:
    #
    # “NOR” - Normal Rate; “ISE” - Exempt;
    #
    # “OUT” - Other, applicable for special VAT schemes.
    #
    # In the case of field 4.1.4.19.15.1 - Tax Type Code
    #
    # (TaxType)
    #
    # = IS, must be filled in with: The corresponding budget code; “ISE” - Exempt.
    #
    # In case of non-subjection it must be filled with “NS”.
    if not item.item_code in global_products:
        global_products.append(item.item_code)

    if not tax_data["tax_code"] in global_tax_codes:
        global_tax_codes.append(tax_data["tax_code"])

    # print(tax_data)
    item_json = {
               "LineNumber": item.serial_no, #"1",
               "ProductCode": item.item_name, #"Art1",
               "ProductDescription": item.description, #"Artigo 1",
               "Quantity": item.qty, #"1.00",
               "UnitOfMeasure": item.uom, # "Unidade",
               "UnitPrice": item.rate, #"1000.0000",
               "TaxPointDate": item.creation, #"2019-04-29",
               "References": {
                  "Reference": reference,
                  "Reason": "Devolucao de Cliente"
               },
               "Description": item.description, #"Artigo 1",
               "DebitAmount": item.amount, #"1000.00",
               "Tax": {
                  "TaxType": tax_data["tax_type"], #"IVA",
                  "TaxCountryRegion": "AO",
                  "TaxCode": tax_data["tax_code"], #"NOR",
                  "TaxPercentage": str(tax_data["tax_rate"]), #"14.00"
               }
            }

    if type == 'stock_item':
        item_json['CreditAmount'] = item_json['DebitAmount']
        del item_json['References']
        del item_json['DebitAmount']

    return item_json

# document.clj
def invoice(invoice_obj, type="sales"):
    import frappe


    if type == "sales":
        invoice_obj = frappe.get_doc('Sales Invoice', invoice_obj)
    elif type == "purchase":
        invoice_obj = frappe.get_doc('Purchase Invoice', invoice_obj)

    items_array = []
    print(invoice_obj.name)
    tax_data2 = ({
                    "tax_type" : "VAT" if "VAT" in invoice_obj.taxes[0].account_head else "IS",
                    "tax_code" : "NOR" if "VAT" in invoice_obj.taxes[0].account_head else "ISE",
                    "tax_rate" : invoice_obj.taxes[0].rate,
                } if invoice_obj.taxes and invoice_obj.taxes[0] else {"tax_type" : "NS", "tax_code" : "NA", "tax_rate": float(0.0) })
    for item in invoice_obj.items:
        items_array.append(item_json(item, type='sales_invoice', tax_data=tax_data2, reference=invoice_obj.name))




    ship_to = invoice_obj.shipping_address_name if type == "sales" else invoice_obj.shipping_address
    ship_from = invoice_obj.shipping_address_name if type == "sales" else invoice_obj.shipping_address

# <select type="text" autocomplete="off" class="input-with-feedback form-control input-sm" maxlength="140" data-fieldtype="Select" data-fieldname="status" placeholder="Status">
#    <option></option>
#    <option value="Draft">Draft</option>
#    <option value="Return">Return</option>
#    <option value="Credit Note Issued">Credit Note Issued</option>
#    <option value="Submitted">Submitted</option>
#    <option value="Paid">Paid</option>
#    <option value="Unpaid">Unpaid</option>
#    <option value="Unpaid and Discounted">Unpaid and Discounted</option>
#    <option value="Overdue and Discounted">Overdue and Discounted</option>
#    <option value="Overdue">Overdue</option>
#    <option value="Cancelled">Canceled</option>
# </select>

    invoice_status = "N"
    if invoice_obj.status in ["Cancelled"]:
        invoice_status = "A"

    invoice_type = "FT"

    if last_hash:
        hash_key = ";".join([str(invoice_obj.posting_date),
                        str(invoice_obj.creation),
                        str(invoice_obj.name),
                        str(invoice_obj.grand_total),
                        last_hash])
    else:
        hash_key = ";".join([str(invoice_obj.posting_date),
                        str(invoice_obj.creation),
                        str(invoice_obj.name),
                        str(invoice_obj.grand_total)])

    json_obj = {
      "InvoiceNo": invoice_obj.name, #"200 20191/1",
      "DocumentStatus": {
         "InvoiceStatus": invoice_status,
         "InvoiceStatusDate": invoice_obj.modified,
         "SourceID": "Operador Demostração", #doubt
         "SourceBilling": "P"
      },
      "Hash": generate_rsa_hash(hash_key),
      "HashControl": "1",
      "Period": "4",
      "InvoiceDate": invoice_obj.posting_date, #"2019-04-29",
      "InvoiceType": invoice_type, #"NC",
      "SpecialRegimes": {
         "SelfBillingIndicator": "0",
         "CashVATSchemeIndicator": "0",
         "ThirdPartiesBillingIndicator": "0"
      },
      "SourceID": "Operador Demostração", # doubt
      "EACCode": "47411", #doubt
      "SystemEntryDate": invoice_obj.creation, #"2019-04-29T08:41:37",
      "CustomerID": invoice_obj.customer, #"1",
      "ShipTo": address_small(ship_to),
      #     {
      #    "Address": {
      #       "AddressDetail": "Morada do Armazém",
      #       "City": "Luanda",
      #       "Country": "AO"
      #    }
      # },
      "ShipFrom": address_small(ship_from), #, # TODO: login company address for sales invoice
      #     {
      #    "Address": {
      #       "AddressDetail": "Morada do Cliente",
      #       "City": "Luanda",
      #       "Country": "AO"
      #    }
      # },
    # item.clj
    #invoice item

      "Line": items_array,
      "DocumentTotals": {
         "TaxPayable": invoice_obj.total_taxes_and_charges, #"140.00",
         "NetTotal": invoice_obj.net_total, #"1000.00",
         "GrossTotal": invoice_obj.grand_total #"1140.00"
      }
    }

    return json_obj

def invoices_totals(sales_invoices, purchase_invoices):

    total_debit = float(0.00)
    total_credit = float(0.00)
    all_invoices_array = []

    for invoice_obj in sales_invoices:
        total_credit += invoice_obj["grand_total"]
        all_invoices_array.append(invoice(invoice_obj))

    for invoice_obj in purchase_invoices:
        total_debit += invoice_obj["grand_total"]
        all_invoices_array.append(invoice(invoice_obj, type="purchase"))

    return {
           "NumberOfEntries": str(len(sales_invoices)+len(purchase_invoices)),
           "TotalDebit": str(total_debit),
           "TotalCredit": str(total_credit),
           "Invoice": all_invoices_array
        }




# guide.clj




def stock_item(delivery_note):
    import frappe

    delivery_note = frappe.get_doc('Delivery Note', delivery_note)

    if last_hash:
        hash_key = ";".join([str(delivery_note.posting_date),
                        str(delivery_note.creation),
                        str(delivery_note.name),
                        str(delivery_note.grand_total),
                        last_hash])
    else:
        hash_key = ";".join([str(delivery_note.posting_date),
                        str(delivery_note.creation),
                        str(delivery_note.name),
                        str(delivery_note.grand_total),])

    items_array = []

    tax_data = ({
                    "tax_type" : "VAT" if "VAT" in delivery_note.taxes[0].account_head else "IS",
                    "tax_code" : "NOR" if "VAT" in delivery_note.taxes[0].account_head else "ISE",
                    "tax_rate" : delivery_note.taxes[0].rate,
                } if delivery_note.taxes and delivery_note.taxes[0] else {"tax_type" : "NS", "tax_code" : "NA", "tax_rate": float(0.0) })

    for item in delivery_note.items:
        items_array.append(item_json(item, type='stock_item',tax_data=tax_data, reference=delivery_note.name))

    movement_status = "N"
    if delivery_note.status in ["Cancelled"]:
        movement_status = "F"

    json_obj = { #delivery note for sales invoice
       "DocumentNumber": delivery_note.name, #"1500 20191/1",
       "DocumentStatus": {
          "MovementStatus":movement_status,
          "MovementStatusDate": delivery_note.posting_date, #"2019-04-29T12:48:15",
          "SourceID": "Supervisor",
          "SourceBilling": "P"
       },
       "Hash": generate_rsa_hash(hash_key),
       "HashControl": "1",
       "Period": "3",
       "MovementDate": delivery_note.posting_date, #"2019-03-30",
       "MovementType": "GT",
       "SystemEntryDate": delivery_note.creation, #"2019-04-29T11:52:00",
       "CustomerID": delivery_note.customer, #"1",
       "SourceID": "Supervisor",
       "ShipTo": address_small(delivery_note.shipping_address_name), # or delivery_note.customer_address
       "ShipFrom": address_small(delivery_note.shipping_address_name), #, # TODO: login company address for delivery_note
       "MovementStartTime":delivery_note.posting_date + delivery_note.posting_time,# "2019-04-29T11:51:00",
       # guide_item.clj
       "Line": items_array,
       #     {
       #    "LineNumber": "1",
       #    "ProductCode": "Art1",
       #    "ProductDescription": "Artigo 1",
       #    "Quantity": "1.00",
       #    "UnitOfMeasure": "Unidade",
       #    "UnitPrice": "1000.0000",
       #    "Description": "Artigo 1",
       #    "CreditAmount": "1000.0000",
       #    "Tax": {
       #       "TaxType": "IVA",
       #       "TaxCountryRegion": "AO",
       #       "TaxCode": "NOR",
       #       "TaxPercentage": "014.00"
       #    }
       # },

       "DocumentTotals": {
          "TaxPayable": delivery_note.total_taxes_and_charges, #"140.00",
          "NetTotal": delivery_note.net_total, #"1000.00",
          "GrossTotal": delivery_note.grand_total #"1140.00"
       }
    }
    return json_obj

# guide_totals.clj
def stock_items(delivery_notes):
    # MovementOfGoods
    total_qty = float(0.00)
    stock_items_array = []

    for delivery_note_obj in delivery_notes:
        total_qty += delivery_note_obj["total_qty"]
        stock_items_array.append(stock_item(delivery_note_obj))

    return {
       "NumberOfMovementLines": str(len(delivery_notes)),
       "TotalQuantityIssued": total_qty,
       "StockMovement": stock_items_array
    }


# payment.clj
def payment(payment):
#doc type - payment entry

    json_obj  =  {
                   "PaymentRefNo": payment.name, #"3000 20191/1",
                   "Period": "4",
                   "TransactionDate":  payment.posting_date, #"2019-04-29",
                   "PaymentType": "RC", #TODO
                   "DocumentStatus": {
                      "PaymentStatus": "N",
                      "PaymentStatusDate": "2019-04-29T08:50:52",
                      "SourceID": "Operador Demostração",
                      "SourcePayment": "P"
                   },
                   # payment_method.clj
                   "PaymentMethod": {
                      "PaymentMechanism": "NU",
                      "PaymentAmount": payment.paid_amount,#"1140.00",
                      "PaymentDate": payment.reference_date, #"2019-04-29" #doubt
                   },
                   "SourceID": "Operador Demostração",
                   "SystemEntryDate": payment.creation, #"2019-04-29T08:50:52",
                   "CustomerID": "1",
                   # payment_item.clj
                   "Line": {
                      "LineNumber": "1",
                      "SourceDocumentID": {
                         "OriginatingON": "1200 20191/1", #where to get
                         "InvoiceDate": "2019-04-29"
                      },
                      "DebitAmount": payment.paid_amount,#"1140.00"
                   },
                   "DocumentTotals": {
                      "TaxPayable": "0.00",
                      "NetTotal": payment.paid_amount,#"1140.00",
                      "GrossTotal":payment.paid_amount,# "1140.00"
                   },
                   "WithholdingTax": {
                       "WithholdingTaxType": "II",
                       "WithholdingTaxDescription": "Da6xPJghr8uLAtQW2VChBRlSX1hgCW",
                       "WithholdingTaxAmount": "16724"
                    }

                }

    return json_obj

# payment_totals.clj
def payment_totals(payments):

    total_debit = float(0.00)
    payment_array = []

    for payment_obj in payments:
        total_debit += payment_obj["paid_amount"]

    return {
       "NumberOfEntries": str(len(payments)),
       "TotalDebit": str(total_debit),
       "TotalCredit": "0.00",
       "Payment": payment_array
    }
@frappe.whitelist()
def generate_report(company, start_date, end_date, report_type):
    import frappe
    import os
    global company_obj

    print(company, start_date, end_date, report_type)

    last_hash = None
    company_obj = frappe.get_doc('Company', company)

    #
    # Draft
    # Return
    # Debit Note Issued
    # Submitted
    # Paid
    # Unpaid
    # Overdue
    # Cancelled

    # //add company filter
    # //history

    sales_invoices = frappe.get_all('Sales Invoice',
                                    filters={ 'posting_date' :[">", start_date ],
                                                'posting_date' :["<", end_date ],
                                                'company': company },
                                    fields=['name', 'customer', 'grand_total'])

    purchase_invoices = frappe.get_all('Purchase Invoice',
                                       filters={'posting_date' :[">", start_date ],
                                                'posting_date' :["<", end_date ],
                                                'company': company },
                                       fields=['name', 'supplier', 'grand_total'])


    payments = frappe.get_all('Payment Entry',
                              filters={ 'posting_date' :[">", start_date ],
                                        'posting_date' :["<", end_date ],
                                        'company': company } ,
                              fields=['name', 'paid_amount'])

    delivery_notes = frappe.get_all('Delivery Note',
                                    filters={ 'posting_date' :[">", start_date ],
                                              'posting_date' :["<", end_date ],
                                              'company': company },
                                    fields=['name', 'customer', 'total_qty'])


    final_report_json = {
        "Header" : header(start_date, end_date)
    }


    final_report_json["MasterFiles"] =  {}

    if report_type in ['I','C']:
        final_report_json["MasterFiles"]["GeneralLedgerAccounts"] = {}
        final_report_json["MasterFiles"]["GeneralLedgerAccounts"]["Account"] = account_balance(start_date, end_date)

    if report_type in ['I','C','F','P','R','S','Q']:
        final_report_json["MasterFiles"]["Customer"] = []
        customer_array = []
        for object in sales_invoices:
            if not object["customer"] in customer_array:
                final_report_json["MasterFiles"]["Customer"].append(customer(object["customer"]))

    if report_type in ['I','C','A','Q']:
        final_report_json["MasterFiles"]["Supplier"] = []
        seller_array = []
        for object in purchase_invoices: #might need to use purchase order
            if not object["supplier"] in seller_array:
                final_report_json["MasterFiles"]["Supplier"].append(supplier(object["supplier"]))


    for object in delivery_notes: #might need to use purchase order
        if not object["customer"] in seller_array:
            final_report_json["MasterFiles"]["Supplier"].append(customer(object["customer"]))


    products_array = []
    ## TODO: traverse all SO, PO and Delvery notes for items/products



    # final_report_json["GeneralLedgerEntries"] = {
    #                                                 #doubts
    #                                             }
    final_report_json["SourceDocuments"] = {}

    if report_type in ['I','C','Q'] and (len(sales_invoices) > 0 or len(purchase_invoices) > 0):
        final_report_json["SourceDocuments"]["SalesInvoices"] = invoices_totals(sales_invoices, purchase_invoices)
    elif report_type in ['F','R','S'] and len(sales_invoices) > 0:
        final_report_json["SourceDocuments"]["SalesInvoices"] = invoices_totals(sales_invoices, [])
    elif report_type == 'A' and len(purchase_invoices) > 0:
        final_report_json["SourceDocuments"]["SalesInvoices"] = invoices_totals([], purchase_invoices)

    if report_type in ['I','F','Q'] and len(delivery_notes) > 0:
        final_report_json["SourceDocuments"]["MovementOfGoods"] = stock_items(delivery_notes)

    if len(payments) > 0 and report_type in ['I','F','Q']:
        final_report_json["SourceDocuments"]["Payments"] = payment_totals(payments)

    # final_report_json["SourceDocuments"]["WorkingDocuments"] = [] # doubts


    if report_type in ['I','F','S','Q']:
        final_report_json["MasterFiles"]["Product"] = []
        for product_code in global_products:
            print(product_code)
            final_report_json["MasterFiles"]["Product"].append(product(product_code))

    final_report_json["MasterFiles"]["TaxTable"] = tax_table()

    file_name = report_type + "_" + start_date + "_" + end_date + "_report.xml"

    # print(final_report_json)

    # return final_report_json
    print('final xml file return')
    return json_to_xml(final_report_json), file_name


# common.clj
# core.clj
# countries.clj

def generate_rsa_hash(string):
    import os
    import subprocess
    # command = "openssl dgst -sha1 -sign /home/jay/private.pem <<< \"" + string +"\" | openssl enc -base64"
    print("Hash Key {}".format(string))
    command = "echo \"" + string +"\" | openssl dgst -sha1 -sign /home/frappe/private.pem  | openssl enc -base64"
    # print(command)
    # last_hash = os.system(command)
    last_hash = subprocess.check_output(command, shell=True).rstrip().decode("utf-8")
    print("hash: {}".format(last_hash))
    return last_hash


##env/bin/pip install json2xml
def json_to_xml(json_obj):
    # from json2xml import json2xml, readfromurl, readfromstring, readfromjson
    from .jsontoxml import jsontoxml
    return jsontoxml(json_obj, "AuditFile")

# from xml.etree.ElementTree import Element, SubElement, tostring
#
# def SubElementWithText(parent, tag, text):
#     attrib = {}
#     element = parent.makeelement(tag, attrib)
#     parent.append(element)
#     element.text = text
#     return element
#
# class XMLJSON(object):
#     def print_json_to_xml(self, json_obj, root=None):
#         from xml.etree.ElementTree import Element, SubElement, tostring
#         if not root:
#             root = Element('AUdit')
#         for key, value in json_obj.items():
#             child = SubElement(root, key)
#             if isinstance(value, dict):
#                 #print('x')
#                 self.print_json_to_xml(value, root=child)
#
#             else:
#                 child.text = value
#
#
#         print(tostring(root))
#         return root
