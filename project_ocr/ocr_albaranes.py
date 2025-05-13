import logging
import re
from pdf2image import convert_from_path
import pytesseract
from datetime import datetime
from pathlib import Path

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración de ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_pdf(pdf_path):
    """Convierte un PDF a imágenes y extrae texto con OCR"""
    images = convert_from_path(str(pdf_path), dpi=300)
    full_text = ""
    for i, img in enumerate(images):
        gray = img.convert('L')  # Convertir a escala de grises
        thresholded = gray.point(lambda x: 0 if x < 128 else 255, '1')  # Binarización para mejor OCR
        page_text = pytesseract.image_to_string(thresholded, config='--psm 6')
        logging.debug(f"Texto extraído de la página {i + 1}:\n{page_text[:100]}...")
        full_text += page_text 
    return full_text

def extract_info(text):
    """Extrae el número de albarán del texto OCR."""
    current_year = datetime.now().year % 100
    # Patrón: letra + año de 2 dígitos + 5 dígitos, o 'AA' + año de 2 dígitos + 4 dígitos
    pattern = rf'\b(?:[A-Z]{str(current_year)}\d{{5}}|AA{str(current_year)}\d{{4}})\b'
    match = re.search(pattern, text)
    if match:
        albaran_number = match.group()
        logging.info(f"Número de albarán encontrado: {albaran_number}")
        return albaran_number
    else:
        logging.warning("Número de albarán no encontrado.")
        return None
    
def create_and_move_file(pdf_path, albaran_number, base_dir):
    """Crea carpetas según la serie de albaranes y mueve el PDF"""
    year = datetime.now().year
    if albaran_number.startswith("AA"):
        serie_folder = Path(base_dir) / "ALBARANES Serie AA"
        folder_name = f"{year} {albaran_number[:4]}"
    else:
        serie_folder = Path(base_dir) / f"ALBARANES Serie {albaran_number[0]}"
        folder_name = f"{year} {albaran_number[:3]}"
    albaran_folder = serie_folder / folder_name
    albaran_folder.mkdir(parents=True, exist_ok=True)
    new_path = albaran_folder / f"{albaran_number}.pdf"
    if new_path.exists():
        logging.info(f"El archivo {new_path} ya existe. No se moverá '{pdf_path.name}'.")
    else:
        pdf_path.rename(new_path)
        logging.info(f"Movido '{pdf_path.name}' a '{new_path}'")

def organize_pdfs(directory):
    """Organiza todos los PDFs en el directorio dado."""
    base_dir = Path(directory)
    if not base_dir.exists():
        logging.error(f"El directorio {base_dir} no existe.")
        return
    for pdf_path in base_dir.glob("*.pdf"):
        logging.info(f"Procesando {pdf_path.name}")
        text = extract_text_from_pdf(pdf_path)
        albaran_number = extract_info(text)
        if albaran_number:
            create_and_move_file(pdf_path, albaran_number, base_dir)
        else:
            logging.warning(f"Número de albarán no encotnrado en {pdf_path.name}")

if __name__ == "__main__":
    # Directorio de trabajo
    directory = Path(r"C:\Users\fcoja\Downloads\Carpeta Prueba")
    organize_pdfs(directory)
    logging.info("Organización de PDFs completada.")