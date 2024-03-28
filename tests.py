from payconpy.femails.femails import *
from payconpy.fpython.fpython import *
from payconpy.fregex.fregex import *

def testa_funcao_para_fazer_ocr_offline():
    from payconpy.fpdf.focr.orc import faz_ocr_em_pdf_offline
    print(faz_ocr_em_pdf_offline('files_tests\Banco Pan.pdf'))


def testa_compressao_de_pdf():
    import fitz  # PyMuPDF

    def compress_pdf(input_path, output_path):
        """
        Comprime um arquivo PDF reamostrando suas imagens.
        
        Args:
            input_path (str): O caminho para o arquivo PDF de entrada.
            output_path (str): O caminho para salvar o arquivo PDF comprimido.
        """
        doc = fitz.open(input_path)
        
        # Iterar por cada página no documento
        for page_number in range(len(doc)):
            page = doc.load_page(page_number)  # Carregar a página atual
            
            # Obter a lista de imagens da página atual
            image_list = page.get_images(full=True)
            
            # Iterar por cada imagem na página
            for image_index, img in enumerate(image_list):
                xref = img[0]  # Referência cruzada da imagem
                
                # Extrair os dados da imagem
                base_image = doc.extract_image(xref)
                imgbytes = base_image["image"]  # Bytes da imagem
                
                # Abrir a imagem com fitz
                img = fitz.open("pdf", imgbytes)
                rect = img[0].rect  # O retângulo da imagem
                
                # Reamostrar a imagem para uma nova resolução, diminuindo sua qualidade
                # Aqui, 'dim' controla as novas dimensões. Valores menores comprimem mais.
                # Ajuste esses valores conforme necessário para equilibrar qualidade e tamanho.
                new_rect = fitz.Rect(rect.tl, rect.br / 2)  # Reduz para 50% do tamanho original
                pixmap = img[0].get_pixmap(matrix=fitz.Matrix(0.5, 0.5), clip=new_rect)
                
                # Substituir a imagem original pela reamostrada
                doc._update_image(xref, pixmap)

        # Salvar o documento comprimido
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()

    # Exemplo de uso
    compress_pdf("files_tests\Banco Pan.pdf", "caminho_para_o_documento_comprimido.pdf")

def testa_download_de_arquivo():
    import requests

    def download_file_from_github(url, save_path):
        """
        Baixa um arquivo do GitHub garantindo que o stream seja tratado corretamente,
        o que é crucial para arquivos grandes.
        
        Args:
            url (str): URL do arquivo no GitHub.
            save_path (str): Caminho local onde o arquivo será salvo.
        """
        with requests.get(url, stream=True) as response:
            # Verifica se a requisição foi bem sucedida
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                # Escreve o conteúdo do arquivo em chunks para não sobrecarregar a memória
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

    # URL para o arquivo raw do tesseract_bin_pt.zip no GitHub
    url = "https://github.com/Paycon-Automacoes/payconpy/raw/main/tesseract_bin_pt.zip"

    # Caminho local onde o arquivo zip será salvo
    save_path = "tesseract_bin_pt.zip"

    # Chamada da função de download
    download_file_from_github(url, save_path)


def testar_ocr_tesseract():
    from payconpy.fpdf.focr.orc import ocr_tesseract_v2
    print(ocr_tesseract_v2('files_tests\Banco Pan.pdf'))


if __name__ == '__main__':
    testar_ocr_tesseract()