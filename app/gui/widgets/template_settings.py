# -*- coding: utf-8 -*-

"""
וידג'ט להגדרות תבנית החילוץ.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QTextEdit, QPushButton,
                             QMessageBox, QComboBox, QDialog, QListWidget)
from PyQt5.QtGui import QFont
from app.models.template import Template
from app.utils.logger import get_logger

logger = get_logger(__name__)


class TemplateSettingsWidget(QWidget):
    """
    וידג'ט להגדרות תבנית החילוץ.
    """

    def __init__(self, config, field_selection, parent=None):
        """
        אתחול וידג'ט הגדרות תבנית.

        Args:
            config (ApplicationConfig): הגדרות האפליקציה
            field_selection (FieldSelectionWidget): וידג'ט בחירת השדות
            parent (QWidget, optional): רכיב האב
        """
        super().__init__(parent)

        self.config = config
        self.field_selection = field_selection

        self.init_ui()

    def init_ui(self):
        """
        אתחול ממשק המשתמש של הוידג'ט.
        """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # כותרת
        self.title_label = QLabel("הגדרות תבנית:")
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.title_label)

        # שם התבנית
        self.template_name_layout = QHBoxLayout()
        self.template_name_label = QLabel("שם התבנית:")
        self.template_name_input = QLineEdit()
        self.template_name_input.setPlaceholderText("הזן שם לתבנית")

        self.template_name_layout.addWidget(self.template_name_label)
        self.template_name_layout.addWidget(self.template_name_input)

        self.layout.addLayout(self.template_name_layout)

        # תיאור התבנית
        self.template_desc_layout = QHBoxLayout()
        self.template_desc_label = QLabel("תיאור התבנית:")
        self.template_desc_input = QTextEdit()
        self.template_desc_input.setPlaceholderText("הזן תיאור לתבנית")
        self.template_desc_input.setMaximumHeight(80)

        self.template_desc_layout.addWidget(self.template_desc_label)
        self.template_desc_layout.addWidget(self.template_desc_input)

        self.layout.addLayout(self.template_desc_layout)

        # כפתורי שמירה וטעינה של תבניות
        self.template_buttons_layout = QHBoxLayout()

        self.save_template_btn = QPushButton("שמור תבנית")
        self.save_template_btn.clicked.connect(self.save_template)

        self.load_template_btn = QPushButton("טען תבנית")
        self.load_template_btn.clicked.connect(self.load_template)

        self.template_buttons_layout.addWidget(self.save_template_btn)
        self.template_buttons_layout.addWidget(self.load_template_btn)

        self.layout.addLayout(self.template_buttons_layout)

        # רשימת תבניות שמורות
        self.templates_combo_layout = QHBoxLayout()
        self.templates_combo_label = QLabel("תבניות שמורות:")
        self.templates_combo = QComboBox()
        self.refresh_btn = QPushButton("רענן")
        self.refresh_btn.clicked.connect(self.refresh_templates_list)

        self.templates_combo_layout.addWidget(self.templates_combo_label)
        self.templates_combo_layout.addWidget(self.templates_combo)
        self.templates_combo_layout.addWidget(self.refresh_btn)

        self.layout.addLayout(self.templates_combo_layout)

        # טעינת רשימת התבניות
        self.refresh_templates_list()

        # הוספת מרווח
        self.layout.addStretch()

    def refresh_templates_list(self):
        """
        רענון רשימת התבניות.
        """
        self.templates_combo.clear()

        try:
            templates = self.config.get_available_templates()

            if templates:
                for template in templates:
                    self.templates_combo.addItem(template.get("name", ""), template)

            # הוספת אפשרות ריקה בתחילת הרשימה
            self.templates_combo.insertItem(0, "בחר תבנית...", None)
            self.templates_combo.setCurrentIndex(0)

            # חיבור אירוע החלפת פריט ברשימה
            self.templates_combo.currentIndexChanged.connect(self.template_selected)

        except Exception as e:
            logger.error(f"Error refreshing templates list: {str(e)}")

    def template_selected(self, index):
        """
        טיפול באירוע בחירת תבנית מהרשימה.

        Args:
            index (int): האינדקס שנבחר
        """
        if index <= 0:
            return

        template_data = self.templates_combo.currentData()
        if template_data:
            self.load_template_data(template_data)

    def load_template_data(self, template_data):
        """
        טעינת נתוני תבנית מסוימת.

        Args:
            template_data (dict): נתוני התבנית
        """
        try:
            # עדכון שדות הטופס
            self.template_name_input.setText(template_data.get("name", ""))
            self.template_desc_input.setText(template_data.get("description", ""))

            # עדכון השדות המסומנים
            selected_field_ids = template_data.get("data", {}).get("selected_field_ids", [])
            self.field_selection.update_from_template(selected_field_ids)

            QMessageBox.information(self, "טעינת תבנית",
                                    f"התבנית '{template_data.get('name', '')}' נטענה בהצלחה")

        except Exception as e:
            logger.error(f"Error loading template data: {str(e)}")
            QMessageBox.warning(self, "שגיאה", f"אירעה שגיאה בטעינת התבנית: {str(e)}")

    def save_template(self):
        """
        שמירת תבנית נוכחית.
        """
        # בדיקה שהוזן שם לתבנית
        template_name = self.template_name_input.text().strip()
        if not template_name:
            QMessageBox.warning(self, "שגיאה", "יש להזין שם לתבנית")
            return

        # קבלת השדות המסומנים
        selected_field_ids = self.field_selection.get_selected_field_ids()

        # הכנת נתוני התבנית
        template = Template(
            name=template_name,
            description=self.template_desc_input.toPlainText(),
            selected_field_ids=selected_field_ids
        )

        # שמירת התבנית
        success = self.config.save_template(template.to_dict())

        if success:
            QMessageBox.information(self, "שמירת תבנית",
                                    f"התבנית '{template_name}' נשמרה בהצלחה")
            # רענון רשימת התבניות
            self.refresh_templates_list()
        else:
            QMessageBox.warning(self, "שגיאה", "אירעה שגיאה בשמירת התבנית")

    def load_template(self):
        """
        טעינת תבנית קיימת מתוך חלון בחירה.
        """
        try:
            # קבלת רשימת התבניות הזמינות
            templates = self.config.get_available_templates()

            if not templates:
                QMessageBox.warning(self, "שגיאה", "לא נמצאו תבניות שמורות")
                return

            # פתיחת חלון בחירת תבנית
            dialog = TemplateSelectionDialog(templates, parent=self)

            if dialog.exec_() == QDialog.Accepted:
                selected_template = dialog.get_selected_template()
                if selected_template:
                    self.load_template_data(selected_template)

        except Exception as e:
            logger.error(f"Error in load_template: {str(e)}")
            QMessageBox.warning(self, "שגיאה", f"אירעה שגיאה בטעינת התבנית: {str(e)}")


class TemplateSelectionDialog(QDialog):
    """
    חלון דיאלוג לבחירת תבנית מרשימה.
    """

    def __init__(self, templates, parent=None):
        """
        אתחול חלון בחירת תבנית.

        Args:
            templates (list): רשימת תבניות זמינות
            parent (QWidget, optional): רכיב האב
        """
        super().__init__(parent)

        self.templates = templates
        self.selected_template = None

        self.init_ui()

    def init_ui(self):
        """
        אתחול ממשק המשתמש של החלון.
        """
        self.setWindowTitle("בחירת תבנית")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # כותרת
        label = QLabel("בחר תבנית מהרשימה:")
        label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(label)

        # רשימת תבניות
        self.templates_list = QListWidget()
        for template in self.templates:
            self.templates_list.addItem(template.get("name", ""))
        layout.addWidget(self.templates_list)

        # כפתורים
        buttons_layout = QHBoxLayout()

        ok_btn = QPushButton("בחר")
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("בטל")
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

    def accept(self):
        """
        אישור הבחירה.
        """
        current_row = self.templates_list.currentRow()
        if current_row >= 0 and current_row < len(self.templates):
            self.selected_template = self.templates[current_row]
            super().accept()
        else:
            QMessageBox.warning(self, "שגיאה", "יש לבחור תבנית מהרשימה")

    def get_selected_template(self):
        """
        קבלת התבנית שנבחרה.

        Returns:
            dict: נתוני התבנית שנבחרה
        """
        return self.selected_template