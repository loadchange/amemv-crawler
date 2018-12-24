# -*- coding: utf-8 -*-

import os
import sys, getopt

import urllib.parse
import urllib.request
import copy
import hashlib
import codecs
import requests
import re
from six.moves import queue as Queue
from threading import Thread
import json
import time

# Setting timeout
TIMEOUT = 10

# Retry times
RETRY = 5

# Numbers of downloading threads concurrently
THREADS = 10

HEADERS = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
}


def getRemoteFileSize(url, proxy=None):
    '''
    通过content-length头获取远程文件大小
    '''
    try:
        request = urllib.request.Request(url)
        request.get_method = lambda: 'HEAD'
        response = urllib.request.urlopen(request)
        response.read()
    except urllib.error.HTTPError as e:
        # 远程文件不存在
        print(e.code)
        print(e.read().decode("utf8"))
        return 0
    else:
        fileSize = dict(response.headers).get('Content-Length', 0)
        return int(fileSize)


def download(medium_type, uri, medium_url, target_folder):
    headers = copy.copy(HEADERS)
    file_name = uri
    if medium_type == 'video':
        file_name += '.mp4'
        headers['user-agent'] = 'Aweme/27014 CFNetwork/974.2.1 Darwin/18.0.0'
    elif medium_type == 'image':
        file_name += '.jpg'
        file_name = file_name.replace("/", "-")
    else:
        return

    file_path = os.path.join(target_folder, file_name)
    if os.path.isfile(file_path):
        remoteSize = getRemoteFileSize(medium_url)
        localSize = os.path.getsize(file_path)
        if remoteSize == localSize:
            return
    print("Downloading %s from %s.\n" % (file_name, medium_url))
    retry_times = 0
    while retry_times < RETRY:
        try:
            resp = requests.get(medium_url, headers=headers, stream=True, timeout=TIMEOUT)
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
    time.sleep(1)


def get_real_address(url):
    if url.find('v.douyin.com') < 0: return url
    res = requests.get(url, headers=HEADERS, allow_redirects=False)
    return res.headers['Location'] if res.status_code == 302 else None


def get_dytk(url):
    res = requests.get(url, headers=HEADERS)
    if not res: return None
    dytk = re.findall("dytk: '(.*)'", res.content.decode('utf-8'))
    if len(dytk): return dytk[0]
    return None


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            medium_type, uri, download_url, target_folder = self.queue.get()
            download(medium_type, uri, download_url, target_folder)
            self.queue.task_done()


class CrawlerScheduler(object):

    def __init__(self, items):
        self.numbers = []
        self.challenges = []
        self.musics = []
        for i in range(len(items)):
            url = get_real_address(items[i])
            if not url: continue
            if re.search('share/user', url): self.numbers.append(url)
            if re.search('share/challenge', url): self.challenges.append(url)
            if re.search('share/music', url): self.musics.append(url)

        self.queue = Queue.Queue()
        self.scheduling()

    @staticmethod
    def generateSignature(value):
        p = os.popen('node fuck-byted-acrawler.js %s' % value)
        return p.readlines()[0]

    @staticmethod
    def calculateFileMd5(filename):
        hmd5 = hashlib.md5()
        fp = open(filename, "rb")
        hmd5.update(fp.read())
        return hmd5.hexdigest()

    def scheduling(self):
        for x in range(THREADS):
            worker = DownloadWorker(self.queue)
            worker.daemon = True
            worker.start()

        for url in self.numbers: self.download_user_videos(url)
        for url in self.challenges: self.download_challenge_videos(url)
        for url in self.musics: self.download_music_videos(url)

    def download_user_videos(self, url):
        number = re.findall(r'share/user/(\d+)', url)
        if not len(number): return
        dytk = get_dytk(url)
        if not dytk: return
        user_id = number[0]
        video_count = self._download_user_media(user_id, dytk, url)
        self.queue.join()
        print("\nAweme number %s, video number %s\n\n" % (user_id, str(video_count)))
        print("\nFinish Downloading All the videos from %s\n\n" % user_id)

    def download_challenge_videos(self, url):
        challenge = re.findall('share/challenge/(\d+)', url)
        if not len(challenge): return
        challenges_id = challenge[0]
        video_count = self._download_challenge_media(challenges_id, url)
        self.queue.join()
        print("\nAweme challenge #%s, video number %d\n\n" % (challenges_id, video_count))
        print("\nFinish Downloading All the videos from #%s\n\n" % challenges_id)

    def download_music_videos(self, url):
        music = re.findall('share/music/(\d+)', url)
        if not len(music): return
        musics_id = music[0]
        video_count = self._download_music_media(musics_id, url)
        self.queue.join()
        print("\nAweme music @%s, video number %d\n\n" % (musics_id, video_count))
        print("\nFinish Downloading All the videos from @%s\n\n" % musics_id)

    def _join_download_queue(self, aweme, target_folder):
        try:
            if aweme.get('video', None):
                uri = aweme['video']['play_addr']['uri']
                download_url = "https://aweme.snssdk.com/aweme/v1/play/?{0}"
                download_params = {
                    'video_id': uri,
                    'line': '0',
                    'ratio': '720p',
                    'media_type': '4',
                    'vr_type': '0',
                    'test_cdn': 'None',
                    'improve_bitrate': '0',
                    'iid': '35628056608',
                    'device_id': '46166618999',
                    'os_api': '18',
                    'app_name': 'aweme',
                    'channel': 'App%20Store',
                    'idfa': '00000000-0000-0000-0000-000000000000',
                    'device_platform': 'iphone',
                    'build_number': '27014',
                    'vid': '2ED380A7-F09C-6C9E-90F5-862D58F3129C',
                    'openudid': '21dae85eeac1da35a69e2a0ffeaeef61c78a2e98',
                    'device_type': 'iPhone8%2C2',
                    'app_version': '2.7.0',
                    'version_code': '2.7.0',
                    'os_version': '12.0',
                    'screen_width': '1242',
                    'aid': '1128',
                    'ac': 'WIFI'
                }
                if aweme.get('hostname') == 't.tiktok.com':
                    download_url = 'http://api.tiktokv.com/aweme/v1/play/?{0}'
                    download_params = {
                        'video_id': uri,
                        'line': '0',
                        'ratio': '720p',
                        'media_type': '4',
                        'vr_type': '0',
                        'test_cdn': 'None',
                        'improve_bitrate': '0',
                        'version_code': '1.7.2',
                        'language': 'en',
                        'app_name': 'trill',
                        'vid': 'D7B3981F-DD46-45A1-A97E-428B90096C3E',
                        'app_version': '1.7.2',
                        'device_id': '6619780206485964289',
                        'channel': 'App Store',
                        'mcc_mnc': '',
                        'tz_offset': '28800'
                    }
                url = download_url.format('&'.join([key + '=' + download_params[key] for key in download_params]))
                self.queue.put(('video', uri, url, target_folder))
            else:
                if aweme.get('image_infos', None):
                    image = aweme['image_infos']['label_large']
                    self.queue.put(('image', image['uri'], image['url_list'][0], target_folder))

        except KeyError:
            return
        except UnicodeDecodeError:
            print("Cannot decode response data from DESC %s" % aweme['desc'])
            return

    def __download_favorite_media(self, user_id, dytk, hostname, signature, favorite_folder, video_count):
        if not os.path.exists(favorite_folder):
            os.makedirs(favorite_folder)
        favorite_video_url = "https://%s/aweme/v1/aweme/favorite/" % hostname
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
            res = requests.get(favorite_video_url, headers=HEADERS, params=favorite_video_params)
            contentJson = json.loads(res.content.decode('utf-8'))
            favorite_list = contentJson.get('aweme_list', [])
            for aweme in favorite_list:
                video_count += 1
                self._join_download_queue(aweme, favorite_folder)
            if contentJson.get('has_more'):
                max_cursor = contentJson.get('max_cursor')
            else:
                break
        return video_count

    def _download_user_media(self, user_id, dytk, url):
        current_folder = os.getcwd()
        target_folder = os.path.join(current_folder, 'download/%s' % user_id)
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)

        if not user_id:
            print("Number %s does not exist" % user_id)
            return
        hostname = urllib.parse.urlparse(url).hostname
        signature = self.generateSignature(str(user_id))
        user_video_url = "https://%s/aweme/v1/aweme/post/" % hostname
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
            res = requests.get(user_video_url, headers=HEADERS, params=user_video_params)
            contentJson = json.loads(res.content.decode('utf-8'))
            aweme_list = contentJson.get('aweme_list', [])
            for aweme in aweme_list:
                video_count += 1
                self._join_download_queue(aweme, target_folder)
            if contentJson.get('has_more'):
                max_cursor = contentJson.get('max_cursor')
            else:
                break
        if not noFavorite:
            favorite_folder = target_folder + '/favorite'
            video_count = self.__download_favorite_media(user_id, dytk, hostname, signature, favorite_folder,
                                                         video_count)

        if video_count == 0:
            print("There's no video in number %s." % user_id)

        return video_count

    def _download_challenge_media(self, challenge_id, url):

        if not challenge_id:
            print("Challenge #%s does not exist" % challenge_id)
            return
        current_folder = os.getcwd()
        target_folder = os.path.join(current_folder, 'download/#%s' % challenge_id)
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)

        hostname = urllib.parse.urlparse(url).hostname
        signature = self.generateSignature(str(challenge_id) + '9' + '0')

        challenge_video_url = "https://%s/aweme/v1/challenge/aweme/" % hostname
        challenge_video_params = {
            'ch_id': str(challenge_id),
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
                challenge_video_params['cursor'] = str(cursor)
                challenge_video_params['_signature'] = self.generateSignature(str(challenge_id) + '9' + str(cursor))
            res = requests.get(challenge_video_url, headers=HEADERS, params=challenge_video_params)
            try:
                contentJson = json.loads(res.content.decode('utf-8'))
            except:
                print(res.content)
            aweme_list = contentJson.get('aweme_list', [])
            if not aweme_list:
                break
            for aweme in aweme_list:
                aweme['hostname'] = hostname
                video_count += 1
                self._join_download_queue(aweme, target_folder)
                print("number: ", video_count)
            if contentJson.get('has_more'):
                cursor = contentJson.get('cursor')
            else:
                break
        if video_count == 0:
            print("There's no video in challenge %s." % challenge_id)
        return video_count

    def _download_music_media(self, music_id, url):
        if not music_id:
            print("Challenge #%s does not exist" % music_id)
            return
        current_folder = os.getcwd()
        target_folder = os.path.join(current_folder, 'download/@%s' % music_id)
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)

        hostname = urllib.parse.urlparse(url).hostname
        signature = self.generateSignature(str(music_id))
        music_video_url = "https://%s/aweme/v1/music/aweme/?{0}" % hostname
        music_video_params = {
            'music_id': str(music_id),
            'count': '9',
            'cursor': '0',
            'aid': '1128',
            'screen_limit': '3',
            'download_click_limit': '0',
            '_signature': signature
        }
        if hostname == 't.tiktok.com':
            for key in ['screen_limit', 'download_click_limit', '_signature']: music_video_params.pop(key)
            music_video_params['aid'] = '1180'

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
            if not aweme_list: break
            for aweme in aweme_list:
                aweme['hostname'] = hostname
                video_count += 1
                self._join_download_queue(aweme, target_folder)
            if contentJson.get('has_more'):
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
