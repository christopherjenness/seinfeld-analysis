from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

CHARACTERS = ['JERRY', 'GEORGE', 'ELAINE', 'KRAMER']
SEASONS = {1: range(1, 6),
           2: range(6, 18),
           3: range(18, 41),
           4: range(41, 65),
           5: range(65, 87),
           6: range(87, 111),
           7: range(111, 135),
           8: range(135, 157),
           9: range(157, 181)}


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


def extract_episode_num(url):
    num = url.split('-')[1].split('.')[0]
    if 'and' in num:
        num = num.split('and')[0]
    return int(num)


def make_df(soup, character, episode):
    lines = extract_lines(soup, character)
    df = pd.DataFrame(lines, columns=['lines'])
    df['character'] = character
    df['episode'] = episode
    return df


def extract_seasons(episode, season_dict=SEASONS):
    for season in season_dict.keys():
        if episode in season_dict[season]:
            return season


if __name__ == '__main__':
    combined_df = pd.DataFrame()
    urls = make_urls()
    for url in urls:
        episode = extract_episode_num(url)
        print(episode)
        season = extract_seasons(episode)
        soup = scrape_script(url)
        for character in CHARACTERS:
            lines = extract_lines(soup, character)
            df = make_df(soup, character, episode)
            combined_df = combined_df.append(df)
    combined_df.to_csv('all_lines.csv')
