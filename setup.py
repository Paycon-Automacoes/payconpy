import os
from setuptools import setup

version = '2.1.0'

with open("README.md", "r", encoding='utf-8') as fh:
    readme = fh.read()
    setup(
        name='payconpy',
        version=version,
        url='https://github.com/githubpaycon/payconpy',
        license='MIT License',
        author='Paycon Automações',
        long_description=readme,
        long_description_content_type="text/markdown",
        author_email='fernanda.yamamoto@paycon.com.br',
        keywords='Funções Para Melhorar Desenvolvimento de Robôs com Selenium',
        description=u'Funções Para Melhorar Desenvolvimento de Robôs com Selenium',
        
        packages= [
            os.path.join('payconpy', 'femails'),
            os.path.join('payconpy', 'fexceptions'),
            os.path.join('payconpy', 'fpdf'),
            os.path.join('payconpy', 'fpdf', 'focr'),
            os.path.join('payconpy', 'fpdf', 'pdfutils'),
            os.path.join('payconpy', 'fpysimplegui'),
            os.path.join('payconpy', 'fpython'),
            os.path.join('payconpy', 'fregex'),
            os.path.join('payconpy', 'fselenium'),
            os.path.join('payconpy', 'utils'),
            os.path.join('payconpy', 'openai'),
            os.path.join('payconpy', 'openai', 'assistants'),
            os.path.join('payconpy', 'openai', 'apis'),
            os.path.join('payconpy', 'odoo'),
        ],
        
        install_requires= [
            'selenium',
            'bs4',
            'requests',
            'html5lib',
            'webdriver-manager',
            'pretty-html-table',
            'PySimpleGUI==4.60.0',
            'xlsxwriter',
            'pandas',
            'sqlalchemy',
            'rich',
            'pyinstaller==5.12.0',
            # for ocr
            'opencv-python==4.8.1.78',
            'pytesseract',
            'PyMuPDF',
        ],
        extras_require={
            'openai': [ # for chatpdf
                'openai',
            ],
    },
)
