from pytube import YouTube, Channel, request
from os import mkdir, path, startfile
from transliterate import translit
from sys import argv
from re import match

url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

def open_explorer(dirPath):
    dirPath = path.realpath(dirPath)
    startfile(dirPath)


def create_dir(dirPath):
    if not path.exists(dirPath):
        mkdir(dirPath)
        print("Directory ", dirPath, " Created ")
    else:
        print("Directory ", dirPath, " already exists")


def download_info(channel):
    to_download: int = len(channel)
    total_size: int = 0
    for video in channel:
        total_size += request.filesize(video)
    print(f'{to_download} videos to download. Total size {total_size/1024} megabytes.')


def download_video(stream, dirPath=None):
    if dirPath is None:
        stream.download()
    else:
        stream.download(dirPath)


def download_channel(channel, dirPath=None):
    download_info(channel)
    if dirPath is not None:
        dirPath = f'{dirPath}\\{translit(channel.channel_name, language_code="ru", reversed=True)}'
        print(dirPath)
    create_dir(dirPath)
    total_videos = len(channel)
    iteration = 1
    for video in channel:
        video = YouTube(video)
        print(f'[{iteration}/{total_videos}] {video.title} is downloading...')
        stream = video.streams.get_by_itag(22)
        download_video(stream, dirPath)
        print(f'{video.title} downloaded')
        iteration += 1


def main(url):
    channel = Channel(url)
    dirPath = r'D:\YouTube Downloader'
    download_channel(channel, dirPath)
    open_explorer(dirPath)


if __name__ == '__main__':
    try:
        if match(url_regex, argv[1]):
            main(argv[1])
    except Exception:
        print("ERROR!!!")