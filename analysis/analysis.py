import pandas as pd
import numpy as np
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
    plt.figure()
    for character in CHARACTERS:
        character_df = line_count_df[line_count_df['character'] == character]
        x = character_df['season']
        y = character_df['percent_lines']
        plt.scatter(x, y, label=character.title())
        plt.plot(x, y, label='_nolegend_')
    plt.ylabel('Percent of Lines')
    plt.xlabel('Season')
    plt.legend()
    plt.title('Character usage over time', loc='left')
    plt.savefig('../plots/character_usage')
    return


def analyze_sentiment(df):
    sentiments = []
    sid = SentimentIntensityAnalyzer()
    for i in range(df.shape[0]):
        if i % 100 == 0:
            print(i)
        line = df['lines'].iloc[i]
        sentiment = sid.polarity_scores(line)
        sentiments.append([sentiment['neg'], sentiment['pos'],
                           sentiment['neu'], sentiment['compound']])
    df[['neg', 'pos', 'neu', 'compound']] = pd.DataFrame(sentiments)
    df['Negative'] = df['compound'] < -0.1
    df['Positive'] = df['compound'] > 0.1
    return df


def episode_negativity(df):
    line_count_df = df.groupby(['episode'], as_index=False)['lines'].count()
    negativity_count_df = df.groupby(['episode'], as_index=False)['Negative'].sum()
    merge_df = line_count_df.merge(negativity_count_df)
    merge_df['percent_neg'] = merge_df['Negative'] / line_count_df['lines']
    return merge_df


def character_episode_negativity(df):
    line_count_df = df.groupby(['season', 'character'], as_index=False)['lines'].count()
    negativity_count_df = df.groupby(['season', 'character'], as_index=False)['Negative'].sum()
    merge_df = line_count_df.merge(negativity_count_df)
    merge_df['percent_neg'] = merge_df['Negative'] / line_count_df['lines']
    return merge_df


def character_episode_positivity(df):
    line_count_df = df.groupby(['season', 'character'], as_index=False)['lines'].count()
    positivity_count_df = df.groupby(['season', 'character'], as_index=False)['Positive'].sum()
    merge_df = line_count_df.merge(positivity_count_df)
    merge_df['percent_neg'] = merge_df['Positive'] / line_count_df['lines']
    return merge_df


def plot_character_mood(df, character):
    plt.figure()
    mood_df = character_episode_positivity(df)
    character_df = mood_df[mood_df['character'] == character]
    x = character_df['season']
    y = character_df['percent_neg']
    plt.scatter(x, y, label=character.title())
    plt.plot(x, y, label='_nolegend_')
    plt.xlabel('Season')
    plt.ylabel('Percent of lines with positive sentiment')
    plt.title("{character}'s mood over time".format(character=character.title()),
              loc='left')
    plt.savefig("../plots/{character}_mood".format(character=character.lower()))


def plot_word_frequency(df, words, category):
    plt.figure()
    allwords = df['lines'].str.cat(sep=' ')
    allwords = allwords.split()
    allwords = [word.lower() for word in allwords]
    allwords = np.array(allwords)
    indices = []
    for word in words:
        new_indices = np.where(allwords == word)
        for index in new_indices[0]:
            indices.append(index)

    ax = sns.distplot(indices, rug=True, hist=False)
    plt.xlim(0, len(allwords))
    plt.ylabel("{category} word frequency".format(category=category))
    plt.xlabel("Time (words)")
    plt.title("{category} words over time".format(category=category),
              loc='left')
    plt.savefig("../plots/{category}_frequency".format(category=category))


if __name__ == '__main__':
    df = load_data()
    line_count_df = count_lines(df)
    plot_character_usage(line_count_df)
    sentiment_df = analyze_sentiment(df)
    negativity = episode_negativity(sentiment_df)
    plot_character_mood(sentiment_df, 'JERRY')
    wedding_words = ['marry', 'marriage', 'engagement', 'engage', 'wedding']
    plot_word_frequency(df, wedding_words, "Wedding")
