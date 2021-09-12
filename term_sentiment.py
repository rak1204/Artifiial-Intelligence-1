import sys
import re

def create_sent_dict(sentiment_file):

    scores = {}

    with open(sentiment_file) as f:
        
        for line in f:
            (term,score)= line.split("\t")
            scores[term] = int(score)
    
    return scores

def get_tweet_sentiment(tweet, sent_scores):
    """A function that find the sentiment of a tweet and outputs a sentiment score.

            Args:
                tweet (string): A clean tweet
                sent_scores (dictionary): The dictionary output by the method create_sent_dict

            Returns:
                score (numeric): The sentiment score of the tweet
        """
    score = 0

    words = tweet.split();

    list = []

    for ba in sent_scores.keys():
        if (re.search(r"\b" + re.escape(ba) + r"\b", tweet)):
            list.append(ba)

    list.sort(key=lambda x: len(x.split()), reverse=True)

    for wd in list:
        if (re.search(r"\b" + re.escape(wd) + r"\b", tweet)):
            tweet = tweet.replace(wd,'')
            score = score + int(sent_scores.get(wd))
    
    return score


def term_sentiment(sent_scores, tweets_file):
    """A function that creates a dictionary which contains terms as keys and their sentiment score as value

            Args:
                sent_scores (dictionary): A dictionary with terms and their scores (the output of create_sent_dict)
                tweets_file (string): The name of a txt file that contain the clean tweets
            Returns:
                dicitonary: A dictionary with schema d[new_term] = score
            """
    new_term_sent = {}
    
    tweets = open(tweets_file, 'r')
    for tweet in tweets:
        wds = tweet.split()
        score = get_tweet_sentiment(tweet, sent_scores)
        for wd in wds:
            if (wd not in sent_scores.keys()):
                if (wd not in new_term_sent.keys()):
                    new_term_sent[wd] = score/len(wds)
                
            elif (wd not in sent_scores.keys()):
                new_term_sent[wd] = new_term_sent[wd] + (score/len(wds))


    
    return new_term_sent


def main():
    sentiment_file = sys.argv[1]
    tweets_file = sys.argv[2]

    # Read the AFINN-111 data into a dictionary
    sent_scores = create_sent_dict(sentiment_file)

    # Derive the sentiment of new terms
    new_term_sent = term_sentiment(sent_scores, tweets_file)

    for term in new_term_sent:        
        print(term, new_term_sent[term])


if __name__ == '__main__':
    main()