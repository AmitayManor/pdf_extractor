# -*- coding: utf-8 -*-

"""
וידג'ט להצגת תוצאות החילוץ.
"""

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFileDialog, QMessageBox, QTabWidget,
                             QSplitter, QTextEdit)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from app.config.constants import FIELD_ID_TO_NAME
from app.core.export_manager import ExportManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ResultsWidget(QWidget):
    """
    וידג'ט להצגת תוצאות החילוץ.
    """

    def __init__(self, parent=None):
        """
        אתחול וידג'ט תוצאות החילוץ.

        Args:
            parent (QWidget, optional): רכיב האב
        """
        super().__init__(parent)

        self.export_manager = ExportManager()
        self.extraction_results = []
        self.selected_field_ids = []

        self.init_ui()

    def init_ui(self):
        """
        אתחול ממשק המשתמש של הוידג'ט.
        """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # כותרת
        self.title_label = QLabel("תוצאות חילוץ:")
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.title_label)

        # טאבים להצגת נתונים
        self.tabs = QTabWidget()

        # טאב טבלה מרכזית
        self.table_tab = QWidget()
        self.table_layout = QVBoxLayout(self.table_tab)

        # טבלה להצגת התוצאות
        self.results_table = QTableWidget()
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table_layout.addWidget(self.results_table)

        # טאב פרטים מורחבים
        self.details_tab = QWidget()
        self.details_layout = QVBoxLayout(self.details_tab)

        # פיצול המסך לרשימת קבצים ופרטים
        self.details_splitter = QSplitter(Qt.Horizontal)

        # טבלת קבצים בצד ימין
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(2)
        self.files_table.setHorizontalHeaderLabels(["שם קובץ", "סטטוס"])
        self.files_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.files_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.files_table.selectionModel().selectionChanged.connect(self.file_selected)

        # פרטי המסמך בצד שמאל
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)

        self.details_splitter.addWidget(self.files_table)
        self.details_splitter.addWidget(self.details_text)
        self.details_splitter.setSizes([200, 600])

        self.details_layout.addWidget(self.details_splitter)

        # הוספת הטאבים
        self.tabs.addTab(self.table_tab, "טבלת נתונים")
        self.tabs.addTab(self.details_tab, "פרטים מורחבים")

        self.layout.addWidget(self.tabs)

        # כפתורים לייצוא ועריכה
        self.buttons_layout = QHBoxLayout()

        self.export_excel_btn = QPushButton("ייצא לאקסל")
        self.export_excel_btn.clicked.connect(self.export_to_excel)

        self.export_csv_btn = QPushButton("ייצא ל-CSV")
        self.export_csv_btn.clicked.connect(self.export_to_csv)

        self.edit_btn = QPushButton("ערוך נתונים")
        self.edit_btn.clicked.connect(self.edit_data)

        self.buttons_layout.addWidget(self.export_excel_btn)
        self.buttons_layout.addWidget(self.export_csv_btn)
        self.buttons_layout.addWidget(self.edit_btn)

        self.layout.addLayout(self.buttons_layout)

    def update_results(self, results, selected_field_ids):
        """
        עדכון התוצאות בטבלה.

        Args:
            results (list): רשימת תוצאות החילוץ
            selected_field_ids (list): רשימת מזהי השדות שנבחרו
        """
        self.extraction_results = results
        self.selected_field_ids = selected_field_ids

        # עדכון טבלת התוצאות
        self._update_results_table()

        # עדכון טבלת הקבצים בטאב הפרטים
        self._update_files_table()

        # מעבר לטאב הטבלה
        self.tabs.setCurrentIndex(0)

    def _update_results_table(self):
        """
        עדכון טבלת התוצאות הראשית.
        """
        # ניקוי הטבלה
        self.results_table.clear()
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(0)

        if not self.extraction_results or not self.selected_field_ids:
            return

        # קביעת כותרות הטבלה
        headers = ["שם קובץ"]
        for field_id in self.selected_field_ids:
            headers.append(FIELD_ID_TO_NAME.get(field_id, field_id))

        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)

        # מילוי הטבלה בנתונים
        for idx, result in enumerate(self.extraction_results):
            if result.has_error():
                continue  # דלג על תוצאות עם שגיאות

            self.results_table.insertRow(idx)

            # הוספת שם הקובץ
            file_item = QTableWidgetItem(result.file_name)
            self.results_table.setItem(idx, 0, file_item)

            # הוספת הנתונים שחולצו
            data = result.data

            for col_idx, field_id in enumerate(self.selected_field_ids, 1):
                cell_value = self._get_field_display_value(data, field_id)
                item = QTableWidgetItem(cell_value)
                self.results_table.setItem(idx, col_idx, item)

        # התאמת גודל הטבלה
        self.results_table.resizeColumnsToContents()
        self.results_table.resizeRowsToContents()

    def _update_files_table(self):
        """
        עדכון טבלת הקבצים בטאב הפרטים.
        """
        # ניקוי הטבלה
        self.files_table.setRowCount(0)

        if not self.extraction_results:
            return

        # מילוי טבלת הקבצים
        for idx, result in enumerate(self.extraction_results):
            self.files_table.insertRow(idx)

            # שם הקובץ
            file_item = QTableWidgetItem(result.file_name)
            self.files_table.setItem(idx, 0, file_item)

            # סטטוס
            status = "שגיאה: " + result.error if result.has_error() else "חולץ בהצלחה"
            status_item = QTableWidgetItem(status)

            # צביעת סטטוס לפי הצלחה/כישלון
            if result.has_error():
                status_item.setForeground(QColor("red"))
            else:
                status_item.setForeground(QColor("green"))

            self.files_table.setItem(idx, 1, status_item)

        # התאמת גודל הטבלה
        self.files_table.resizeColumnsToContents()
        self.files_table.resizeRowsToContents()

    def file_selected(self):
        """
        טיפול באירוע של בחירת קובץ מרשימת הקבצים.
        """
        selected_rows = self.files_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row >= 0 and row < len(self.extraction_results):
            self._display_file_details(self.extraction_results[row])

    def _display_file_details(self, result):
        """
        הצגת פרטי חילוץ מורחבים של קובץ.

        Args:
            result (ExtractionResult): תוצאת החילוץ להצגה
        """
        if result.has_error():
            details = f"<h3>שגיאה בחילוץ הקובץ</h3>"
            details += f"<p><b>שם הקובץ:</b> {result.file_name}</p>"
            details += f"<p><b>נתיב מלא:</b> {result.file_path}</p>"
            details += f"<p><b>שגיאה:</b> <span style='color:red'>{result.error}</span></p>"
            self.details_text.setHtml(details)
            return

        details = f"<h3>פרטי חילוץ</h3>"
        details += f"<p><b>שם הקובץ:</b> {result.file_name}</p>"
        details += f"<p><b>נתיב מלא:</b> {result.file_path}</p>"

        # הצגת נתונים כלליים
        details += "<h4>נתונים כלליים</h4>"
        details += "<ul>"
        for field_id in self.selected_field_ids:
            if not field_id.startswith(("owner_", "mortgage_", "remark_")):
                field_name = FIELD_ID_TO_NAME.get(field_id, field_id)
                value = result.data.get(field_id, "")
                details += f"<li><b>{field_name}:</b> {value}</li>"
        details += "</ul>"

        # הצגת נתוני בעלים
        if any(field_id.startswith("owner_") for field_id in self.selected_field_ids):
            details += "<h4>פרטי בעלים</h4>"
            owners = result.data.get("owners", [])
            if owners:
                details += "<table border='1' cellpadding='5' style='border-collapse: collapse;'>"

                # כותרות
                details += "<tr>"
                owner_fields = ["name", "id_number", "id_type", "share"]
                owner_field_names = ["שם", "מספר זיהוי", "סוג זיהוי", "חלק בנכס"]

                for field_name in owner_field_names:
                    details += f"<th>{field_name}</th>"
                details += "</tr>"

                # נתונים
                for owner in owners:
                    details += "<tr>"
                    for field in owner_fields:
                        value = owner.get(field, "")
                        details += f"<td>{value}</td>"
                    details += "</tr>"

                details += "</table>"
            else:
                details += "<p>לא נמצאו נתוני בעלים</p>"

        # הצגת נתוני משכנתאות
        if any(field_id.startswith("mortgage_") for field_id in self.selected_field_ids):
            details += "<h4>פרטי משכנתאות</h4>"
            mortgages = result.data.get("mortgages", [])
            if mortgages:
                details += "<table border='1' cellpadding='5' style='border-collapse: collapse;'>"

                # כותרות
                details += "<tr>"
                mortgage_fields = ["holder", "rank", "amount"]
                mortgage_field_names = ["בעל המשכנתה", "דרגה", "סכום"]

                for field_name in mortgage_field_names:
                    details += f"<th>{field_name}</th>"
                details += "</tr>"

                # נתונים
                for mortgage in mortgages:
                    details += "<tr>"
                    for field in mortgage_fields:
                        value = mortgage.get(field, "")
                        details += f"<td>{value}</td>"
                    details += "</tr>"

                details += "</table>"
            else:
                details += "<p>לא נמצאו נתוני משכנתאות</p>"

        # הצגת נתוני הערות
        if any(field_id.startswith("remark_") for field_id in self.selected_field_ids):
            details += "<h4>פרטי הערות</h4>"
            remarks = result.data.get("remarks", [])
            if remarks:
                details += "<table border='1' cellpadding='5' style='border-collapse: collapse;'>"

                # כותרות
                details += "<tr>"
                remark_fields = ["type", "content"]
                remark_field_names = ["סוג הערה", "תוכן"]

                for field_name in remark_field_names:
                    details += f"<th>{field_name}</th>"
                details += "</tr>"

                # נתונים
                for remark in remarks:
                    details += "<tr>"
                    for field in remark_fields:
                        value = remark.get(field, "")
                        details += f"<td>{value}</td>"
                    details += "</tr>"

                details += "</table>"
            else:
                details += "<p>לא נמצאו נתוני הערות</p>"

        self.details_text.setHtml(details)

    def _get_field_display_value(self, data, field_id):
        """
        חילוץ ערך להצגה עבור שדה.

        Args:
            data (dict): נתוני החילוץ
            field_id (str): מזהה השדה

        Returns:
            str: הערך להצגה
        """
        # טיפול בשדות בעלים
        if field_id.startswith("owner_"):
            owners = data.get("owners", [])
            if not owners:
                return ""

            field_parts = field_id.split("_", 1)
            if len(field_parts) > 1:
                field_type = field_parts[1]
                owners_data = []

                mapping = {
                    "name": "name",
                    "id": "id_number",
                    "id_type": "id_type",
                    "share": "share"
                }

                if field_type in mapping:
                    for owner in owners:
                        value = owner.get(mapping[field_type], "")
                        if value:
                            owners_data.append(str(value))

                return ", ".join(owners_data)

        # טיפול בשדות משכנתאות
        elif field_id.startswith("mortgage_"):
            mortgages = data.get("mortgages", [])
            if not mortgages:
                return ""

            field_parts = field_id.split("_", 1)
            if len(field_parts) > 1:
                field_type = field_parts[1]
                mortgage_data = []

                mapping = {
                    "holder": "holder",
                    "amount": "amount",
                    "rank": "rank"
                }

                if field_type in mapping:
                    for mortgage in mortgages:
                        value = mortgage.get(mapping[field_type], "")
                        if value:
                            mortgage_data.append(str(value))

                return ", ".join(mortgage_data)

        # טיפול בשדות הערות
        elif field_id.startswith("remark_"):
            remarks = data.get("remarks", [])
            if not remarks:
                return ""

            field_parts = field_id.split("_", 1)
            if len(field_parts) > 1:
                field_type = field_parts[1]
                remark_data = []

                mapping = {
                    "type": "type",
                    "content": "content"
                }

                if field_type in mapping:
                    for remark in remarks:
                        value = remark.get(mapping[field_type], "")
                        if value:
                            remark_data.append(str(value))

                return ", ".join(remark_data)

        # שדות רגילים
        else:
            return str(data.get(field_id, ""))

    def clear_results(self):
        """
        ניקוי כל התוצאות.
        """
        self.extraction_results = []
        self.selected_field_ids = []

        # ניקוי הטבלאות
        self.results_table.clear()
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(0)

        self.files_table.setRowCount(0)
        self.details_text.clear()

    def export_to_excel(self):
        """
        ייצוא הנתונים לקובץ אקסל.
        """
        if not self.extraction_results:
            QMessageBox.warning(self, "שגיאה", "אין נתונים לייצוא")
            return

        # בחירת מיקום לשמירת הקובץ
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "שמירת קובץ אקסל", "", "Excel Files (*.xlsx);;All Files (*)",
            options=options)

        if not file_name:
            return

        # הוספת סיומת אם צריך
        if not file_name.lower().endswith(".xlsx"):
            file_name += ".xlsx"

        # ייצוא הנתונים
        success = self.export_manager.export_to_excel(
            self.extraction_results, self.selected_field_ids, file_name)

        if success:
            QMessageBox.information(self, "ייצוא לאקסל",
                                    f"הנתונים יוצאו בהצלחה לקובץ:\n{file_name}")
        else:
            QMessageBox.critical(self, "שגיאה בייצוא",
                                 "אירעה שגיאה בייצוא הנתונים לאקסל")

    def export_to_csv(self):
        """
        ייצוא הנתונים לקובץ CSV.
        """
        if not self.extraction_results:
            QMessageBox.warning(self, "שגיאה", "אין נתונים לייצוא")
            return

        # בחירת מיקום לשמירת הקובץ
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "שמירת קובץ CSV", "", "CSV Files (*.csv);;All Files (*)",
            options=options)

        if not file_name:
            return

        # הוספת סיומת אם צריך
        if not file_name.lower().endswith(".csv"):
            file_name += ".csv"

        # ייצוא הנתונים
        success = self.export_manager.export_to_csv(
            self.extraction_results, self.selected_field_ids, file_name)

        if success:
            QMessageBox.information(self, "ייצוא ל-CSV",
                                    f"הנתונים יוצאו בהצלחה לקובץ:\n{file_name}")
        else:
            QMessageBox.critical(self, "שגיאה בייצוא",
                                 "אירעה שגיאה בייצוא הנתונים ל-CSV")

    def edit_data(self):
        """
        הפיכת הטבלה לניתנת לעריכה.
        """
        if not self.extraction_results:
            QMessageBox.warning(self, "שגיאה", "אין נתונים לעריכה")
            return

        # הפיכת הטבלה לניתנת לעריכה
        self.results_table.setEditTriggers(
            QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)

        QMessageBox.information(self, "עריכת נתונים",
                                "ניתן לערוך את הנתונים ישירות בטבלה על ידי לחיצה כפולה על התא המבוקש")

        # מעבר לטאב הטבלה
        self.tabs.setCurrentIndex(0)