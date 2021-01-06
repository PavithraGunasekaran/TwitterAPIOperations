import pytest

from APITask1 import get_retweeters_list, get_retweet_count
from PostTweet import post_tweet
from Retweet import retweet
from Untweet import untweet
from DeleteTweet import delete_tweet


def APITask2():

    # Call the post_tweet method to post a tweet and get its tweet id
    tweet_id = post_tweet()

    # Retweet the tweet posted above by passing its tweet id
    retweet(tweet_id)

    # Get the retweeters id list and the count after retweet
    retweeters_list = get_retweeters_list(tweet_id)
    retweeters_count = get_retweet_count(tweet_id)
    print("After retweet ")
    print("Retweeters list : \n" + str(retweeters_list) + "\n" + "Retweeters count : \n" + str(retweeters_count) + "\n")

    # Untweet the tweet
    untweet(tweet_id)

    # Get the retweeters id list and teh count after untweet
    untweeters_list = get_retweeters_list(tweet_id)
    untweeters_count = get_retweet_count(tweet_id)
    print("After untweet ")
    print("Retweeters list : \n" + str(untweeters_list) + "\n" + "Retweeters count : \n" + str(untweeters_count) + "\n")

    # Delete the tweet
    delete_tweet(tweet_id)
    return retweeters_list, retweeters_count, untweeters_list, untweeters_count

# Tests if the retweet count is not zero after the retweet operation
def test_retweet_count():
    retweeters_list, retweeters_count,untweeters_list, untweeters_count = APITask2()
    assert retweeters_count > 0, "retweet count is 0"

# Tests if the retweeters list is not empty after the retweet operation
def test_retweeters_list():
    retweeters_list, retweeters_count,untweeters_list, untweeters_count = APITask2()
    assert len(retweeters_list) > 0, "no data in retweeters list"

# Tests if the retweet count is zero after the untweet operation
def test_untweet_count():
    retweeters_list, retweeters_count,untweeters_list, untweeters_count = APITask2()
    assert untweeters_count == 0, "untweet count is not 0"

# Tests if the retweeters list is empty after the untweet operation
def test_untweeters_list():
    retweeters_list, retweeters_count,untweeters_list, untweeters_count = APITask2()
    assert len(untweeters_list) == 0, "data present in untweeters list even after untweeting"



if __name__ == "__main__":
    APITask2()
