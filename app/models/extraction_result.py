# -*- coding: utf-8 -*-

"""
מודל תוצאת חילוץ - מייצג את תוצאות החילוץ מקובץ PDF.
"""

import os


class ExtractionResult:
    """
    מחלקה המייצגת תוצאת חילוץ מקובץ PDF.
    """

    def __init__(self, file_path):
        """
        אתחול תוצאת חילוץ.

        Args:
            file_path (str): נתיב הקובץ שממנו בוצע החילוץ
        """
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.data = {}  # נתונים שחולצו
        self.error = None  # שגיאה (אם היתה)

    def set_data(self, data):
        """
        הגדרת נתונים שחולצו.

        Args:
            data (dict): נתונים שחולצו מהקובץ
        """
        self.data = data

    def set_error(self, error_message):
        """
        הגדרת הודעת שגיאה.

        Args:
            error_message (str): הודעת השגיאה
        """
        self.error = error_message

    def has_error(self):
        """
        בדיקה אם יש שגיאה בתוצאת החילוץ.

        Returns:
            bool: האם יש שגיאה
        """
        return self.error is not None

    def to_dict(self):
        """
        המרת תוצאת החילוץ לדיקשנרי.

        Returns:
            dict: דיקשנרי המייצג את תוצאת החילוץ
        """
        return {
            "file_path": self.file_path,
            "file_name": self.file_name,
            "data": self.data,
            "error": self.error
        }

    @classmethod
    def from_dict(cls, result_dict):
        """
        יצירת תוצאת חילוץ מדיקשנרי.

        Args:
            result_dict (dict): דיקשנרי המייצג תוצאת חילוץ

        Returns:
            ExtractionResult: אובייקט תוצאת חילוץ חדש
        """
        result = cls(result_dict.get("file_path", ""))
        result.file_name = result_dict.get("file_name", "")
        result.data = result_dict.get("data", {})
        result.error = result_dict.get("error", None)

        return result