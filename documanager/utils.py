# Utilities for documanager
import markdown2

def make_html(plain_text = None):
    if plain_text is None:
        raise ValueError("Please provide some text to convert")
    else:
        html = markdown2.markdown(plain_text, extras=["wiki-tables"])
        return html.lstrip()
        
