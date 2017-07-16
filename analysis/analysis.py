import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


nltk.download('vader_lexicon')
CHARACTERS = ['JERRY', 'ELAINE', 'KRAMER', 'GEORGE']

def load_data():
    df = pd.read_csv('../scraper/all_lines.csv')
    return df


def count_lines(df):
    line_count_df = df.groupby(['season', 'character'], as_index=False)['lines'].count()
    season_totals = line_count_df.groupby('season')['lines'].sum()
    line_count_df = line_count_df.merge(pd.DataFrame(season_totals), left_on='season', right_index=True)
    line_count_df.columns = ['season', 'character', 'lines',
                             'season_lines']
    line_count_df['percent_lines'] = line_count_df['lines'] / line_count_df['season_lines']
    return line_count_df

def plot_character_usage(line_count_df):
    for character in CHARACTERS:
        character_df = line_count_df[line_count_df['character'] == character]
        x = character_df['season']
        y = character_df['percent_lines']
        plt.scatter(x, y, label=character.title())
        plt.plot(x, y, label='_nolegend_')
    plt.ylabel('Percent of Lines')
    plt.xlabel('Character')
    plt.legend()
    plt.title('Character usage over time', loc='left')
    plt.show()

def analyze_sentiment(df):
    sentiments = []
    sid = SentimentIntensityAnalyzer()
    for i in range(df.shape[0]):
        if i % 100 == 0:
            print(i)
        line = df['lines'].iloc[i]
        sentiment = sid.polarity_scores(line)
        sentiments.append([sentiment['neg'], sentiment['pos'],
                           sentiment['neu']])
    df[['neg', 'pos', 'neu']] = pd.DataFrame(sentiments)
    return df

def episode_negativity(df):
    df.groupby('episode').sum()

df = load_data()
line_count_df = count_lines(df)
sentiment_df = analyze_sentiment(df)

df['Negative'] = df['neg'] > df['pos']
df['Positive'] = df['pos'] > df['neg']

positive_df = df[df['Positive'] == True]
negative_df = df[df['Negative'] == True]
positive_df.groupby('character').count()
negative_df.groupby('character').count()
