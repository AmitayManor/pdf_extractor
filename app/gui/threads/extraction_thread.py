# -*- coding: utf-8 -*-

"""
תהליכון לחילוץ מידע מקבצי PDF.
"""

import os
from PyQt5.QtCore import QThread, pyqtSignal

from app.core.data_processor import DataProcessor
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ExtractionThread(QThread):
    """
    תהליכון לביצוע חילוץ המידע מקבצי PDF ברקע.
    """

    # אותות להודעות והתקדמות
    progress = pyqtSignal(int)
    file_progress = pyqtSignal(str, float)
    extraction_complete = pyqtSignal(list)

    def __init__(self, pdf_files, extraction_config):
        """
        אתחול תהליכון החילוץ.

        Args:
            pdf_files (list): רשימת נתיבים לקבצי PDF
            extraction_config (ExtractionConfig): הגדרות החילוץ
        """
        super().__init__()
        self.pdf_files = pdf_files
        self.extraction_config = extraction_config
        self.data_processor = DataProcessor()

    def run(self):
        """
        מתודת הריצה העיקרית של התהליכון.
        מבצעת את חילוץ המידע ומעדכנת את ההתקדמות.
        """
        try:
            # עיבוד הקבצים באמצעות מעבד הנתונים
            results = self.data_processor.process_multiple_pdf_files(
                self.pdf_files,
                self.extraction_config,
                self._progress_callback
            )

            # סיום החילוץ - שליחת הנתונים חזרה לממשק המשתמש
            self.extraction_complete.emit(results)

        except Exception as e:
            logger.error(f"Error in extraction thread: {str(e)}")
            # במקרה של שגיאה - שליחת רשימה ריקה
            self.extraction_complete.emit([])

    def _progress_callback(self, file_path, percent):
        """
        פונקציית קולבק להתקדמות עיבוד הקבצים.

        Args:
            file_path (str): נתיב הקובץ המעובד כעת
            percent (float): אחוז ההתקדמות
        """
        self.file_progress.emit(file_path, percent)
        self.progress.emit(int(percent))