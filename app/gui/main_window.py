# -*- coding: utf-8 -*-

"""
חלון ראשי של האפליקציה.
"""

import os
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QPushButton, QLabel, QFileDialog,
                             QSplitter, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt

from app.config.constants import APP_NAME, DEFAULT_WINDOW_SIZE
from app.gui.widgets.field_selection import FieldSelectionWidget
from app.gui.widgets.template_settings import TemplateSettingsWidget
from app.gui.widgets.results_widget import ResultsWidget
from app.gui.threads.extraction_thread import ExtractionThread
from app.models.extraction_config import ExtractionConfig


class MainWindow(QMainWindow):
    """
    חלון ראשי של האפליקציה.
    """

    def __init__(self, config):
        """
        אתחול החלון הראשי.

        Args:
            config (ApplicationConfig): הגדרות האפליקציה
        """
        super().__init__()

        self.config = config
        self.selected_pdf_files = []

        # אתחול רכיבי הממשק
        self.init_ui()

    def init_ui(self):
        """
        אתחול ממשק המשתמש.
        """
        # הגדרות כלליות של החלון
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, *DEFAULT_WINDOW_SIZE)

        # יצירת ווידג'ט מרכזי
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # לייאאוט ראשי
        self.main_layout = QVBoxLayout(self.central_widget)

        # יצירת לייאאוט עליון עם כפתורים לבחירת קבצים
        self._create_top_layout()

        # יצירת ספליטר מרכזי
        self._create_central_splitter()

        # יצירת רכיבי הגדרות
        self._create_settings_widgets()

        # יצירת רכיב התוצאות
        self._create_results_widget()

        # הוספת הרכיבים לספליטר
        self.splitter.addWidget(self.settings_widget)
        self.splitter.addWidget(self.results_widget)

        # התאמת גדלים התחלתיים
        self.splitter.setSizes([400, 400])

        # הוספת הספליטר ללייאאוט הראשי
        self.main_layout.addWidget(self.splitter)

        # יצירת לייאאוט תחתון עם כפתור חילוץ ופס התקדמות
        self._create_bottom_layout()

    def _create_top_layout(self):
        """
        יצירת לייאאוט עליון עם כפתורים לבחירת קבצים.
        """
        self.top_layout = QHBoxLayout()

        # כפתורים לבחירת קבצים
        self.select_files_btn = QPushButton("בחר קבצים")
        self.select_files_btn.clicked.connect(self.select_files)

        self.select_folder_btn = QPushButton("בחר תיקייה")
        self.select_folder_btn.clicked.connect(self.select_folder)

        # תווית מצב קבצים
        self.files_label = QLabel("לא נבחרו קבצים")

        # הוספת הרכיבים ללייאאוט
        self.top_layout.addWidget(self.select_files_btn)
        self.top_layout.addWidget(self.select_folder_btn)
        self.top_layout.addWidget(self.files_label)

        # הוספת הלייאאוט ללייאאוט הראשי
        self.main_layout.addLayout(self.top_layout)

    def _create_central_splitter(self):
        """
        יצירת ספליטר מרכזי לחלוקת המסך.
        """
        self.splitter = QSplitter(Qt.Vertical)

    def _create_settings_widgets(self):
        """
        יצירת רכיבי הגדרות האפליקציה.
        """
        # רכיב ההגדרות המכיל את וידג'ט בחירת השדות והגדרות התבנית
        self.settings_widget = QWidget()
        self.settings_layout = QHBoxLayout(self.settings_widget)

        # וידג'ט בחירת שדות
        self.field_selection = FieldSelectionWidget(self.config)

        # וידג'ט הגדרות תבנית
        self.template_settings = TemplateSettingsWidget(self.config, self.field_selection)

        # הוספת הוידג'טים ללייאאוט ההגדרות
        self.settings_layout.addWidget(self.field_selection, 2)
        self.settings_layout.addWidget(self.template_settings, 1)

    def _create_results_widget(self):
        """
        יצירת רכיב תוצאות.
        """
        self.results_widget = ResultsWidget()

    def _create_bottom_layout(self):
        """
        יצירת לייאאוט תחתון עם כפתור חילוץ ופס התקדמות.
        """
        self.bottom_layout = QHBoxLayout()

        # כפתור חילוץ נתונים
        self.extract_btn = QPushButton("חלץ נתונים")
        self.extract_btn.clicked.connect(self.extract_data)
        self.extract_btn.setEnabled(False)  # לא פעיל עד שייבחרו קבצים

        # פס התקדמות
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setValue(0)

        # תווית סטטוס
        self.status_label = QLabel("מוכן")

        # הוספת הרכיבים ללייאאוט
        self.bottom_layout.addWidget(self.extract_btn)
        self.bottom_layout.addWidget(self.progress_bar)
        self.bottom_layout.addWidget(self.status_label)

        # הוספת הלייאאוט ללייאאוט הראשי
        self.main_layout.addLayout(self.bottom_layout)

    def select_files(self):
        """
        בחירת קבצי PDF בודדים.
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("PDF Files (*.pdf)")

        if file_dialog.exec_():
            self.selected_pdf_files = file_dialog.selectedFiles()

            if self.selected_pdf_files:
                self.files_label.setText(f"נבחרו {len(self.selected_pdf_files)} קבצים")
                self.extract_btn.setEnabled(True)
            else:
                self.files_label.setText("לא נבחרו קבצים")
                self.extract_btn.setEnabled(False)

    def select_folder(self):
        """
        בחירת תיקייה עם קבצי PDF.
        """
        folder_path = QFileDialog.getExistingDirectory(self, "בחר תיקייה עם קבצי PDF")

        if folder_path:
            # איסוף כל קבצי ה-PDF בתיקייה
            pdf_files = []
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))

            self.selected_pdf_files = pdf_files

            if self.selected_pdf_files:
                self.files_label.setText(f"נבחרו {len(self.selected_pdf_files)} קבצים מתיקייה")
                self.extract_btn.setEnabled(True)
            else:
                self.files_label.setText("לא נמצאו קבצי PDF בתיקייה")
                self.extract_btn.setEnabled(False)

    def extract_data(self):
        """
        הפעלת תהליך חילוץ הנתונים.
        """
        if not self.selected_pdf_files:
            QMessageBox.warning(self, "שגיאה", "יש לבחור קבצי PDF לחילוץ")
            return

        # קבלת רשימת השדות הנבחרים
        selected_field_ids = self.field_selection.get_selected_field_ids()

        if not selected_field_ids:
            QMessageBox.warning(self, "שגיאה", "יש לבחור לפחות שדה אחד לחילוץ")
            return

        # הגדרת תצורת החילוץ
        extraction_config = ExtractionConfig()
        extraction_config.update_from_field_ids(selected_field_ids)

        # איפוס רכיב התוצאות
        self.results_widget.clear_results()

        # עדכון ממשק המשתמש
        self.progress_bar.setValue(0)
        self.extract_btn.setEnabled(False)
        self.status_label.setText("מתחיל חילוץ...")

        # הפעלת תהליכון החילוץ
        self.extraction_thread = ExtractionThread(self.selected_pdf_files, extraction_config)

        # חיבור אותות התהליכון
        self.extraction_thread.progress.connect(self.update_progress)
        self.extraction_thread.file_progress.connect(self.update_status)
        self.extraction_thread.extraction_complete.connect(self.handle_extraction_results)

        # הפעלת התהליכון
        self.extraction_thread.start()

    def update_progress(self, value):
        """
        עדכון פס ההתקדמות.

        Args:
            value (int): ערך ההתקדמות באחוזים
        """
        self.progress_bar.setValue(value)

    def update_status(self, file_name, percent):
        """
        עדכון הודעת סטטוס.

        Args:
            file_name (str): שם הקובץ המעובד כעת
            percent (float): אחוז ההתקדמות
        """
        message = f"מעבד קובץ {os.path.basename(file_name)}... ({int(percent)}%)"
        self.status_label.setText(message)

    def handle_extraction_results(self, results):
        """
        טיפול בתוצאות החילוץ.

        Args:
            results (list): רשימת תוצאות החילוץ
        """
        # עדכון ממשק המשתמש
        self.extract_btn.setEnabled(True)
        self.status_label.setText(f"הסתיים חילוץ של {len(results)} קבצים")

        # הצגת התוצאות
        self.results_widget.update_results(results, self.field_selection.get_selected_field_ids())

        # התאמת גדלים שוב לאחר מילוי התוצאות
        self.splitter.setSizes([200, 600])