#!/usr/bin/env python3
"""Find the sections of Rhizome's documentation that answer a question.

    search.py "Wie funktioniert Konsent?"            (German docs)
    search.py "How does a dot poll work?" --lang en
    search.py check

Fetches the docs site's search index – the live one, so the answer is as
current as the docs – ranks its sections against the question and prints the
best ones with their anchor URL, breadcrumb and text. German is the original;
the English docs are a translation of it.

`check` is the self-check: a known question in each language must bring up
the expected section among the first three.
"""

import argparse
import html
import json
import math
import re
import ssl
import sys
import urllib.error
import urllib.request

DOCS = 'https://docs.get-rhizome.app'
# The index is ~45 kB, and the site has taken over ten seconds to send it.
TIMEOUT = 90
CERTIFICATES = (
    'This Python has no CA certificates, so it trusts no HTTPS server. With '
    'Python from python.org on macOS, run "Install Certificates.command" in '
    'its folder under /Applications, or use /usr/bin/python3.'
)

# Words that carry no subject. Short words (< 3 letters) are dropped anyway.
STOPWORDS = frozenset(
    """
    wie was wer wann warum wo wozu welche welcher welches kann können könnte
    muss mus soll darf gibt geht funktioniert macht mache machen ich ein eine
    einen einem einer der die das den dem des und oder mit von für bei auf aus
    ist sind wird werden wurde sich nicht auch noch nur mein meine unser dass
    zum zur rhizome
    how what who when why where which can could does do doing work works the
    and for with from that this there are was were into about get use using
    my our you your
    """.split()
)


def fetch(lang: str) -> list[dict]:
    """The docs sections of one language, as the site's search index lists them.

    :param lang: ``de`` or ``en``.
    :return: The index's items: ``location``, ``title``, ``text``, ``path``.
    """
    url = f'{DOCS}/{lang}/search.json'
    with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
        return json.load(response)['items']


def plain(text: str) -> str:
    """The index's HTML as plain text.

    :param text: A section's text.
    :return: The text without markup, whitespace collapsed.
    """
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', text)).split())


def words(text: str) -> list[str]:
    """Lower-case words of a text, without markup.

    :param text: Plain text or the index's HTML.
    :return: The words, in order.
    """
    return re.findall(r'\w+', plain(text).lower())


def terms(question: str) -> list[str]:
    """The words of a question worth searching for.

    :param question: What the person asked.
    :return: Distinct terms, in order.
    """
    found = []
    for word in words(question):
        if len(word) >= 3 and word not in STOPWORDS and word not in found:
            found.append(word)
    return found


def hits(term: str, tokens: list[str]) -> int:
    """How often a term occurs in a section's words.

    A term of five letters or more matches inside a longer word, so
    „widerstand" finds „Widerstandsabfrage"; a shorter one only starts a
    word, so „tag" finds „Tags" and not „Kontakt". A long word matches a term
    that extends it, so „entscheidungen" finds „Entscheidung".

    :param term: One search term.
    :param tokens: The section's words.
    :return: The number of matching words.
    """
    return sum(
        1
        for token in tokens
        if (term in token if len(term) >= 5 else token.startswith(term))
        or (len(token) >= 5 and term.startswith(token))
    )


def rank(items: list[dict], question: str, limit: int) -> list[tuple[float, dict]]:
    """The sections that answer a question best, best first.

    A term scores in the section's title (weight 3), its breadcrumb (1) and
    its text (1, damped by length), weighted by how rare it is across the
    docs. A section matching more of the question's terms wins.

    :param items: The index's sections.
    :param question: What the person asked.
    :param limit: How many sections to return.
    :return: ``(score, section)`` pairs with a score above zero.
    """
    wanted = terms(question)
    sections = [
        (item, words(item['title']), words(' '.join(item['path'])), words(item['text']))
        for item in items
    ]
    rarity = {
        term: math.log(
            1
            + len(sections)
            / (
                1
                + sum(
                    1
                    for _, title, path, text in sections
                    if hits(term, title + path + text)
                )
            )
        )
        for term in wanted
    }
    scored = []
    for item, title, path, text in sections:
        score, matched = 0.0, 0
        for term in wanted:
            weight = (
                3 * hits(term, title) + hits(term, path) + math.log1p(hits(term, text))
            )
            if weight:
                matched += 1
                score += weight * rarity[term]
        if score:
            scored.append((score * matched, item))
    scored.sort(key=lambda pair: -pair[0])
    return scored[:limit]


def url(lang: str, item: dict) -> str:
    """The section's address on the docs site.

    :param lang: ``de`` or ``en``.
    :param item: A section from the index.
    :return: The page URL with the section's anchor.
    """
    return f"{DOCS}/{lang}/{item['location']}"


def show(lang: str, found: list[tuple[float, dict]], chars: int) -> None:
    """Print the sections found.

    :param lang: ``de`` or ``en``.
    :param found: ``(score, section)`` pairs, best first.
    :param chars: How much of each section's text to print.
    """
    if not found:
        print('No section matches.')
    for score, item in found:
        text = plain(item['text'])
        print(
            f"{url(lang, item)}\n  {' › '.join(item['path'])} › {item['title']}  ({score:.1f})"
        )
        if text:
            print(f"  {text[:chars]}{'…' if len(text) > chars else ''}")
        print()


# A question per language, and the page its answer must come from.
CHECKS = [
    ('de', 'Wie funktioniert Konsent?', 'funktionen/entscheidungsmodi/konsent/'),
    ('de', 'Wie archiviere ich ein Thema?', 'funktionen/konzepte/themen-und-status/'),
    ('en', 'How does a dot poll work?', 'features/decision-modes/dot-poll/'),
    ('en', 'What is a quorum?', 'reference/quorum/'),
]


def check() -> int:
    """Run every known question against the live docs.

    :return: The exit status: 0 if every expected page is among the first three.
    """
    failed = 0
    indexes = {lang: fetch(lang) for lang in {lang for lang, _, _ in CHECKS}}
    for lang, question, expected in CHECKS:
        top = [url(lang, item) for _, item in rank(indexes[lang], question, 3)]
        ok = any(f'/{lang}/{expected}' in link for link in top)
        failed += not ok
        print(
            f"{'ok  ' if ok else 'FAIL'} [{lang}] {question} → {top[0] if top else '–'}"
        )
    return 1 if failed else 0


def main() -> int:
    """Search, or run the self-check, and say so if the docs can't be read.

    :return: The exit status.
    """
    try:
        if sys.argv[1:] == ['check']:
            return check()
        return search()
    except (OSError, KeyError, ValueError) as error:
        # OSError covers URLError and timeouts; the others, an index in a new shape.
        if isinstance(error, urllib.error.URLError) and isinstance(
            error.reason, ssl.SSLCertVerificationError
        ):
            print(CERTIFICATES, file=sys.stderr)
        print(
            f'Could not read the docs search index at {DOCS}: {error!r}',
            file=sys.stderr,
        )
        return 2


def search() -> int:
    """Answer the question on the command line.

    :return: The exit status.
    """
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('question')
    parser.add_argument('--lang', choices=['de', 'en'], default='de')
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument(
        '--chars', type=int, default=1500, help='text printed per section'
    )
    args = parser.parse_args()
    if not terms(args.question):
        print('No search terms left: ask with the subject words, e.g. „Konsent“.')
        return 1
    show(args.lang, rank(fetch(args.lang), args.question, args.limit), args.chars)
    return 0


if __name__ == '__main__':
    sys.exit(main())
