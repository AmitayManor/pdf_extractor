# -*- coding: utf-8 -*-

"""
מודול ייצוא - אחראי על ייצוא נתונים לקבצים.
"""

import os
import pandas as pd
from app.config.constants import FIELD_ID_TO_NAME
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ExportManager:
    """
    אחראי על ייצוא נתונים מחולצים לפורמטים שונים.
    """

    def __init__(self):
        """
        אתחול מנהל הייצוא.
        """
        pass

    def export_to_excel(self, results, selected_fields, file_path):
        """
        ייצוא נתונים לקובץ אקסל.

        Args:
            results (list): רשימת תוצאות החילוץ
            selected_fields (list): רשימת מזהי השדות שנבחרו
            file_path (str): נתיב לקובץ האקסל שייווצר

        Returns:
            bool: האם הייצוא הצליח
        """
        try:
            # הכנת הנתונים לייצוא
            data_rows = self._prepare_data_for_export(results, selected_fields)

            # יצירת DataFrame ושמירה לאקסל
            df = pd.DataFrame(data_rows)

            # בדיקה אם הקובץ קיים, ואם כן - ניסיון לסגור אותו
            if os.path.exists(file_path):
                try:
                    # נסיון למחוק את הקובץ הקיים
                    os.remove(file_path)
                except Exception as e:
                    logger.error(f"Error removing existing file {file_path}: {str(e)}")
                    return False

            # שמירה לקובץ אקסל
            df.to_excel(file_path, index=False)

            return True

        except Exception as e:
            logger.error(f"Error exporting to Excel: {str(e)}")
            return False

    def export_to_csv(self, results, selected_fields, file_path):
        """
        ייצוא נתונים לקובץ CSV.

        Args:
            results (list): רשימת תוצאות החילוץ
            selected_fields (list): רשימת מזהי השדות שנבחרו
            file_path (str): נתיב לקובץ ה-CSV שייווצר

        Returns:
            bool: האם הייצוא הצליח
        """
        try:
            # הכנת הנתונים לייצוא
            data_rows = self._prepare_data_for_export(results, selected_fields)

            # יצירת DataFrame ושמירה ל-CSV
            df = pd.DataFrame(data_rows)

            # שמירה לקובץ CSV עם קידוד UTF-8-sig (תומך בעברית)
            df.to_csv(file_path, index=False, encoding='utf-8-sig')

            return True

        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return False

    def _prepare_data_for_export(self, results, selected_fields):
        """
        הכנת נתונים לייצוא.

        Args:
            results (list): רשימת תוצאות החילוץ
            selected_fields (list): רשימת מזהי השדות שנבחרו

        Returns:
            list: רשימת שורות נתונים מוכנה לייצוא
        """
        data_rows = []

        for result in results:
            # דלג על תוצאות עם שגיאות
            if result.has_error():
                continue

            # בסיס השורה - שם הקובץ
            row_data = {"שם קובץ": result.file_name}
            data = result.data

            # הוספת נתונים פשוטים
            for field_id in selected_fields:
                if field_id.startswith("owner_"):
                    # טיפול בשדות בעלים
                    owners = data.get("owners", [])
                    if owners:
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

                            row_data[FIELD_ID_TO_NAME.get(field_id, field_id)] = ", ".join(owners_data)

                elif field_id.startswith("mortgage_"):
                    # טיפול בשדות משכנתאות
                    mortgages = data.get("mortgages", [])
                    if mortgages:
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

                            row_data[FIELD_ID_TO_NAME.get(field_id, field_id)] = ", ".join(mortgage_data)

                elif field_id.startswith("remark_"):
                    # טיפול בשדות הערות
                    remarks = data.get("remarks", [])
                    if remarks:
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

                            row_data[FIELD_ID_TO_NAME.get(field_id, field_id)] = ", ".join(remark_data)

                else:
                    # שדות רגילים
                    display_name = FIELD_ID_TO_NAME.get(field_id, field_id)
                    row_data[display_name] = data.get(field_id, "")

            data_rows.append(row_data)

        return data_rows