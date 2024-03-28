from payconpy.fpython.fpython import *
from payconpy.fpdf.pdfutils.pdfutils import split_pdf
from tqdm import tqdm
from PIL import Image
import numpy as np
import fitz, uuid, os, gdown, pytesseract, cv2, base64

def faz_ocr_em_pdf_offline(path_pdf: str, export_from_file_txt: str = False) -> str:
    """
    Converte pdf(s) em texto com fitz (PyMuPDF)
        
    Atenção, só funciona corretamente em PDF's que o texto é selecionável!
    
    Args:
        path_pdf (str): caminho do pdf
        export_from_file_txt (bool | str): passar um caminho de arquivo txt para o texto sair

    Returns:
        str: texto do PDF
    """
    
    text = []
    
    # Abre o arquivo PDF com fitz
    doc = fitz.open(path_pdf)
    
    # Itera por cada página do documento
    for page in doc:
        # Extrai o texto da página
        text.append(page.get_text())
        
    # Converte a lista de textos em uma única string
    text = "\n".join(text)
    
    # Se um caminho para um arquivo de texto for fornecido, salva o texto extraído nesse arquivo
    if export_from_file_txt:
        with open(export_from_file_txt, 'w', encoding='utf-8') as f:
            f.write(text)
    
    # Retorna o texto extraído
    return text

def ocr_google_vision(pdf, api_key, dpi=300, file_output=uuid.uuid4(), return_text=True, limit_pages=None):
    def detect_text(files_png: list[str], api_key) -> str:
        """Recupera o texto das imagens

        Args:
            files_png (list[str]): Lista de imagens do pdf

        Raises:
            Exception: != de 200 a response

        Returns:
            str: O texto do PDF
        """
        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        requests_json = []
        result = ''
        contador = len(files_png)
        while contador != 0:  # enquanto existir imagens...
            faz_log(f'Recuperando 16 imagens de {contador} imagens | Se tiver 16 de fato, senão pega o resto')
            files_png_temp = files_png[:16]
            for filepath in files_png_temp:  # faz uma lista de requests para o post
                with open(filepath, mode='rb') as file:
                    bytes_content = file.read()
                    requests_json.append(
                        {
                            "image": {
                                "content": base64.b64encode(bytes_content).decode("utf-8")
                            },
                            "features": [{"type": "TEXT_DETECTION"}]
                        }
                    )
            else:
                for i in files_png_temp:
                    files_png.remove(i)
                    

                r = requests.post(url=url, json={"requests": requests_json})
                requests_json = []  # limpa para os proximos 10
                if r.status_code == 200:
                    # faz_log(r.text)
                    r_json = r.json()
                    for resp in r_json['responses']:
                        try:
                            result = result + str(resp['textAnnotations'][0]['description']).strip()
                        except Exception as e:
                            faz_log(repr(e))
                            raise Exception(repr(e))
                    else:
                        contador = len(files_png)
                else:
                    raise Exception(r.json()['error']['message'])

        return remover_acentos(result.lower().strip())
    
    with fitz.open(pdf) as pdf_fitz:
        cria_dir_no_dir_de_trabalho_atual('pages')
        limpa_diretorio('pages')
        faz_log(f'Convertendo PDF para páginas...')
        number_of_pages = len(pdf_fitz) if limit_pages is None else min(limit_pages, len(pdf_fitz))
        with tqdm(total=number_of_pages, desc='EXTRACT PAGES') as bar:
            for i, page in enumerate(pdf_fitz):
                if i >= number_of_pages:
                    break
                page = pdf_fitz.load_page(i)
                mat = fitz.Matrix(dpi/72, dpi/72)  # Matriz de transformação usando DPI
                pix = page.get_pixmap(matrix=mat)
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                image.save(f'pages/{i}.png')
                bar.update(1)
        
    faz_log('Enviando para Google Vision...')
    files = list(arquivos_com_caminho_absoluto_do_arquivo('pages'))
    text_ocr = detect_text(files, api_key)
    limpa_diretorio('pages')
    if return_text:
        return text_ocr
    else:
        file_path = arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt')
        with open(file_path, 'w') as f:
            text_ocr.write(f)
        return file_path
    
    
    
def ocr_tesseract_v2(pdf, dpi=300, file_output=uuid.uuid4(), return_text=True, config_tesseract='', limit_pages=None, lang='por', timeout=120):
    path_exit = arquivo_com_caminho_absoluto('temp_tess', 'Tesseract-OCR.zip')
    path_tesseract_extract = arquivo_com_caminho_absoluto('bin', 'Tesseract-OCR')
    path_tesseract = arquivo_com_caminho_absoluto(('bin', 'Tesseract-OCR'), 'tesseract.exe')

    if not os.path.exists(path_tesseract):
        faz_log('Baixando binários do Tesseract, aguarde...')
        cria_dir_no_dir_de_trabalho_atual('temp_tess')
        cria_dir_no_dir_de_trabalho_atual('bin')
        gdown.download('https://drive.google.com/uc?id=1yX6I7906rzo3YHK5eTmdDOY4FulpQKJ-', path_exit, quiet=True)
        sleep(1)
        with zipfile.ZipFile(path_exit, 'r') as zip_ref:
            # Obtém o nome da pasta interna dentro do arquivo ZIP
            zip_info = zip_ref.infolist()[0]
            folder_name = zip_info.filename.split("/")[0]

            # Extrai o conteúdo da pasta interna para a pasta de destino
            for file_info in zip_ref.infolist():
                if file_info.filename.startswith(f"{folder_name}/"):
                    file_info.filename = file_info.filename.replace(f"{folder_name}/", "", 1)
                    zip_ref.extract(file_info, path_tesseract_extract)
        deleta_diretorio('temp_tess')
    pytesseract.pytesseract.tesseract_cmd = path_tesseract

    with fitz.open(pdf) as pdf_fitz:
        cria_dir_no_dir_de_trabalho_atual('pages')
        limpa_diretorio('pages')
        faz_log(f'Convertendo PDF para páginas...')
        number_of_pages = len(pdf_fitz) if limit_pages is None else min(limit_pages, len(pdf_fitz))
        with tqdm(total=number_of_pages, desc='EXTRACT PAGES') as bar:
            for i, page in enumerate(pdf_fitz):
                if i >= number_of_pages:
                    break
                page = pdf_fitz.load_page(i)
                mat = fitz.Matrix(dpi/72, dpi/72)  # Matriz de transformação usando DPI
                pix = page.get_pixmap(matrix=mat)
                pix.save(arquivo_com_caminho_absoluto('pages', f'{i}.png'))
                bar.update(1)
        

        files = arquivos_com_caminho_absoluto_do_arquivo('pages')
        with tqdm(total=len(files), desc='OCR') as bar:
            for i, image in enumerate(files):
                try:
                    text = pytesseract.image_to_string(image, config=config_tesseract, lang=lang, timeout=timeout)
                except Exception as e:
                    return False
                with open(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'), 'a', encoding='utf-8') as f:
                    f.write(text)
                bar.update(1)
            else:
                limpa_diretorio('pages')
                if return_text:
                    text_all = ''
                    with open(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'), 'r', encoding='utf-8') as f:
                        text_all = f.read()
                    os.remove(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'))
                    return text_all
                else:
                    return os.path.abspath(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'))