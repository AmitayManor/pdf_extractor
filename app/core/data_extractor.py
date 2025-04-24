# -*- coding: utf-8 -*-

"""
מודול לחילוץ מידע מובנה מטקסט.
"""

import re
from app.utils.regex_patterns import PATTERNS
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DataExtractor:
    """
    אחראי על חילוץ מידע מובנה מטקסט של נסח טאבו באמצעות ביטויים רגולריים וניתוח טקסט.
    """

    def __init__(self):
        """
        אתחול מחלץ הנתונים.
        """
        self.patterns = PATTERNS

    def extract_data_from_text(self, text_content, extraction_config):
        """
        חילוץ מידע מטקסט של נסח טאבו לפי תצורת החילוץ שהוגדרה.

        Args:
            text_content (str): הטקסט של הנסח
            extraction_config (ExtractionConfig): תצורת החילוץ

        Returns:
            dict: מידע מובנה שחולץ מהטקסט
        """
        if not text_content:
            return {}

        # התוצאה תכיל את כל הנתונים שחולצו
        result = {}

        try:
            # חילוץ נתונים כלליים
            self._extract_general_data(text_content, result, extraction_config)

            # חילוץ נתוני בעלים
            self._extract_owners_data(text_content, result, extraction_config)

            # חילוץ נתוני משכנתאות
            self._extract_mortgages_data(text_content, result, extraction_config)

            # חילוץ נתוני הערות
            self._extract_remarks_data(text_content, result, extraction_config)

            return result

        except Exception as e:
            logger.error(f"Error extracting data from text: {str(e)}")
            return result

    def _extract_general_data(self, text_content, result, extraction_config):
        """
        חילוץ נתונים כלליים מהטקסט.

        Args:
            text_content (str): הטקסט המלא
            result (dict): דיקשנרי התוצאות שיעודכן
            extraction_config (ExtractionConfig): תצורת החילוץ
        """
        # מספר נסח
        if 'nesach_number' in extraction_config.selected_field_ids:
            match = re.search(self.patterns['nesach_number'], text_content)
            if match:
                result['nesach_number'] = match.group(1).strip()

        # תאריך הפקה
        if 'date' in extraction_config.selected_field_ids:
            match = re.search(self.patterns['date'], text_content)
            if match:
                result['date'] = match.group(1).strip()

        # גוש
        if 'gush' in extraction_config.selected_field_ids:
            match = re.search(self.patterns['gush'], text_content)
            if match:
                result['gush'] = match.group(1).strip()

        # חלקה
        if 'helka' in extraction_config.selected_field_ids:
            match = re.search(self.patterns['helka'], text_content)
            if match:
                result['helka'] = match.group(1).strip()

        # שטח במ"ר
        if 'area' in extraction_config.selected_field_ids:
            match = re.search(self.patterns['area'], text_content)
            if match:
                result['area'] = match.group(1).strip()

        # רשות מקומית
        if 'authority' in extraction_config.selected_field_ids:
            match = re.search(self.patterns['authority'], text_content)
            if match:
                result['authority'] = match.group(1).strip()

        # סוג מקרקעין
        if 'land_type' in extraction_config.selected_field_ids:
            match = re.search(self.patterns['land_type'], text_content)
            if match:
                result['land_type'] = match.group(1).strip()

    def _extract_owners_data(self, text_content, result, extraction_config):
        """
        חילוץ נתוני בעלים מהטקסט.

        Args:
            text_content (str): הטקסט המלא
            result (dict): דיקשנרי התוצאות שיעודכן
            extraction_config (ExtractionConfig): תצורת החילוץ
        """
        owners_ids = {'owner_name', 'owner_id', 'owner_id_type', 'owner_share'}

        # בדיקה אם נדרש לחלץ נתוני בעלים
        if not owners_ids.intersection(extraction_config.selected_field_ids):
            return

        try:
            # חיפוש חלק בטקסט שמכיל את רשימת הבעלים
            owners_section = re.search(self.patterns['owners_section'], text_content, re.DOTALL)

            if owners_section:
                owners_text = owners_section.group(0)
                owners = []

                # התבנית מחפשת את הבעלים, מספר הזיהוי, סוג הזיהוי והחלק בנכס
                owner_pattern = re.finditer(self.patterns['owner_entry'], owners_text, re.DOTALL)

                for match in owner_pattern:
                    owner_name = match.group(1).strip() if match.group(1) else ""
                    id_number = match.group(2).strip() if match.group(2) else ""
                    share = match.group(3).strip() if match.group(3) else ""

                    owner_entry = {}

                    if 'owner_name' in extraction_config.selected_field_ids:
                        owner_entry['name'] = owner_name

                    if 'owner_id' in extraction_config.selected_field_ids:
                        owner_entry['id_number'] = id_number

                    if 'owner_id_type' in extraction_config.selected_field_ids:
                        # קביעת סוג זיהוי בהתאם לפורמט
                        if re.match(r'^\d+$', id_number):
                            owner_entry['id_type'] = "ת.ז"
                        elif re.match(r'^\d{3,9}$', id_number):
                            owner_entry['id_type'] = "חברה"
                        else:
                            owner_entry['id_type'] = "אחר"

                    if 'owner_share' in extraction_config.selected_field_ids:
                        owner_entry['share'] = share

                    owners.append(owner_entry)

                if owners:
                    result['owners'] = owners

        except Exception as e:
            logger.error(f"Error extracting owners data: {str(e)}")

    def _extract_mortgages_data(self, text_content, result, extraction_config):
        """
        חילוץ נתוני משכנתאות מהטקסט.

        Args:
            text_content (str): הטקסט המלא
            result (dict): דיקשנרי התוצאות שיעודכן
            extraction_config (ExtractionConfig): תצורת החילוץ
        """
        mortgage_ids = {'mortgage_holder', 'mortgage_amount', 'mortgage_rank'}

        # בדיקה אם נדרש לחלץ נתוני משכנתאות
        if not mortgage_ids.intersection(extraction_config.selected_field_ids):
            return

        try:
            # חיפוש חלק בטקסט שמכיל את רשימת המשכנתאות
            mortgages_section = re.search(self.patterns['mortgages_section'], text_content, re.DOTALL)

            if mortgages_section:
                mortgages_text = mortgages_section.group(0)
                mortgages = []

                # חיפוש פרטי כל משכנתה
                mortgage_pattern = re.finditer(self.patterns['mortgage_entry'], mortgages_text, re.DOTALL)

                for match in mortgage_pattern:
                    bank_name = match.group(1).strip() if match.group(1) else ""
                    rank = match.group(2).strip() if match.group(2) else ""
                    amount = match.group(3).strip() if match.group(3) else ""

                    mortgage_entry = {}

                    if 'mortgage_holder' in extraction_config.selected_field_ids:
                        mortgage_entry['holder'] = bank_name

                    if 'mortgage_rank' in extraction_config.selected_field_ids:
                        mortgage_entry['rank'] = rank

                    if 'mortgage_amount' in extraction_config.selected_field_ids:
                        mortgage_entry['amount'] = amount

                    mortgages.append(mortgage_entry)

                if mortgages:
                    result['mortgages'] = mortgages

        except Exception as e:
            logger.error(f"Error extracting mortgages data: {str(e)}")

    def _extract_remarks_data(self, text_content, result, extraction_config):
        """
        חילוץ נתוני הערות מהטקסט.

        Args:
            text_content (str): הטקסט המלא
            result (dict): דיקשנרי התוצאות שיעודכן
            extraction_config (ExtractionConfig): תצורת החילוץ
        """
        remark_ids = {'remark_type', 'remark_content'}

        # בדיקה אם נדרש לחלץ נתוני הערות
        if not remark_ids.intersection(extraction_config.selected_field_ids):
            return

        try:
            # חיפוש חלק בטקסט שמכיל את רשימת ההערות
            remarks_section = re.search(self.patterns['remarks_section'], text_content, re.DOTALL)

            if remarks_section:
                remarks_text = remarks_section.group(0)
                remarks = []

                # חיפוש פרטי כל הערה
                remark_pattern = re.finditer(self.patterns['remark_entry'], remarks_text, re.DOTALL)

                for match in remark_pattern:
                    remark_type = match.group(1).strip() if match.group(1) else ""
                    beneficiary = match.group(2).strip() if match.group(2) else ""

                    remark_entry = {}

                    if 'remark_type' in extraction_config.selected_field_ids:
                        remark_entry['type'] = remark_type

                    if 'remark_content' in extraction_config.selected_field_ids:
                        remark_entry['content'] = beneficiary

                    remarks.append(remark_entry)

                if remarks:
                    result['remarks'] = remarks

        except Exception as e:
            logger.error(f"Error extracting remarks data: {str(e)}")