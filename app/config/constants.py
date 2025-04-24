# -*- coding: utf-8 -*-

"""
קבועים של האפליקציה.
"""

# רשימת השדות האפשריים לחילוץ
DEFAULT_FIELDS = {
    "general": [
        {"id": "nesach_number", "name": "מספר נסח", "default": True},
        {"id": "date", "name": "תאריך הפקה", "default": True},
        {"id": "gush", "name": "גוש", "default": True},
        {"id": "helka", "name": "חלקה", "default": True},
        {"id": "area", "name": "שטח במ\"ר", "default": True},
        {"id": "authority", "name": "רשות מקומית", "default": True},
        {"id": "land_type", "name": "סוג מקרקעין", "default": True}
    ],
    "owners": [
        {"id": "owner_name", "name": "בעלים - שם", "default": True},
        {"id": "owner_id", "name": "בעלים - מספר זיהוי", "default": True},
        {"id": "owner_id_type", "name": "בעלים - סוג זיהוי", "default": True},
        {"id": "owner_share", "name": "בעלים - חלק בנכס", "default": True}
    ],
    "mortgages": [
        {"id": "mortgage_holder", "name": "משכנתאות - בעל המשכנתה", "default": True},
        {"id": "mortgage_amount", "name": "משכנתאות - סכום", "default": True},
        {"id": "mortgage_rank", "name": "משכנתאות - דרגה", "default": True}
    ],
    "remarks": [
        {"id": "remark_type", "name": "הערות - סוג הערה", "default": True},
        {"id": "remark_content", "name": "הערות - תוכן", "default": True}
    ]
}

# מיפוי בין מזהי שדות לשמות עבריים
FIELD_ID_TO_NAME = {
    "nesach_number": "מספר נסח",
    "date": "תאריך הפקה",
    "gush": "גוש",
    "helka": "חלקה",
    "area": "שטח במ\"ר",
    "authority": "רשות מקומית",
    "land_type": "סוג מקרקעין",
    "owner_name": "בעלים - שם",
    "owner_id": "בעלים - מספר זיהוי",
    "owner_id_type": "בעלים - סוג זיהוי",
    "owner_share": "בעלים - חלק בנכס",
    "mortgage_holder": "משכנתאות - בעל המשכנתה",
    "mortgage_amount": "משכנתאות - סכום",
    "mortgage_rank": "משכנתאות - דרגה",
    "remark_type": "הערות - סוג הערה",
    "remark_content": "הערות - תוכן"
}

# מיפוי לקבלת מזהה שדה משם עברי
FIELD_NAME_TO_ID = {v: k for k, v in FIELD_ID_TO_NAME.items()}

# שם האפליקציה
APP_NAME = "מחלץ נתונים מנסחי טאבו"

# גודל חלון ברירת מחדל
DEFAULT_WINDOW_SIZE = (1200, 800)