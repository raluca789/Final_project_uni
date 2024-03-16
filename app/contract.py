# from flask import Flask, render_template, request, send_file
# import PyPDF2
# from PyPDF2.generic import NameObject, createStringObject


# app = Flask(__name__, template_folder='templates')

# @app.route('/')
# def index():
#     return render_template('contract_template.html')

# @app.route('/generate_contract', methods=['POST'])
# def generate_contract():
#     # Procesează datele primite de la client
#     company_name = request.form['companyName']
#     contact = request.form['contact']

#     # Completează formularul PDF
#     input_pdf = 'templates/contract_template.pdf'
#     output_pdf = 'contract_completed.pdf'
#     complete_pdf_form(input_pdf, output_pdf, {'companyName': company_name, 'contact': contact})

#     # Trimite PDF-ul completat către client
#     return send_file(output_pdf, as_attachment=True)

# def complete_pdf_form(input_pdf, output_pdf, field_data):
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         for page in reader.pages:
#             if '/Annots' in page:
#                 for annotation in page['/Annots']:
#                     field = annotation.getObject()
#                     if '/T' in field and '/V' in field:
#                         field_name = field['/T']
#                         if field_name in field_data:
#                             field_value = field_data[field_name]
#                             field.update({
#                                 NameObject('/V'): createStringObject(field_value)
#                             })
            
#             writer.add_page(page)

#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# if __name__ == '__main__':
#     app.run(debug=True)
# #A trebuit sa i doau doar 'Reload Window' din View->Command Pallette ca sa mearga

from flask import Flask, render_template, request, send_file
import PyPDF2
from PyPDF2.generic import NameObject, createStringObject

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('contract_template.html')

@app.route('/generate_contract', methods=['POST'])
def generate_contract():
    # Procesează datele primite de la client
    company_name = request.form['companyName']
    contact = request.form['contact']

    # Completează formularul PDF
    input_pdf = 'templates/contract_template.pdf'
    output_pdf = 'contract_completed.pdf'
    complete_pdf_form(input_pdf, output_pdf, {'companyName': company_name, 'contact': contact})

    # Trimite PDF-ul completat către client
    return send_file(output_pdf, as_attachment=True)

def complete_pdf_form(input_pdf, output_pdf, field_data):
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page_number, page in enumerate(reader.pages, 1):
            annotations = page.get("/Annots", [])

            for annotation in annotations:
                field = annotation.get_object()
                if '/T' in field and '/V' in field:
                    field_name = field['/T']
                    if field_name in field_data:
                        field_value = field_data[field_name]
                        print(f"Field '{field_name}': {field_value}")
                        field['/V'] = createStringObject(field_value)

            writer.add_page(page)

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

if __name__ == '__main__':
    app.run(debug=True)
