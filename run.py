#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
נקודת הכניסה לאפליקציית חילוץ נתונים מנסחי טאבו.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from app.main import PDFExtractorApplication


def main():
    """נקודת הכניסה הראשית לאפליקציה."""
    app = QApplication(sys.argv)

    # הגדרת כיוון טקסט מימין לשמאל
    app.setLayoutDirection(Qt.RightToLeft)

    # הגדרת פונט ברירת מחדל לתמיכה בעברית
    font = QFont("Arial", 10)
    app.setFont(font)

    # יצירה והפעלה של האפליקציה
    window = PDFExtractorApplication()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()