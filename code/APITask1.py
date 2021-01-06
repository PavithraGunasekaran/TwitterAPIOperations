import time

import pytest
import requests
import os
from os import path
import json
import base64
import urllib
from DownloadVideo import DownloadVideoFromURL


# Function to get the encoded value of the consumer keys using RFC 1738.
# RFC 1738 encoding is done through urrlib.parse.quote()
def EncodeOAuthConsumer(oauth_parameters):
    encoded_oauth_consumer_parameters = urllib.parse.quote(oauth_parameters, safe='_')
    # print(encoded_oauth_consumer_parameters)
    return encoded_oauth_consumer_parameters


# Function to create the base64 encoded value of the RFC 1738 encoded consumer keys
def CreateBase64EncodedConsumerKeys(encoded_consumer_key, encoded_consumer_secret):
    encoded_consumer_key_secret = encoded_consumer_key + ":" + encoded_consumer_secret
    base64_consumer_key_secret = base64.b64encode(encoded_consumer_key_secret.encode("utf-8"))
    return base64_consumer_key_secret.decode()


# function to generate the Bearer token using the consumer keys
def GetBearerToken(oauth_consumer_key, oauth_consumer_secret):
    encoded_consumer_key = EncodeOAuthConsumer(oauth_consumer_key)
    encoded_consumer_secret = EncodeOAuthConsumer(oauth_consumer_secret)
    auth_string = CreateBase64EncodedConsumerKeys(encoded_consumer_key, encoded_consumer_secret)
    get_bearer_header = {
        "Accept": "*/*",
        "Connection": "close",
        "User-Agent": "My Twitter App v1.0.23",
        "Authorization": "Basic " + str(auth_string),
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": '176',
        "Host": "api.twitter.com",
        "Accept-Encoding": "gzip"
    }
    payload = "grant_type=client_credentials"
    get_bearer_request = requests.post('https://api.twitter.com/oauth2/token', headers=get_bearer_header, data=payload)

    res = json.loads(get_bearer_request.text)
    file = open('bearer.json', 'w')
    file.write(json.dumps(res, sort_keys=True, indent=4))
    bearer_token = res['access_token']
    base64_bearer_token = base64.b64encode(bearer_token.encode("utf-8"))
    # base64_bearer_token = base64_bearer_token.decode()
    # print("base64 bearer token : "+str(base64_bearer_token))
    return bearer_token


def GetAuthenticationHeader():
    oauth_consumer_key = ''  # Enter your consumer key
    oauth_consumer_secret = ''  # Enter your consumer secret

    # Authentication method used here is OAuth2.0 Bearer token where the authentication is made only through the consumer keys
    # The first step in this authentication is to obtain a bearer token with teh consumer keys
    bearer_token = GetBearerToken(oauth_consumer_key, oauth_consumer_secret)

    # Form a header string with the obtained bearer token to authenticate the user's API requests
    header_string = {
        "Accept": "*/*",
        "Connection": "close",
        "User-Agent": "My Twitter App v1.0.23",
        "Authorization": "Bearer " + str(bearer_token),
        "Content-Type": "application/json",
        "Host": "api.twitter.com",
        "Accept-Encoding": "gzip"
    }
    return header_string


# Function to get the tweet's text and download its video
def get_tweet_text_video(tweet_id):
    # Endpoint to get the contents of a tweet
    show_tweet_url = 'https://api.twitter.com/1.1/statuses/show.json?id=' + tweet_id + '&tweet_mode=extended'

    # Get Authentication header for API requests
    header_string = GetAuthenticationHeader()

    # Get tweet text and save to APITask1.txt
    r = requests.get(show_tweet_url, headers=header_string)
    show_tweet = json.loads(r.text)
    file = open('show_tweet.json', 'w')
    file.write(json.dumps(show_tweet, sort_keys=True, indent=4))
    tweet_text = show_tweet['full_text']
    file = open('APITask1.txt', 'w')
    file.write("Tweet content : \n")
    file.write(tweet_text)
    # print(tweet_text)
    file.write("\n")

    # Get the url of the video to be downloaded
    video_url = show_tweet['extended_entities']['media'][0]['video_info']['variants'][0]['url']

    # If there is a video associated with the tweet,
    #   then  download it
    #   else no action is performed
    if video_url:
        save_to_file_path = "C:/Users/91770/PycharmProjects/Twitter/TweetVideo"  # Enter the folder path where the video file has to be stored

        # if the folder path specified for storing video does not exists, then create a new folder
        if path.exists(save_to_file_path):
            pass
        else:
            os.mkdir("C:/Users/91770/PycharmProjects/Twitter/TweetVideo")
        video_file_path = DownloadVideoFromURL(video_url, save_to_file_path)

        # Get the last modified time of the video and the current time for further testing
        video_last_modified_time = time.ctime(os.path.getmtime(video_file_path))
        current_time = time.ctime()

    return tweet_text, video_last_modified_time, current_time

# Function to get the retweeters id list

def get_retweeters_list(tweet_id):

    # Endpoint to get the retweeters id list
    get_retweeters_id_url = ' https://api.twitter.com/1.1/statuses/retweeters/ids.json?id=' + tweet_id + '&count=100&cursor=2'

    # Get Authentication header for API requests
    header_string = GetAuthenticationHeader()

    # Get Retweeters ID
    r = requests.get(get_retweeters_id_url, headers=header_string)
    retweet_ids = json.loads(r.text)
    file = open('APITask1.txt', 'a+')
    file.write("Retweeter IDs \n" + str(retweet_ids['ids']))
    file.write("\n")
    retweeters_list = retweet_ids['ids']
    file.close()
    return retweeters_list


def get_retweet_count(tweet_id):

    # Endpoint to get the retweets of the tweet
    get_retweet_url = ' https://api.twitter.com/1.1/statuses/retweets/' + tweet_id + '.json'

    # Get Authentication header for API requests
    header_string = GetAuthenticationHeader()

    # Get Retweet count
    r = requests.get(get_retweet_url, headers=header_string)
    retweet_count = json.loads(r.text)
    file = open('APITask1.txt', 'a+')

    #Save the retweet count to the file if it is not zero else write the value zero
    if len(retweet_count) != 0:
        retweeters_count = retweet_count[0]['retweet_count']
        file.write("Retweeters count : \n" + str(retweeters_count))
        file.write("\n")
        file.close()
        # print(retweeters_count)
    else:
        retweeters_count = 0
        file.write("Retweeters count : \n" + str(retweeters_count))
        file.write("\n")
    return retweeters_count


# Tests if the tweet text extracted is valid by checking its length
def test_tweet_text():
    tweet_text, modified_time, current_time = get_tweet_text_video('1257326183101980673')
    assert len(tweet_text) > 0, "tweet content is empty"

# Tests if the retweet count is greater than zero
def test_retweet_count():
    assert get_retweet_count('1257326183101980673') > 0, "retweet count is 0"

# Tests if the retweeters id list is not empty
def test_retweeters_list():
    assert len(get_retweeters_list('1257326183101980673')) > 0, "no data in retweeters list"

# Tests if the tweet video is downloaded properly by comparing its modified time with teh current time
def test_tweet_video():
    tweet_text, modified_time, current_time = get_tweet_text_video('1257326183101980673')
    assert modified_time == current_time, "The video file is not downloaded"


if __name__ == "__main__":
    get_tweet_text_video('1257326183101980673')
    get_retweeters_list('1257326183101980673')
    get_retweet_count('1257326183101980673')
