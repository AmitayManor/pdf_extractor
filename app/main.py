# -*- coding: utf-8 -*-

"""
מודול ראשי של האפליקציה, אחראי על איחוד כל הרכיבים והתנעת האפליקציה.
"""

from app.gui.main_window import MainWindow
from app.config.application_config import ApplicationConfig


class PDFExtractorApplication:
    """
    מחלקה מרכזית המקשרת בין כל חלקי האפליקציה.
    """

    def __init__(self):
        """
        אתחול האפליקציה.
        """
        # טעינת הגדרות האפליקציה
        self.config = ApplicationConfig()

        # יצירת החלון הראשי
        self.main_window = MainWindow(self.config)

    def show(self):
        """
        הצגת החלון הראשי של האפליקציה.
        """
        self.main_window.show()