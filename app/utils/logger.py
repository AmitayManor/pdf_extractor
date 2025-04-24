# -*- coding: utf-8 -*-

"""
מודול תיעוד - אחראי על ניהול תיעודים של האפליקציה.
"""

import os
import logging
from pathlib import Path
from datetime import datetime

# הגדרת פורמט התיעוד
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

# ספריית התיעודים
LOG_DIR = Path.home() / "PDFExtractor" / "logs"

# יצירת ספריית התיעודים אם לא קיימת
LOG_DIR.mkdir(parents=True, exist_ok=True)

# שם קובץ התיעוד הנוכחי
LOG_FILE = LOG_DIR / f"pdf_extractor_{datetime.now().strftime('%Y%m%d')}.log"

# הגדרת handler לקובץ
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# הגדרת handler לקונסול
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))


def get_logger(name):
    """
    קבלת logger לשימוש במודולים השונים.

    Args:
        name (str): שם המודול המתעד

    Returns:
        logging.Logger: אובייקט logger מוגדר
    """
    logger = logging.getLogger(name)

    # הוספת handlers רק אם אין כאלה כבר
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.setLevel(LOG_LEVEL)

    return logger