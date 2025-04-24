# -*- coding: utf-8 -*-

"""
מודל תבנית - מייצג תבנית חילוץ שנשמרה.
"""

import datetime


class Template:
    """
    מחלקה המייצגת תבנית חילוץ שנשמרה.
    """

    def __init__(self, name, description="", selected_field_ids=None):
        """
        אתחול תבנית חילוץ.

        Args:
            name (str): שם התבנית
            description (str, optional): תיאור התבנית
            selected_field_ids (list, optional): רשימת מזהי השדות שנבחרו בתבנית
        """
        self.name = name
        self.description = description
        self.selected_field_ids = selected_field_ids or []
        self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self):
        """
        המרת התבנית לדיקשנרי.

        Returns:
            dict: דיקשנרי המייצג את התבנית
        """
        return {
            "name": self.name,
            "description": self.description,
            "selected_field_ids": self.selected_field_ids,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, template_dict):
        """
        יצירת תבנית מדיקשנרי.

        Args:
            template_dict (dict): דיקשנרי המייצג תבנית

        Returns:
            Template: אובייקט תבנית חדש
        """
        template = cls(
            template_dict.get("name", ""),
            template_dict.get("description", ""),
            template_dict.get("selected_field_ids", [])
        )

        # שחזור תאריך היצירה המקורי
        if "created_at" in template_dict:
            template.created_at = template_dict["created_at"]

        return template