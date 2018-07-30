# -*- coding: utf-8 -*-

import os
import sys, getopt

import hashlib
import codecs
import requests
import re
from six.moves import queue as Queue
from threading import Thread
import json

# Setting timeout
TIMEOUT = 10

# Retry times
RETRY = 5

# Numbers of downloading threads concurrently
THREADS = 10

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}

FAILED_FILE_MD5 = '6419a414275112dcc2e073f62a3ce91e'


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            medium_type, uri, download_url, target_folder = self.queue.get()
            self.download(medium_type, uri, download_url, target_folder)
            self.queue.task_done()

    def download(self, medium_type, uri, download_url, target_folder):
        if medium_type == 'image':
            self._download(uri, 'image', download_url, target_folder)
        elif medium_type == 'video':
            download_url = 'https://aweme.snssdk.com/aweme/v1/play/?{0}'
            download_params = {
                'video_id': uri,
                'line': '0',
                'ratio': '720p',
                'media_type': '4',
                'vr_type': '0',
                'test_cdn': 'None',
                'improve_bitrate': '0'
            }
            download_url = download_url.format(
                '&'.join(
                    [key + '=' + download_params[key] for key in download_params]
                )
            )
            self._download(uri, 'video', download_url, target_folder)
        elif medium_type == 'videowm':
            self._download(uri, 'video', download_url, target_folder)
            download_url = 'https://aweme.snssdk.com/aweme/v1/playwm/?video_id={0}&line=0'
            download_url = download_url.format(uri)
            res = requests.get(download_url, headers=HEADERS, allow_redirects=False)
            download_url = res.headers['Location']
            self._download(uri, 'video', download_url, target_folder)

    def _download(self, uri, medium_type, medium_url, target_folder):
        file_name = uri
        if medium_type == 'video':
            file_name += '.mp4'
        elif medium_type == 'image':
            file_name += '.jpg'
            file_name = file_name.replace("/", "-")
        else:
            return

        file_path = os.path.join(target_folder, file_name)
        if not os.path.isfile(file_path):
            print("Downloading %s from %s.\n" % (file_name, medium_url))
            retry_times = 0
            while retry_times < RETRY:
                try:
                    resp = requests.get(medium_url, headers=HEADERS, stream=True, timeout=TIMEOUT)
                    if resp.status_code == 403:
                        retry_times = RETRY
                        print("Access Denied when retrieve %s.\n" % medium_url)
                        raise Exception("Access Denied")
                    with open(file_path, 'wb') as fh:
                        for chunk in resp.iter_content(chunk_size=1024):
                            fh.write(chunk)
                    break
                except:
                    pass
                retry_times += 1
            else:
                try:
                    os.remove(file_path)
                except OSError:
                    pass
                print("Failed to retrieve %s from %s.\n" % medium_url)


class CrawlerScheduler(object):

    def __init__(self, items):
        self.numbers = []
        self.challenges = []
        self.musics = []
        for i in range(len(items)):
            url = self.getRealAddress(items[i])
            if not url: continue

            if re.search('share/user', url):
                user_id = re.findall('share/user/(\d+)', url)
                if not len(user_id): continue
                res = requests.get(url, headers=HEADERS)
                if not res: continue
                dytk = re.findall("dytk: '(.*)'", res.content.decode('utf-8'))
                if len(dytk):
                    dytk.insert(0, user_id[0])
                    self.numbers.append(dytk)

            if re.search('share/challenge', url):
                challenges_id = re.findall('share/challenge/(\d+)', url)
                if len(challenges_id): self.challenges.append(challenges_id[0])

            if re.search('share/music', url):
                musics_id = re.findall('share/music/(\d+)', url)
                if len(musics_id): self.musics.append(musics_id[0])

        self.queue = Queue.Queue()
        self.scheduling()

    # 短地址转长地址
    def getRealAddress(self, url):
        if url.find('v.douyin.com') < 0: return url
        res = requests.get(url, headers=HEADERS, allow_redirects=False)
        return res.headers['Location']

    def generateSignature(self, str):
        p = os.popen('node fuck-byted-acrawler.js %s' % str)
        return p.readlines()[0]

    def calculateFileMd5(self, filename):
        hmd5 = hashlib.md5()
        fp = open(filename, "rb")
        hmd5.update(fp.read())
        return hmd5.hexdigest()

    def checkFile(self, directory):
        current_folder = os.getcwd()
        targetDir = os.path.join(current_folder, 'download/%s' % directory)
        list = os.listdir(targetDir)
        failedUriList = []
        for i in range(0, len(list)):
            path = os.path.join(targetDir, list[i])
            if not os.path.isfile(path): break
            if self.calculateFileMd5(path) == FAILED_FILE_MD5:
                uri = re.findall(targetDir + '/(.*).mp4', path)
                if uri: failedUriList.append(uri[0])
                os.remove(path)
        if failedUriList:
            print(failedUriList)
            print('failed downloads: %d, The downgrade plan is ready to be downloaded!' % len(failedUriList))
            for uri in self.numbers:
                self.queue.put(('videowm', uri, None, targetDir))
            self.queue.join()
            print("\nFinish Downloading All the videos from %d\n\n" % len(failedUriList))

    def scheduling(self):
        for x in range(THREADS):
            worker = DownloadWorker(self.queue)
            worker.daemon = True
            worker.start()

        for params in self.numbers:
            self.download_videos(params)

        for challenge in self.challenges:
            self.download_challenge_videos(challenge)

        for music in self.musics:
            self.download_music_videos(music)

    def download_videos(self, params):
        if len(params) < 2: return
        number = params[0]
        dytk = params[1]
        video_count = self._download_user_media(number, dytk)
        self.queue.join()
        print("\nAweme number %s, video number %s\n\n" % (number, str(video_count)))
        print("\nFinish Downloading All the videos from %s\n\n" % number)
        self.checkFile(number)

    def download_challenge_videos(self, challenge):
        video_count = self._download_challenge_media(challenge)
        self.queue.join()
        print("\nAweme challenge #%s, video number %d\n\n" % (challenge, video_count))
        print("\nFinish Downloading All the videos from #%s\n\n" % challenge)
        self.checkFile('#' + challenge)

    def download_music_videos(self, music):
        video_count = self._download_music_media(music)
        self.queue.join()
        print("\nAweme music @%s, video number %d\n\n" % (music, video_count))
        print("\nFinish Downloading All the videos from @%s\n\n" % music)
        self.checkFile('@' + music)

    def _join_download_queue(self, aweme, target_folder):
        try:
            if aweme.get('video', None):
                self.queue.put(('video', aweme['video']['play_addr']['uri'], None, target_folder))
            else:
                if aweme.get('image_infos', None):
                    image = aweme['image_infos']['label_large']
                    self.queue.put(('image', image['uri'], image['url_list'][0], target_folder))

        except KeyError:
            return
        except UnicodeDecodeError:
            print("Cannot decode response data from DESC %s" % aweme['desc'])
            return

    def __download_favorite_media(self, user_id, dytk, signature, favorite_folder, video_count):
        if not os.path.exists(favorite_folder):
            os.makedirs(favorite_folder)
        favorite_video_url = "https://www.douyin.com/aweme/v1/aweme/favorite/?{0}"
        favorite_video_params = {
            'user_id': str(user_id),
            'count': '21',
            'max_cursor': '0',
            'aid': '1128',
            '_signature': signature,
            'dytk': dytk
        }
        max_cursor = None
        while True:
            if max_cursor:
                favorite_video_params['max_cursor'] = str(max_cursor)
            url = favorite_video_url.format(
                '&'.join([key + '=' + favorite_video_params[key] for key in favorite_video_params]))
            res = requests.get(url, headers=HEADERS)
            contentJson = json.loads(res.content.decode('utf-8'))
            favorite_list = contentJson.get('aweme_list', [])
            for aweme in favorite_list:
                video_count += 1
                self._join_download_queue(aweme, favorite_folder)
            if contentJson.get('has_more') == 1:
                max_cursor = contentJson.get('max_cursor')
            else:
                break
        return video_count

    def _download_user_media(self, user_id, dytk):
        current_folder = os.getcwd()
        target_folder = os.path.join(current_folder, 'download/%s' % user_id)
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)

        if not user_id:
            print("Number %s does not exist" % user_id)
            return

        signature = self.generateSignature(str(user_id))

        user_video_url = "https://www.douyin.com/aweme/v1/aweme/post/?{0}"
        user_video_params = {
            'user_id': str(user_id),
            'count': '21',
            'max_cursor': '0',
            'aid': '1128',
            '_signature': signature,
            'dytk': dytk
        }
        max_cursor, video_count = None, 0
        while True:
            if max_cursor:
                user_video_params['max_cursor'] = str(max_cursor)
            url = user_video_url.format('&'.join([key + '=' + user_video_params[key] for key in user_video_params]))
            res = requests.get(url, headers=HEADERS)
            print(url)
            print(res.content.decode('utf-8'))
            contentJson = json.loads(res.content.decode('utf-8'))
            aweme_list = contentJson.get('aweme_list', [])
            for aweme in aweme_list:
                video_count += 1
                self._join_download_queue(aweme, target_folder)
            if contentJson.get('has_more') == 1:
                max_cursor = contentJson.get('max_cursor')
            else:
                break
        if not noFavorite:
            favorite_folder = target_folder + '/favorite'
            video_count = self.__download_favorite_media(user_id, dytk, signature, favorite_folder, video_count)

        if video_count == 0:
            print("There's no video in number %s." % user_id)

        return video_count

    def _download_challenge_media(self, challenge_id):

        if not challenge_id:
            print("Challenge #%s does not exist" % challenge_id)
            return
        current_folder = os.getcwd()
        target_folder = os.path.join(current_folder, 'download/#%s' % challenge_id)
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)

        signature = self.generateSignature(str(challenge_id) + '9' + '0')

        challenge_video_url = "https://www.iesdouyin.com/aweme/v1/challenge/aweme/?{0}"
        challenge_video_params = {
            'ch_id': str(challenge_id),
            'count': '9',
            'cursor': '0',
            'aid': '1128',
            'screen_limit': '3',
            'download_click_limit': '3',
            '_signature': signature

        }

        cursor, video_count = None, 0
        while True:
            if cursor:
                challenge_video_params['cursor'] = str(cursor)
                challenge_video_params['_signature'] = self.generateSignature(str(challenge_id) + '9' + str(cursor))
            url = challenge_video_url.format(
                '&'.join([key + '=' + challenge_video_params[key] for key in challenge_video_params]))
            res = requests.get(url, headers=HEADERS)
            contentJson = json.loads(res.content.decode('utf-8'))
            aweme_list = contentJson.get('aweme_list', [])
            if not aweme_list:
                break
            for aweme in aweme_list:
                video_count += 1
                self._join_download_queue(aweme, target_folder)
            if contentJson.get('has_more') == 1:
                cursor = contentJson.get('cursor')
            else:
                break
        if video_count == 0:
            print("There's no video in challenge %s." % challenge_id)
        return video_count

    def _download_music_media(self, music_id):
        if not music_id:
            print("Challenge #%s does not exist" % music_id)
            return
        current_folder = os.getcwd()
        target_folder = os.path.join(current_folder, 'download/@%s' % music_id)
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)

        signature = self.generateSignature(str(music_id))
        music_video_url = "https://www.iesdouyin.com/aweme/v1/music/aweme/?{0}"
        music_video_params = {
            'music_id': str(music_id),
            'count': '9',
            'cursor': '0',
            'aid': '1128',
            'screen_limit': '3',
            'download_click_limit': '0',
            '_signature': signature
        }
        cursor, video_count = None, 0
        while True:
            if cursor:
                music_video_params['cursor'] = str(cursor)
                music_video_params['_signature'] = self.generateSignature(str(music_id) + '9' + str(cursor))

            url = music_video_url.format(
                '&'.join([key + '=' + music_video_params[key] for key in music_video_params]))
            res = requests.get(url, headers=HEADERS)
            contentJson = json.loads(res.content.decode('utf-8'))
            aweme_list = contentJson.get('aweme_list', [])
            if not aweme_list:
                break
            for aweme in aweme_list:
                video_count += 1
                self._join_download_queue(aweme, target_folder)
            if contentJson.get('has_more') == 1:
                cursor = contentJson.get('cursor')
            else:
                break
        if video_count == 0:
            print("There's no video in music %s." % music_id)
        return video_count


def usage():
    print("1. Please create file share-url.txt under this same directory.\n"
          "2. In share-url.txt, you can specify amemv share page url separated by "
          "comma/space/tab/CR. Accept multiple lines of text\n"
          "3. Save the file and retry.\n\n"
          "Sample File Content:\nurl1,url2\n\n"
          "Or use command line options:\n\n"
          "Sample:\npython amemv-video-ripper.py number1,number2\n\n\n")
    print(u"未找到share-url.txt文件，请创建.\n"
          u"请在文件中指定抖音分享页面URL，并以 逗号/空格/tab/表格鍵/回车符 分割，支持多行.\n"
          u"保存文件并重试.\n\n"
          u"例子: url1,url12\n\n"
          u"或者直接使用命令行参数指定站点\n"
          u"例子: python amemv-video-ripper.py url1,url2")


def parse_sites(fileName):
    with open(fileName, "rb") as f:
        txt = f.read().rstrip().lstrip()
        txt = codecs.decode(txt, 'utf-8')
        txt = txt.replace("\t", ",").replace("\r", ",").replace("\n", ",").replace(" ", ",")
        txt = txt.split(",")
    numbers = list()
    for raw_site in txt:
        site = raw_site.lstrip().rstrip()
        if site:
            numbers.append(site)
    return numbers


noFavorite = False

if __name__ == "__main__":
    content, opts, args = None, None, []

    try:
        if len(sys.argv) >= 2:
            opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["no-favorite"])
    except getopt.GetoptError as err:
        usage()
        sys.exit(2)

    if not args:
        # check the sites file
        filename = "share-url.txt"
        if os.path.exists(filename):
            content = parse_sites(filename)
        else:
            usage()
            sys.exit(1)
    else:
        content = (args[0] if args else '').split(",")

    if len(content) == 0 or content[0] == "":
        usage()
        sys.exit(1)

    if opts:
        for o, val in opts:
            if o in ("-nf", "--no-favorite"):
                noFavorite = True
                break

    CrawlerScheduler(content)
