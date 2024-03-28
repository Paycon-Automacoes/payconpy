import fitz
from payconpy.fpython.fpython import *

def extract_pages(original_pdf_path, new_pdf_path, num_pages):
    """
    Extracts a specified number of pages from a given PDF file and creates a new PDF file using PyMuPDF (fitz).
    
    :param original_pdf_path: A string representing the path to the original PDF file.
    :param new_pdf_path: A string representing the path to the new PDF file.
    :param num_pages: An integer representing the number of pages to extract.
    
    :return: None
    
    This function uses the fitz.open function to read the original PDF file and creates a new PDF file with the
    specified number of pages using the same library. If the number of pages to extract is greater than the total number
    of pages in the original PDF file, it extracts all the available pages.

    Example:
        >>> extract_pages_fitz('input.pdf', 'output.pdf', 10)
    """
    # Open the original PDF
    doc = fitz.open(original_pdf_path)
    total_pages = doc.page_count
    
    # Calculate the number of pages to extract
    num_pages_to_extract = min(num_pages, total_pages)
    
    # Create a new PDF document for the output
    new_doc = fitz.open()  # New, empty PDF document
    
    # Loop through the specified range and add each page to the new document
    for page_num in range(num_pages_to_extract):
        page = doc.load_page(page_num)  # Load the current page
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)  # Insert the page into the new document
    
    # Save the new document to the specified path
    new_doc.save(new_pdf_path)
    
    # Close the documents
    doc.close()
    new_doc.close()

def split_pdf(input_path, output_dir='output_split', interval=30):
    """
    Splits a PDF file into multiple files with a specified page interval using PyMuPDF (fitz).
    
    :param input_path: The path to the input PDF file.
    :param output_dir: The directory where the output PDF files will be saved. Defaults to 'output_split'.
    :param interval: The number of pages in each output PDF file. Defaults to 30.
    """
    # Cria o diretório de saída, se não existir
    cria_dir_no_dir_de_trabalho_atual(output_dir)
    limpa_diretorio(output_dir)

    # Abre o arquivo PDF de entrada
    doc = fitz.open(input_path)
    total_pages = doc.page_count

    # Divide o PDF em intervalos de tamanho 'interval'
    for start in range(0, total_pages, interval):
        end = min(start + interval, total_pages)

        # Cria um novo documento fitz para cada intervalo
        output_doc = fitz.open()  # Cria um documento vazio

        # Adiciona as páginas ao novo documento
        output_doc.insert_pdf(doc, from_page=start, to_page=end-1)  # to_page é inclusivo em fitz

        # Define o nome do arquivo de saída
        output_path = os.path.join(output_dir, f'output_{start + 1}-{end}.pdf')

        # Salva o novo documento como um arquivo PDF de saída
        output_doc.save(output_path)

        # Fecha o documento de saída
        output_doc.close()

    # Fecha o documento original
    doc.close()
    
    # Retorna a lista de arquivos no diretório de saída
    return arquivos_com_caminho_absoluto_do_arquivo(output_dir)