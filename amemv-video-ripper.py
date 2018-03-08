# -*- coding: utf-8 -*-

import os
import sys

import requests
import time
from six.moves import queue as Queue
from threading import Thread
import json

# Setting timeout
TIMEOUT = 10

# Retry times
RETRY = 5

# Numbers of downloading threads concurrently
THREADS = 10


def _create_user_info_file(folder, user_info):
    txtName = folder + '/' + user_info.get('uid', 'user_info') + '.json'
    f = file(txtName, "a+")
    f.write(json.dumps(user_info, sort_keys=True, indent=2))
    f.close()


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            uri, download_url, target_folder = self.queue.get()
            self.download(uri, download_url, target_folder)
            self.queue.task_done()

    def download(self, uri, download_url, target_folder):
        try:
            if download_url is not None:
                self._download(uri, download_url, target_folder)
        except TypeError:
            pass

    def _download(self, uri, download_url, target_folder):
        file_name = uri + '.mp4'
        file_path = os.path.join(target_folder, file_name)
        if not os.path.isfile(file_path):
            print("Downloading %s from %s.\n" % (file_name, download_url))
            retry_times = 0
            while retry_times < RETRY:
                try:
                    resp = requests.get(download_url, stream=True, timeout=TIMEOUT)
                    if resp.status_code == 403:
                        retry_times = RETRY
                        print("Access Denied when retrieve %s.\n" % download_url)
                        raise Exception("Access Denied")
                    with open(file_path, 'wb') as fh:
                        for chunk in resp.iter_content(chunk_size=1024):
                            fh.write(chunk)
                    break
                except:
                    # try again
                    pass
                retry_times += 1
            else:
                try:
                    os.remove(file_path)
                except OSError:
                    pass
                print("Failed to retrieve %s from %s.\n" % download_url)


class CrawlerScheduler(object):

    def __init__(self, numbers):
        self.numbers = numbers
        self.queue = Queue.Queue()
        self.scheduling()

    def scheduling(self):
        # create workers
        for x in range(THREADS):
            worker = DownloadWorker(self.queue)
            # Setting daemon to True will let the main thread exit
            # even though the workers are blocking
            worker.daemon = True
            worker.start()

        for number in self.numbers:
            self.download_videos(number)

    def download_videos(self, number):
        self._download_media(number)
        # wait for the queue to finish processing all the tasks from one
        # single site
        self.queue.join()
        print("Finish Downloading All the videos from %s" % number)

    def _download_media(self, number):
        current_folder = os.getcwd()
        target_folder = os.path.join(current_folder, 'download/%s' % number)
        print target_folder
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)
        base_url = "https://api.amemv.com/aweme/v1/discover/search/?{0}"
        params = {
            'iid': '26666102238',
            'device_id': '46166717995',
            'os_api': '18',
            'app_name': 'aweme',
            'channel': 'App%20Store',
            'idfa': '00000000-0000-0000-0000-000000000000',
            'device_platform': 'iphone',
            'build_number': '17409',
            'vid': '2ED370A7-F09C-4C9E-90F5-872D57F3127C',
            'openudid': '20dae85eeac1da35a69e2a0ffeaeef41c78a2e97',
            'device_type': 'iPhone8,2',
            'app_version': '1.7.4',
            'version_code': '1.7.4',
            'os_version': '11.2.6',
            'screen_width': '1242',
            'aid': '1128',
            'ac': 'WIFI',
            'count': '20',
            'cursor': '0',
            'keyword': number,
            'search_source': 'discover',
            'type': '1',
            'mas': '00c535afeea60d0368d1a71368a2e4fc43dfb7fb4db8dc52b104ee',
            'as': 'a1c5a90a2959ba94808053',
            'ts': str(int(time.time()))
        }

        while True:
            user_search_url = base_url.format('&'.join([key + '=' + params[key] for key in params]))
            response = requests.get(user_search_url)

            results = json.loads(response.content.decode('utf-8'))
            user_list = results.get('user_list', [])
            if len(user_list) == 0:
                print("Number %s does not exist" % number)
                break
            user_info = user_list[0]['user_info']
            _create_user_info_file(target_folder, user_info)

            user_video_url = "https://www.douyin.com/aweme/v1/aweme/post/?{0}"
            user_video_params = {
                'user_id': str(user_info.get('uid')),
                'count': '21',
                'max_cursor': '0',
                'aid': '1128'
            }
            user_video_url = user_video_url.format('&'.join([key + '=' + user_video_params[key] for key in user_video_params]))
            response = requests.get(user_video_url)
            results = json.loads(response.content.decode('utf-8'))
            aweme_list = results.get('aweme_list', [])
            if len(aweme_list) == 0:
                print("There's no video in number %s." % number)
                break
            try:
                for post in aweme_list:
                    uri = post['video']['play_addr']['uri']
                    download_url = post['video']['play_addr']['url_list'][0]
                    self.queue.put((uri, download_url, target_folder))
                break
            except KeyError:
                break
            except UnicodeDecodeError:
                print("Cannot decode response data from URL %s" % user_video_url)
                continue


def usage():
    print("1. Please create file user-number under this same directory.\n"
          "2. In user-number.txt, you can specify amemv number separated by "
          "comma/space/tab/CR. Accept multiple lines of text\n"
          "3. Save the file and retry.\n\n"
          "Sample File Content:\nnumber1,number2\n\n"
          "Or use command line options:\n\n"
          "Sample:\npython amemv-video-ripper.py number1,number2\n\n\n")
    print(u"未找到user-number.txt文件，请创建.\n"
          u"请在文件中指定抖音号，并以 逗号/空格/tab/表格鍵/回车符 分割，支持多行.\n"
          u"保存文件并重试.\n\n"
          u"例子: 抖音号1,抖音号2\n\n"
          u"或者直接使用命令行参数指定站点\n"
          u"例子: python amemv-video-ripper.py 抖音号1,抖音号2")


def parse_sites(fileName):
    with open(fileName, "r") as f:
        raw_sites = f.read().rstrip().lstrip()

    raw_sites = raw_sites.replace("\t", ",") \
        .replace("\r", ",") \
        .replace("\n", ",") \
        .replace(" ", ",")
    raw_sites = raw_sites.split(",")

    numbers = list()
    for raw_site in raw_sites:
        site = raw_site.lstrip().rstrip()
        if site:
            numbers.append(site)
    return numbers


if __name__ == "__main__":
    numbers = None

    if len(sys.argv) < 2:
        # check the sites file
        filename = "user-number.txt"
        if os.path.exists(filename):
            numbers = parse_sites(filename)
        else:
            usage()
            sys.exit(1)
    else:
        numbers = sys.argv[1].split(",")

    if len(numbers) == 0 or numbers[0] == "":
        usage()
        sys.exit(1)
    CrawlerScheduler(numbers)
