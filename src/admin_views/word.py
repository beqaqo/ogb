from datetime import datetime

from src.admin_views.base import SecureModelView

class WordView(SecureModelView):
    can_delete = True

    edit_modal = True

    column_list = ("paragraph", "text", "position")
    column_editable_list = ("text", "position")
    column_searchable_list = ("paragraph.text", "text", "position")
    column_filters = ("paragraph", "text", "position")

    form_edit_rules = (
        "paragraph",
        "position",
        "text",
        "lemma",
        "grammar",
        "greek_text", 
        "armenian_text", 
        "english_text",)

    column_labels = {
        'paragraph': 'მუხლი',
        'text': 'სიტყვა',
        'position': 'რიგითობა',
        'lemma': 'ლემა',
        'grammar': 'მორფოლოგიური თეგები',
        'greek_text': 'ბერძნული თარგმანი',
        'armenian_text': 'სომხური თარგმანი',
        'english_text': 'ინგლისური თარგმანი',
    }
