#!/usr/bin/env python3
"""Draw a mirror card or the decision canvas as ASCII art.

    render.py card 5 10 4 --lang en                      (one or more cards)
    render.py canvas canvas.json --lang de [--narrow]    (a file, - for stdin, or the JSON itself)
    render.py check

A canvas file names a title and, per field number 1–10, what is settled
and what is still open. A field left out renders as open:

    {"title": "Pilot 4-Tage-Woche Engineering",
     "fields": {"1": {"settled": ["…"], "open": ["…"]}, "5": {…}}}

`check` is the self-check: every card and both canvas layouts, in both
languages, must render with lines of equal display width.
"""

import argparse
import json
import os
import re
import sys
import unicodedata

CARDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cards.json')

SETTLED, OPEN = '✓', '○'
# What Rhizome asks with a control of its own; such a card becomes a hint.
CONTROLS = ('method', 'participation', 'experiment', 'conclusion')
ZWJ, VS16 = '‍', '️'

TEXT = {
    'de': {
        'heading': 'Entscheidungs-Canvas',
        'legend': f'{SETTLED} geklärt  {OPEN} offen',
        'groups': ['Wie?', 'Was?', 'Wer?'],
        'fields': {
            1: 'Thema',
            2: 'Vorschlag',
            3: 'Zusammenhänge',
            4: 'Werte und Ziele',
            5: 'Dringlichkeit',
            6: 'Modus',
            7: 'Funktion',
            8: 'Expert:innen',
            9: 'Betroffene und Umsetzende',
            10: 'Formale Struktur',
        },
    },
    'en': {
        'heading': 'Decision canvas',
        'legend': f'{SETTLED} settled  {OPEN} open',
        'groups': ['How?', 'What?', 'Who?'],
        'fields': {
            1: 'Topic',
            2: 'Proposal',
            3: 'Connections',
            4: 'Values and goals',
            5: 'Urgency',
            6: 'Mode',
            7: 'Function',
            8: 'Experts',
            9: 'Affected and implementers',
            10: 'Formal structure',
        },
    },
}

# Wie? | Was? (two columns) | Wer?  – a list inside a cell stacks its fields.
WIDE = [[[5, 6], [1], [2], [8, 9]], [[7], [3], [4], [10]]]
GROUPS = [[5, 6, 7], [1, 2, 3, 4], [8, 9, 10]]
WIDE_CW, NARROW_CW = 25, 40


def w(s):
    """Display width of a string in a terminal: wide characters and emoji count 2.

    ponytail: approximates grapheme clusters (ZWJ joins, VS16, skin tones);
    swap for the wcwidth package if a card ever misaligns.
    """
    n = prev = 0
    joined = False
    for c in s:
        if joined:
            joined = False
            continue
        if c == ZWJ:
            joined = True
            continue
        if c == VS16:
            n += 2 - prev if prev == 1 else 0
            prev = 2
            continue
        if unicodedata.combining(c) or 0x1F3FB <= ord(c) <= 0x1F3FF:
            continue
        prev = 2 if unicodedata.east_asian_width(c) in 'WF' else 1
        n += prev
    return n


def pad(s, n):
    return s + ' ' * (n - w(s))


def wrap(s, n):
    """Greedy word wrap by display width; a word longer than a line is cut."""
    lines = ['']
    for word in s.split():
        sep = ' ' if lines[-1] else ''
        if w(lines[-1] + sep + word) <= n:
            lines[-1] += sep + word
            continue
        if lines[-1]:
            lines.append('')
        for ch in word:
            if w(lines[-1] + ch) > n:
                lines.append('')
            lines[-1] += ch
    return lines


def load_cards():
    with open(CARDS, encoding='utf-8') as f:
        return {c['no']: c for c in json.load(f)}


def card(c, lang, width=31):
    """A card: number and emoji on top, title, question."""
    inner = width - 4
    t = c[lang]
    lines = [pad(f"{c['no']:>2}", inner - w(c['emoji'])) + c['emoji'], '']
    lines += wrap(t['title'].upper(), inner) + [''] + wrap(t['question'], inner)
    rule = '─' * (width - 2)
    return (
        ['╭' + rule + '╮']
        + ['│ ' + pad(line, inner) + ' │' for line in lines]
        + ['╰' + rule + '╯']
    )


def cell(no, field, lang, cw):
    """One canvas field: its number and name, then settled items before open ones."""
    num = f'({no}) '
    first, *rest = wrap(TEXT[lang]['fields'][no], cw - len(num))
    body = [num + first] + [' ' * len(num) + r for r in rest] + ['']
    items = [(SETTLED, t) for t in field.get('settled', [])] + [
        (OPEN, t) for t in field.get('open', [])
    ]
    for mark, text in items or [(OPEN, '–')]:
        first, *rest = wrap(text, cw - 2)
        body += [f'{mark} {first}'] + ['  ' + r for r in rest]
    return body


def table(grid, fields, lang, cw):
    """Rows of columns, each column one or more stacked fields, framed."""
    n = len(grid[0])

    def rule(left, mid, right):
        return left + mid.join('─' * (cw + 2) for _ in range(n)) + right

    out = [rule('╭', '┬', '╮')]
    for i, row in enumerate(grid):
        cols = []
        for nos in row:
            lines = []
            for k, no in enumerate(nos):
                lines += (['─' * cw] if k else []) + cell(
                    no, fields.get(str(no), {}), lang, cw
                )
            cols.append(lines)
        for j in range(max(len(c) for c in cols)):
            out.append(
                '│ '
                + ' │ '.join(pad(c[j] if j < len(c) else '', cw) for c in cols)
                + ' │'
            )
        out.append(rule('├', '┼', '┤') if i < len(grid) - 1 else rule('╰', '┴', '╯'))
    return out


def canvas(data, lang, narrow=False):
    """The decision canvas, about 113 columns wide, or one column on narrow screens."""
    t = TEXT[lang]
    fields = data.get('fields', {})
    cw = NARROW_CW if narrow else WIDE_CW
    width = cw + 4 if narrow else 4 * (cw + 3) + 1
    legend = t['legend']
    title = wrap(f"{t['heading']} · {data.get('title', '')}", width - w(legend) - 2)
    out = (
        [pad(title[0], width - w(legend)) + legend]
        + [pad(rest, width) for rest in title[1:]]
        + [pad('', width)]
    )
    if narrow:
        for head, nos in zip(t['groups'], GROUPS):
            out += [pad('  ' + head, width)] + table([[nos]], fields, lang, cw)
    else:
        heads = [t['groups'][0], t['groups'][1], '', t['groups'][2]]
        out += [''.join(pad('  ' + h, cw + 3) for h in heads) + ' '] + table(
            WIDE, fields, lang, cw
        )
    return out


EXAMPLE = {
    'title': 'Pilot 4-Tage-Woche Engineering',
    'fields': {
        '1': {
            'settled': [
                'Pilot: 32 h bei vollem Lohn im Engineering, 6 Monate.',
                'Anlass: Überlastung, Recruiting-Druck.',
            ]
        },
        '2': {
            'settled': ['Freitag frei, Rufbereitschaft rotiert.'],
            'open': ['Woran messen wir Erfolg?'],
        },
        '3': {
            'settled': ['ODR 12 „Kernarbeitszeit 10–15 Uhr" müsste abgelöst werden.']
        },
        '5': {'settled': ['Nicht akut, Start zum Quartal.']},
        '6': {'settled': ['Konsent, als Experiment.']},
        '8': {'open': ['Wer spürt kulturelle Folgen früh?']},
    },
}


def check():
    cards = load_cards()
    assert sorted(cards) == list(range(1, 51)), 'cards must be numbered 1–50'
    assert [n for n, c in cards.items() if c.get('control')] == [
        29, 37, 38, 44, 49
    ], 'control cards'
    assert [n for n, c in cards.items() if c.get('private')] == [
        9, 11, 12, 14, 33, 34, 35, 41
    ], 'private cards'
    assert cards[26]['de']['question'].startswith(
        'Wen sollte man beteiligen'
    ), 'card 26 carries the new question'
    with open(CARDS, encoding='utf-8') as f:
        raw = f.read()
    assert not re.search(
        r'phase|\b[EMVBK]\d{1,2}\b', raw, re.I
    ), 'no phase vocabulary or old codes'
    for no, c in cards.items():
        assert w(c['emoji']) == 2, f'card {no}: emoji must be two columns wide'
        assert c.get('field') in range(1, 11), f'card {no}: needs a canvas field 1–10'
        assert c.get('control') in (None, *CONTROLS), f'card {no}: unknown control'
        for lang in TEXT:
            assert (
                c[lang]['title'] and c[lang]['question']
            ), f'card {no}: {lang} text missing'
            lines = card(c, lang)
            assert (
                len({w(line) for line in lines}) == 1
            ), f'card {no} ({lang}) is ragged'
    wide_text = {
        'fields': {'9': {'open': ['会議室 👩‍💻 Rufbereitschaftsrotationsplanung']}}
    }
    for lang in TEXT:
        for narrow, data in [(False, EXAMPLE), (True, EXAMPLE), (False, wide_text)]:
            lines = canvas(data, lang, narrow)
            assert (
                len({w(line) for line in lines}) == 1
            ), f'canvas ({lang}, narrow={narrow}) is ragged'
        assert (
            110 <= w(canvas(EXAMPLE, lang)[0]) <= 120
        ), 'wide canvas is about 113 columns'
    print('ok: 50 cards and the canvas render with equal line widths in de and en')


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = p.add_subparsers(dest='cmd', required=True)
    pc = sub.add_parser('card')
    pc.add_argument('no', type=int, nargs='+')
    pc.add_argument('--lang', choices=TEXT, default='de')
    pv = sub.add_parser('canvas')
    pv.add_argument('source', help='a JSON file, - for stdin, or the JSON itself')
    pv.add_argument('--lang', choices=TEXT, default='de')
    pv.add_argument('--narrow', action='store_true')
    sub.add_parser('check')
    a = p.parse_args()

    if a.cmd == 'check':
        check()
    elif a.cmd == 'card':
        cards = load_cards()
        for no in a.no:
            if no not in cards:
                sys.exit(f'no card {no}: the deck runs from 1 to {len(cards)}')
        print('\n\n'.join('\n'.join(card(cards[no], a.lang)) for no in a.no))
    else:
        if a.source.lstrip().startswith('{'):
            data = json.loads(a.source)
        elif a.source == '-':
            data = json.load(sys.stdin)
        else:
            with open(a.source, encoding='utf-8') as f:
                data = json.load(f)
        print('\n'.join(canvas(data, a.lang, a.narrow)))


if __name__ == '__main__':
    main()
