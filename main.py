from pytube import YouTube, Channel, request
from os import mkdir, path, startfile
from transliterate import translit


def open_explorer(dirPath):
    dirPath = path.realpath(dirPath)
    startfile(dirPath)


def create_dir(dirPath):
    if not path.exists(dirPath):
        mkdir(dirPath)
        print("Directory ", dirPath, " Created ")
    else:
        print("Directory ", dirPath, " already exists")

    return True


def download_info(channel):
    channel_info = {'to_download': len(channel), 'total_size': 0}
    for video in channel:
        video_size = channel_info.get('total_size') + request.filesize(video)
        channel_info.update({'total_size': video_size})
    print(f'{channel_info.get("to_download")} videos to download. '
          f'Total size {channel_info.get("total_size") / 1024} megabytes.')

    return channel_info


def download_video(stream, dirPath=None):
    if dirPath is None:
        stream.download()
    else:
        stream.download(dirPath)

    return True


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

    return True


def multiple_channels_download(urls, dirPath=None):
    total_channels = len(urls)
    iteration = 1
    for url in urls:
        channel = Channel(url)
        print(f'[{iteration}/{total_channels}] {channel.channel_name} is downloading...')
        download_channel(channel, dirPath)
        iteration += 1

    return True


def main():
    channel = Channel('https://www.youtube.com/channel/UCYx6EY5B3EDGLcIm8xPqvJw')
    dirPath = r'E:\YouTube Downloader'
    download_channel(channel, dirPath)
    open_explorer(dirPath)


if __name__ == '__main__':
    main()
