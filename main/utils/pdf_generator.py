
from io import BytesIO
from xhtml2pdf import pisa
import PyPDF2


class PDFGenerator():
    '''this class is dedicated to generate a pdf file using 
    the django template engine and xhtml2pdf library'''

    def __init__(self, template, context):
        '''parameters
            template(django.template.loader.get_template)   : the html template to where we are going to render the data 
            context(json, dict)                             : structured data that we are going to render on the template
        '''
        self.template = template
        self.context = context

    def generate(self, pdf_destination  = '', password = None):
        '''a function that will generate the pdf file 
        parameter:
            pdf_destination(str)     : location of the pdf after generation 
            password(str)            : password of the pdf file in case you want to protect it with a password
        return 
            pdf(BytesIO)             : the resulting PDF
        '''
        pdf = BytesIO()
        html = self.template.render(self.context)

        if pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=pdf).err:
            raise RuntimeError('Error generating pdf')

        pdf.seek(0)
        if not password == None:
            
            if pdf_destination == '':
                raise ValueError('Please provide a pdf destination')
            
            enc_pdf = self.encrypt_pdf(password, pdf_destination, pdf)
            return enc_pdf

        return pdf

    def encrypt_pdf(self, password, pdf_destination, pdf):
        '''
        function that will encrypt a pdf file
        parameter:
            pdf_destination(str)     : location of the pdf after generation 
            password(str)            : password of the pdf file in case you want to protect it with a password
            pdf(BytesIO)             : the pdf that will be encrypted
        return 
            encypted_pdf(BytesIO)    : the resulting encrypted PDF
        '''
        try:
            inputpdf = PyPDF2.PdfFileReader(pdf)
            pages_no = inputpdf.numPages
            output = PyPDF2.PdfFileWriter()

            for i in range(pages_no):
                output.addPage(inputpdf.getPage(i))
                output.encrypt(password)

                with open(pdf_destination, "w+b") as outputStream:
                    output.write(outputStream)

            encypted_pdf = open(pdf_destination, "r+b")
            encypted_pdf.seek(0)
        except RuntimeError as e:
            raise RuntimeError(f'Error encrypting the pdf {e}')

        return encypted_pdf
        
pdf_generator = PDFGenerator
