# -*- coding: utf-8 -*-

"""
וידג'ט לבחירת שדות לחילוץ.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QGridLayout, QCheckBox,
                             QPushButton, QLabel)
from PyQt5.QtGui import QFont
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FieldSelectionWidget(QWidget):
    """
    וידג'ט לבחירת שדות לחילוץ.
    """

    def __init__(self, config, parent=None):
        """
        אתחול וידג'ט בחירת שדות.

        Args:
            config (ApplicationConfig): הגדרות האפליקציה
            parent (QWidget, optional): רכיב האב
        """
        super().__init__(parent)

        self.config = config
        self.checkboxes = {}  # {field_id: QCheckBox}

        self.init_ui()

    def init_ui(self):
        """
        אתחול ממשק המשתמש של הוידג'ט.
        """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # כותרת
        self.title_label = QLabel("בחר שדות לחילוץ:")
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.title_label)

        # יצירת קבוצות השדות
        self._create_field_groups()

        # הוספת כפתורים לבחירת הכל / ניקוי הכל
        self.buttons_layout = QHBoxLayout()

        self.select_all_btn = QPushButton("בחר הכל")
        self.select_all_btn.clicked.connect(self.select_all)

        self.clear_all_btn = QPushButton("נקה הכל")
        self.clear_all_btn.clicked.connect(self.clear_all)

        self.buttons_layout.addWidget(self.select_all_btn)
        self.buttons_layout.addWidget(self.clear_all_btn)

        self.layout.addLayout(self.buttons_layout)

    def _create_field_groups(self):
        """
        יצירת קבוצות שדות לפי סוגים.
        """
        # קבוצה לשדות כלליים
        self.general_group = QGroupBox("שדות כלליים")
        self.general_layout = QGridLayout()
        self.general_group.setLayout(self.general_layout)
        self.layout.addWidget(self.general_group)

        # קבוצה לשדות בעלים
        self.owners_group = QGroupBox("שדות בעלים")
        self.owners_layout = QGridLayout()
        self.owners_group.setLayout(self.owners_layout)
        self.layout.addWidget(self.owners_group)

        # קבוצה לשדות משכנתאות
        self.mortgages_group = QGroupBox("שדות משכנתאות")
        self.mortgages_layout = QGridLayout()
        self.mortgages_group.setLayout(self.mortgages_layout)
        self.layout.addWidget(self.mortgages_group)

        # קבוצה לשדות הערות
        self.remarks_group = QGroupBox("שדות הערות")
        self.remarks_layout = QGridLayout()
        self.remarks_group.setLayout(self.remarks_layout)
        self.layout.addWidget(self.remarks_group)

        # מילוי השדות בקבוצות השונות
        self._populate_field_groups()

    def _populate_field_groups(self):
        """
        מילוי קבוצות השדות בשדות המתאימים.
        """
        # שדות כלליים
        self._add_fields_to_group(self.config.available_fields.get("general", []),
                                  self.general_layout)

        # שדות בעלים
        self._add_fields_to_group(self.config.available_fields.get("owners", []),
                                  self.owners_layout)

        # שדות משכנתאות
        self._add_fields_to_group(self.config.available_fields.get("mortgages", []),
                                  self.mortgages_layout)

        # שדות הערות
        self._add_fields_to_group(self.config.available_fields.get("remarks", []),
                                  self.remarks_layout)

    def _add_fields_to_group(self, fields, layout):
        """
        הוספת שדות לקבוצה.

        Args:
            fields (list): רשימת שדות להוספה
            layout (QGridLayout): הלייאאוט של הקבוצה
        """
        for i, field in enumerate(fields):
            field_id = field.get("id")
            field_name = field.get("name")
            default_selected = field.get("default", False)

            checkbox = QCheckBox(field_name)
            checkbox.setChecked(default_selected)

            row, col = divmod(i, 3)
            layout.addWidget(checkbox, row, col)

            self.checkboxes[field_id] = checkbox

    def select_all(self):
        """
        סימון כל השדות.
        """
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)

    def clear_all(self):
        """
        ניקוי כל הסימונים.
        """
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)

    def get_selected_field_ids(self):
        """
        קבלת רשימת מזהי השדות המסומנים.

        Returns:
            list: רשימת מזהי השדות שנבחרו
        """
        selected = []
        for field_id, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected.append(field_id)
        return selected

    def update_from_template(self, selected_field_ids):
        """
        עדכון הסימונים לפי תבנית.

        Args:
            selected_field_ids (list): רשימת מזהי שדות לסימון
        """
        # ראשית, נקה את כל הסימונים
        self.clear_all()

        # סמן את השדות הנבחרים בתבנית
        for field_id in selected_field_ids:
            if field_id in self.checkboxes:
                self.checkboxes[field_id].setChecked(True)