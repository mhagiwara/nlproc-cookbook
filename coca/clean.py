import sys
import re


def split_subtext(text):
    """Split chunk of text into subtext by structural markers e.g., <p> and @ @ ... @.

    Parameters:
        text (string): input text

    Returns:
        list of split subtext (string)
    """
    return re.split(r'(?:@ )+| ?<p> ?', text.rstrip())


def clean_text(text):
    """Remove special tokens e.g., '##223859' and '@!SANDER-VANOCUR' from text."""

    return re.sub(r'##[^ ]+ ?|@[^ ]+ ?', '', text)


def main():
    for line in sys.stdin:
        for subtext in split_subtext(line.rstrip()):
            subtext = clean_text(subtext).strip()
            if subtext:
                print subtext

if __name__ == '__main__':
    main()
