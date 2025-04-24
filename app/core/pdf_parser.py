# -*- coding: utf-8 -*-

"""
מודול לחילוץ טקסט מקבצי PDF.
"""

import pdfplumber
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PDFParser:
    """
    מחלקה לחילוץ טקסט מקבצי PDF.
    מפרידה בין האחריות על חילוץ טקסט מהקובץ לבין עיבוד וחילוץ המידע מהטקסט.
    """

    def __init__(self):
        """
        אתחול ה-PDF Parser.
        """
        pass

    def extract_text_from_pdf(self, pdf_path):
        """
        חילוץ טקסט מלא מקובץ PDF.

        Args:
            pdf_path (str): נתיב לקובץ ה-PDF

        Returns:
            str: הטקסט המלא מהקובץ, או None במקרה של שגיאה
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_content = ""

                # איסוף הטקסט מכל העמודים
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n\n"

                return text_content

        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            return None

    def extract_tables_from_pdf(self, pdf_path):
        """
        חילוץ טבלאות מקובץ PDF.

        Args:
            pdf_path (str): נתיב לקובץ ה-PDF

        Returns:
            list: רשימה של טבלאות מהקובץ, או רשימה ריקה במקרה של שגיאה
        """
        try:
            tables = []

            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)

            return tables

        except Exception as e:
            logger.error(f"Error extracting tables from PDF {pdf_path}: {str(e)}")
            return []