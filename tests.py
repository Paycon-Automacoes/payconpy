from payconpy.femails.femails import *
from payconpy.fpython.fpython import *
from payconpy.fregex.fregex import *

def testa_funcao_para_fazer_ocr_offline():
    from payconpy.fpdf.focr.orc import faz_ocr_em_pdf_offline
    print(faz_ocr_em_pdf_offline('files_tests\Banco Pan.pdf'))


if __name__ == '__main__':
    testa_funcao_para_fazer_ocr_offline()