import requests


def DownloadVideoFromURL(url, savetofilepath):
    r = requests.get(url, allow_redirects=True)
    video_file_name = 'TweetVideo.mp4'
    open(savetofilepath+"/"+video_file_name, 'wb').write(r.content)
    return savetofilepath+"/"+video_file_name
