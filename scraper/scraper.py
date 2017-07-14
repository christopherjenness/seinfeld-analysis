from urllib.request import urlopen
from bs4 import BeautifulSoup

CHARACTERS = ['JERRY', 'GEORGE', 'ELAINE', 'KRAMER']

def make_urls():
    baseurl = "http://www.seinology.com/scripts/script-"
    special_eps = [82, 83, 100, 101, 177, 178, 179, 180]
    urls = []
    for episode in range(1, 180):
        if episode not in special_eps:
            url = "{baseurl}{num}.shtml".format(baseurl=baseurl,
                                                num=str(episode).zfill(2))
            urls.append(url)
    special_urls = ['82and83', '100and101', '177and178', '179and180']
    for special_url in special_urls:
            url = "{baseurl}{num}.shtml".format(baseurl=baseurl,
                                                num=special_url)
            urls.append(url)
    return urls


def scrape_script(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup


def extract_lines(soup, character):
    lines = []
    for tag in soup.descendants:
        if tag.string and \
           "{character}:".format(character=character) in tag.string:
            raw_line = tag.string.strip()
            line = raw_line.lstrip("{character}:"
                                   .format(character=character)).strip()
            lines.append(line)
    return lines


def make_df(soup, character, episode):
    """IN PROGRESS"""
    lines = extract_lines()
    return


if __name__ == '__main__':
    urls = make_urls

