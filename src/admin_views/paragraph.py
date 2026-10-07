from datetime import datetime

from flask_admin.model import InlineFormAdmin
from wtforms.fields import StringField

from src.admin_views.base import SecureModelView
from src.models import Note, Word

from src.utils import remove_punctuation, remove_trailing_spaces

class InlineNote(InlineFormAdmin):
    form_excluded_columns = ('date_created', 'date_modified')

class ParagraphView(SecureModelView):
    can_delete = True

    column_list = ("book", "chapter_number", "index", "text", "greek_text")
    column_searchable_list = ("text", "greek_text")

    form_columns = ("book", "index", "chapter_number", "text", "greek_text", "notes", "old_text")
    form_extra_fields = {"old_text": StringField("")}
    form_widget_args = {"old_text": {"style": "display: none"}}

    inline_models = [InlineNote(Note)]

    def on_form_prefill(self, form, id):
        form.old_text.data = form.text.data

    def on_model_change(self, form, model, is_created):
        model.date_modified = datetime.now()
        if form.text.data != form.old_text.data:
            for idx, raw_word in enumerate(model.text.split()):
                clean_word = remove_trailing_spaces(remove_punctuation(raw_word))
                new_word = Word(position=idx, text=clean_word)

                similar_word = (
                    Word.query.filter(
                        Word.text == clean_word,
                        Word.greek_text != None,
                        Word.english_text != None,
                        Word.armenian_text != None,
                        Word.lemma != None,
                        Word.grammar != None,
                    )
                    .order_by(Word.id.desc())
                    .first()
                )

                if similar_word:
                    new_word.greek_text = similar_word.greek_text
                    new_word.english_text = similar_word.english_text
                    new_word.armenian_text = similar_word.armenian_text
                    new_word.lemma = similar_word.lemma
                    new_word.grammar = similar_word.grammar

                model.words.append(new_word)
