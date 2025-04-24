# -*- coding: utf-8 -*-

"""
מודל תצורת חילוץ - מייצג את הגדרות החילוץ והשדות שיש לחלץ.
"""

from app.config.constants import FIELD_NAME_TO_ID


class ExtractionConfig:
    """
    מחלקה המייצגת תצורת חילוץ - אילו שדות ונתונים יש לחלץ.
    """

    def __init__(self, selected_field_names=None):
        """
        אתחול תצורת החילוץ.

        Args:
            selected_field_names (list, optional): רשימת שמות השדות שנבחרו לחילוץ
        """
        # רשימת מזהי שדות שנבחרו לחילוץ
        self.selected_field_ids = []

        # עדכון רשימת השדות אם סופקה
        if selected_field_names:
            self.update_from_field_names(selected_field_names)

    def update_from_field_names(self, field_names):
        """
        עדכון תצורת החילוץ מרשימת שמות שדות.

        Args:
            field_names (list): רשימת שמות שדות בעברית
        """
        self.selected_field_ids = []

        for field_name in field_names:
            if field_name in FIELD_NAME_TO_ID:
                self.selected_field_ids.append(FIELD_NAME_TO_ID[field_name])

    def update_from_field_ids(self, field_ids):
        """
        עדכון תצורת החילוץ מרשימת מזהי שדות.

        Args:
            field_ids (list): רשימת מזהי שדות
        """
        self.selected_field_ids = list(field_ids)

    def to_dict(self):
        """
        המרת תצורת החילוץ לדיקשנרי.

        Returns:
            dict: דיקשנרי המייצג את תצורת החילוץ
        """
        return {
            "selected_field_ids": self.selected_field_ids
        }

    @classmethod
    def from_dict(cls, config_dict):
        """
        יצירת תצורת חילוץ מדיקשנרי.

        Args:
            config_dict (dict): דיקשנרי המייצג תצורת חילוץ

        Returns:
            ExtractionConfig: אובייקט תצורת חילוץ חדש
        """
        config = cls()

        if "selected_field_ids" in config_dict:
            config.selected_field_ids = list(config_dict["selected_field_ids"])

        return config