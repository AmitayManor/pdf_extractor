# -*- coding: utf-8 -*-

"""
מודל שדה - מייצג שדה לחילוץ מנסח טאבו.
"""


class Field:
    """
    מחלקה המייצגת שדה לחילוץ.
    """

    def __init__(self, field_id, name, default_selected=False, group=None):
        """
        אתחול שדה.

        Args:
            field_id (str): מזהה השדה
            name (str): שם השדה בעברית
            default_selected (bool, optional): האם השדה נבחר כברירת מחדל
            group (str, optional): קבוצת השדה (כללי, בעלים, משכנתאות, הערות)
        """
        self.id = field_id
        self.name = name
        self.default_selected = default_selected
        self.group = group

    def to_dict(self):
        """
        המרת השדה לדיקשנרי.

        Returns:
            dict: דיקשנרי המייצג את השדה
        """
        return {
            "id": self.id,
            "name": self.name,
            "default": self.default_selected,
            "group": self.group
        }

    @classmethod
    def from_dict(cls, field_dict):
        """
        יצירת שדה מדיקשנרי.

        Args:
            field_dict (dict): דיקשנרי המייצג שדה

        Returns:
            Field: אובייקט שדה חדש
        """
        return cls(
            field_dict.get("id", ""),
            field_dict.get("name", ""),
            field_dict.get("default", False),
            field_dict.get("group", None)
        )