import logging
import re
import os
from pdf2image import convert_from_path
import pytesseract
from datetime import datetime
from pathlib import Path
from django.conf import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(str(pdf_path), dpi=300)
    full_text = ''
    for img in images:
        gray = img.convert('L')
        thresh = gray.point(lambda x: 0 if x < 128 else 255, '1')
        full_text += pytesseract.image_to_string(thresh, config='--psm 6')
    return full_text

def extract_info(text):
    current_year = datetime.now().year % 100
    pattern = rf"\b(?:[A-Z]{{{current_year}}}\d{{5}}|AA{current_year}\d{{4}})\b"
    match = re.search(pattern, text)
    return match.group() if match else None

extract_number = extract_info

def create_and_move_file(pdf_path, albaran_number, base_dir):
    year = datetime.now().year
    if not albaran_number:
        return
    if albaran_number.startswith('AA'):
        serie_folder = Path(base_dir) / 'ALBARANES Serie AA'
        folder_name = f"{year} {albaran_number[:4]}"
    else:
        serie_folder = Path(base_dir) / f"ALBARANES Serie {albaran_number[0]}"
        folder_name = f"{year} {albaran_number[:3]}"
    target = serie_folder / folder_name
    target.mkdir(parents=True, exist_ok=True)
    new_path = target / f"{albaran_number}.pdf"
    if not new_path.exists():
        Path(pdf_path).rename(new_path)
