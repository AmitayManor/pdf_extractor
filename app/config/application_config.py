# -*- coding: utf-8 -*-

"""
הגדרות האפליקציה.
"""

import os
import json
from pathlib import Path
from app.config.constants import DEFAULT_FIELDS


class ApplicationConfig:
    """
    ניהול הגדרות האפליקציה, כולל הגדרות משתמש ונתיבי קבצים.
    """

    def __init__(self):
        """
        אתחול הגדרות האפליקציה.
        """
        # נתיב ספריית הגדרות המשתמש
        self.user_config_dir = Path.home() / "PDFExtractor"
        self.templates_dir = self.user_config_dir / "templates"

        # יצירת ספריות הגדרות אם לא קיימות
        self._ensure_directories_exist()

        # טעינת הגדרות ברירת מחדל
        self.available_fields = DEFAULT_FIELDS

    def _ensure_directories_exist(self):
        """
        וידוא קיום ספריות ההגדרות.
        """
        self.user_config_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def save_template(self, template_data):
        """
        שמירת תבנית הגדרות לקובץ.

        Args:
            template_data (dict): נתוני התבנית לשמירה

        Returns:
            bool: האם השמירה הצליחה
        """
        try:
            template_name = template_data.get("name", "")
            if not template_name:
                return False

            template_file = self.templates_dir / f"{template_name}.json"

            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"Error saving template: {str(e)}")
            return False

    def load_template(self, template_name):
        """
        טעינת תבנית הגדרות מקובץ.

        Args:
            template_name (str): שם התבנית לטעינה

        Returns:
            dict או None: נתוני התבנית אם נטענה בהצלחה, אחרת None
        """
        try:
            template_file = self.templates_dir / f"{template_name}.json"

            if not template_file.exists():
                return None

            with open(template_file, 'r', encoding='utf-8') as f:
                template_data = json.load(f)

            return template_data

        except Exception as e:
            print(f"Error loading template: {str(e)}")
            return None

    def get_available_templates(self):
        """
        קבלת רשימת התבניות הזמינות.

        Returns:
            list: רשימת דיקשנרי עם פרטי התבניות הזמינות
        """
        templates = []

        try:
            template_files = list(self.templates_dir.glob("*.json"))

            for template_file in template_files:
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)

                    templates.append({
                        "file_path": str(template_file),
                        "name": template_data.get("name", template_file.stem),
                        "description": template_data.get("description", ""),
                        "data": template_data
                    })

                except Exception as e:
                    print(f"Error loading template {template_file}: {str(e)}")

        except Exception as e:
            print(f"Error listing templates: {str(e)}")

        return templates