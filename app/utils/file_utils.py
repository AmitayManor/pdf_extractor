# -*- coding: utf-8 -*-

"""
פונקציות עזר לטיפול בקבצים.
"""

import os
import shutil
from pathlib import Path
from app.utils.logger import get_logger

logger = get_logger(__name__)


def ensure_directory_exists(directory_path):
    """
    וידוא קיום ספרייה, ויצירתה אם לא קיימת.

    Args:
        directory_path (str או Path): נתיב הספרייה

    Returns:
        bool: האם הספרייה קיימת (או נוצרה בהצלחה)
    """
    try:
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory_path}: {str(e)}")
        return False


def get_pdf_files_in_directory(directory_path, recursive=True):
    """
    מציאת כל קבצי ה-PDF בספרייה.

    Args:
        directory_path (str או Path): נתיב הספרייה
        recursive (bool, optional): האם לחפש גם בתתי-ספריות

    Returns:
        list: רשימת נתיבים לקבצי PDF
    """
    pdf_files = []

    try:
        path = Path(directory_path)

        if recursive:
            # חיפוש בכל הספריות והתת-ספריות
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))
        else:
            # חיפוש רק בספרייה הנוכחית
            for file in path.glob("*.pdf"):
                pdf_files.append(str(file))

        return pdf_files

    except Exception as e:
        logger.error(f"Error searching for PDF files in {directory_path}: {str(e)}")
        return []


def get_file_name(file_path):
    """
    חילוץ שם הקובץ מנתיב מלא.

    Args:
        file_path (str): נתיב מלא לקובץ

    Returns:
        str: שם הקובץ (כולל סיומת)
    """
    return os.path.basename(file_path)


def get_file_name_without_extension(file_path):
    """
    חילוץ שם הקובץ ללא סיומת.

    Args:
        file_path (str): נתיב מלא לקובץ

    Returns:
        str: שם הקובץ ללא סיומת
    """
    return os.path.splitext(os.path.basename(file_path))[0]


def ensure_file_extension(file_path, extension):
    """
    וידוא שלקובץ יש סיומת מסוימת, והוספתה אם אין.

    Args:
        file_path (str): נתיב הקובץ
        extension (str): הסיומת הרצויה (למשל: '.xlsx')

    Returns:
        str: נתיב הקובץ עם הסיומת הנכונה
    """
    if not extension.startswith('.'):
        extension = '.' + extension

    if not file_path.lower().endswith(extension.lower()):
        file_path += extension

    return file_path


def copy_file(source_path, target_path, overwrite=False):
    """
    העתקת קובץ ממקום למקום.

    Args:
        source_path (str): נתיב המקור
        target_path (str): נתיב היעד
        overwrite (bool, optional): האם לדרוס קובץ קיים

    Returns:
        bool: האם ההעתקה הצליחה
    """
    try:
        # בדיקה אם הקובץ קיים ואם מותר לדרוס
        if os.path.exists(target_path) and not overwrite:
            logger.warning(f"File {target_path} already exists and overwrite=False")
            return False

        # וידוא קיום ספריית היעד
        target_dir = os.path.dirname(target_path)
        ensure_directory_exists(target_dir)

        # העתקת הקובץ
        shutil.copy2(source_path, target_path)
        return True

    except Exception as e:
        logger.error(f"Error copying file from {source_path} to {target_path}: {str(e)}")
        return False


def delete_file(file_path):
    """
    מחיקת קובץ.

    Args:
        file_path (str): נתיב הקובץ למחיקה

    Returns:
        bool: האם המחיקה הצליחה
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
        return False