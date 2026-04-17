import ssl
import re
import urllib.request
from html.parser import HTMLParser

class MRGParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_mrg = False
        self.div_depth = 0
        self.skip_tag = False
        self.skip_depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.skip_tag = True
            self.skip_depth = 1
            return
        if self.skip_tag:
            self.skip_depth += 1
            return
        if tag == 'div' and not self.inside_mrg and attrs.get('class') == 'mrg':
            self.inside_mrg = True
            self.div_depth = 1
            return
        if self.inside_mrg:
            if tag == 'div':
                self.div_depth += 1
            if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'tr', 'li'):
                self.parts.append('\n')
            if tag == 'br':
                self.parts.append('\n')
            if tag == 'td':
                self.parts.append(' ')

    def handle_endtag(self, tag):
        if self.skip_tag:
            self.skip_depth -= 1
            if self.skip_depth == 0:
                self.skip_tag = False
            return
        if self.inside_mrg:
            if tag == 'div':
                self.div_depth -= 1
                if self.div_depth == 0:
                    self.inside_mrg = False
            if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'tr', 'li'):
                self.parts.append('\n')

    def handle_data(self, data):
        if self.inside_mrg and not self.skip_tag:
            self.parts.append(data.replace('\xa0', ' '))

    def get_text(self):
        text = ''.join(self.parts)
        text = re.sub(r'\r', '', text)
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()


def fetch_hexagram(code, ctx, headers):
    url = f'https://www.iching-online.com/hexagrams/iching-hexagram-{code}.html'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        html = resp.read().decode('iso-8859-1', errors='ignore')
    parser = MRGParser()
    parser.feed(html)
    text = parser.get_text()
    if not text:
        body = re.search(r'<body.*?>(.*)</body>', html, re.S | re.I)
        if body:
            cleaned = re.sub(r'<[^>]+>', '', body.group(1))
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            text = cleaned
    if text:
        text = re.split(r'\nThe 64 I Ching Hexagrams', text, maxsplit=1)[0].strip()
        text = re.split(
            r'(?m)^\s*Read more about the polarity of Yin and Yang here:\s*(?:\n|$)',
            text,
            maxsplit=1,
        )[0].strip()
        text = re.split(
            r'(?m)^\s*Compare to the Reversed Trigrams\b',
            text,
            maxsplit=1,
        )[0].strip()
    return text

if __name__ == '__main__':
    ctx = ssl._create_unverified_context()
    headers = {'User-Agent': 'Mozilla/5.0'}
    out_path = 'iching_hexagrams_texts.txt'
    with open(out_path, 'w', encoding='utf-8') as out_file:
        for i in range(64):
            code = format(i, '06b')
            try:
                text = fetch_hexagram(code, ctx, headers)
            except Exception as exc:
                text = f'ERROR fetching page: {exc}'
            out_file.write(f'{code}\n{text}\n\n')
            print(code, end=' ', flush=True)
    print('\nDone writing', out_path)
