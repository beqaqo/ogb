from string import punctuation as default_punctuation
import unicodedata
from os import path
import re

from src import Config

def remove_punctuation(text, punctuation=None):
    if punctuation is None:
        translation_table = str.maketrans('', '', default_punctuation)
    else:
        translation_table = str.maketrans('', '', punctuation)

    unpunctuated_text = text.translate(translation_table)
    return unpunctuated_text

def remove_trailing_spaces(text):
    while '  ' in text:
        text = text.replace('  ', ' ')

    return text



def is_punctuation_token(text):
    text = text.strip()

    if not text:
        return True

    return all(unicodedata.category(ch).startswith("P") for ch in text)

def load_svg(name, width=None, height=None, css_class=None):
    if '..' in name or name.startswith('/'):
        raise ValueError("Directory traversal not allowed")

    svg_dir = path.join(Config.PROJECT_ROOT, 'static', 'img', name)
    if not path.isfile(svg_dir):
        raise FileNotFoundError(f"{name} not found")

    with open(svg_dir, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    attrs = ""
    if css_class: attrs += f' class="{css_class}"'
    if width: attrs += f' width="{width}"'
    if height: attrs += f' height="{height}"'

    if attrs:
        svg_content = re.sub(r'<svg\b', f'<svg{attrs}', svg_content, count=1)
    return svg_content


def make_word_matcher(q_word, q_lemma, q_translation, q_grammar):
    q_word, q_lemma = q_word.lower(), q_lemma.lower()
    q_translation, q_grammar = q_translation.lower(), q_grammar.lower()

    def contains(value, q):
        return bool(q and value and q in value.lower())

    def match(token, word):
        """token = the text as displayed, word = the Word row"""
        return (
            contains(token, q_word)
            or contains(word.lemma, q_lemma)
            or bool(q_grammar and word.grammar and word.grammar.lower().startswith(q_grammar))
            or any(contains(t, q_translation)
                for t in (word.greek_text, word.armenian_text, word.english_text))
        )

    return match
