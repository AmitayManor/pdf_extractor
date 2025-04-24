# -*- coding: utf-8 -*-

"""
מודול עיבוד נתונים - אחראי על עיבוד המידע המחולץ ממסמכי PDF.
"""

from app.models.extraction_result import ExtractionResult
from app.core.pdf_parser import PDFParser
from app.core.data_extractor import DataExtractor
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DataProcessor:
    """
    אחראי על תהליך חילוץ ועיבוד המידע מקבצי PDF.
    """

    def __init__(self):
        """
        אתחול מעבד הנתונים.
        """
        self.pdf_parser = PDFParser()
        self.data_extractor = DataExtractor()

    def process_pdf_file(self, pdf_path, extraction_config):
        """
        עיבוד קובץ PDF וחילוץ נתונים ממנו.

        Args:
            pdf_path (str): נתיב לקובץ ה-PDF
            extraction_config (ExtractionConfig): תצורת החילוץ

        Returns:
            ExtractionResult: תוצאות החילוץ
        """
        try:
            # יצירת אובייקט תוצאות
            result = ExtractionResult(pdf_path)

            # חילוץ טקסט מהקובץ
            text_content = self.pdf_parser.extract_text_from_pdf(pdf_path)

            if not text_content:
                result.set_error("לא ניתן לחלץ טקסט מהקובץ")
                return result

            # חילוץ נתונים מהטקסט
            extracted_data = self.data_extractor.extract_data_from_text(text_content, extraction_config)

            # שמירת הנתונים המחולצים בתוצאה
            result.set_data(extracted_data)

            return result

        except Exception as e:
            logger.error(f"Error processing PDF file {pdf_path}: {str(e)}")

            # יצירת תוצאה עם שגיאה
            result = ExtractionResult(pdf_path)
            result.set_error(f"שגיאה בעיבוד הקובץ: {str(e)}")

            return result

    def process_multiple_pdf_files(self, pdf_paths, extraction_config, progress_callback=None):
        """
        עיבוד מספר קבצי PDF וחילוץ נתונים מהם.

        Args:
            pdf_paths (list): רשימת נתיבים לקבצי PDF
            extraction_config (ExtractionConfig): תצורת החילוץ
            progress_callback (callable, optional): פונקציית קולבק לעדכון התקדמות

        Returns:
            list: רשימת תוצאות החילוץ
        """
        results = []
        total_files = len(pdf_paths)

        for idx, pdf_path in enumerate(pdf_paths):
            try:
                # עדכון התקדמות (אם סופק קולבק)
                if progress_callback:
                    progress_callback(pdf_path, (idx + 1) / total_files * 100)

                # עיבוד הקובץ הנוכחי
                result = self.process_pdf_file(pdf_path, extraction_config)
                results.append(result)

            except Exception as e:
                logger.error(f"Error in process_multiple_pdf_files for {pdf_path}: {str(e)}")

                # יצירת תוצאה עם שגיאה
                result = ExtractionResult(pdf_path)
                result.set_error(f"שגיאה כללית: {str(e)}")
                results.append(result)

        return results