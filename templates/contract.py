from flask import Flask, render_template, request, send_file
import PyPDF2

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
    input_pdf = 'contract_template.pdf'
    output_pdf = 'contract_completed.pdf'
    complete_pdf_form(input_pdf, output_pdf, {'companyName': company_name, 'contact': contact})

    # Trimite PDF-ul completat către client
    return send_file(output_pdf, as_attachment=True)

def complete_pdf_form(input_pdf, output_pdf, field_data):
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        writer = PyPDF2.PdfFileWriter()

        for page_number in range(reader.numPages):
            page = reader.getPage(page_number)
            
            if '/Annots' in page:
                for annotation in page['/Annots']:
                    field = annotation.getObject()
                    if '/T' in field and '/V' in field:
                        field_name = field['/T']
                        if field_name in field_data:
                            field_value = field_data[field_name]
                            page.mergePage(PyPDF2.pdf.PageObject.createFormField(field_name, field_value))
            
            writer.addPage(page)

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

if __name__ == '__main__':
    app.run(debug=True)
