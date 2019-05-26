amemv-crawler
===============

> Please run Python3

This is a [Python] script (https://www.python.org), which can be configured to download all video (including favorites) of the specified chatter user, or all video under the specified theme (challenge) or music.

## How to discuss and communicate conveniently

* Open a new issue directly on [Github](https://github.com/loadchange/amemv-crawler/issues/new);

## Warning

~~Hello, everyone, this project is a **hands-on project**, the source code is only used with you **to learn Python**, you can be free: copy, distribute and derive the current source code. You may not use it for *commercial purposes* or other *malicious purposes*.~~Thanks to [@Means88](https://github.com/Means88) ([#120](https://github.com/loadchange/amemv-crawler/issues/120))

In addition, the function to be completed in this project is to download video successfully. Some friends put forward some unexpected requirements in **issue**, such as the rename of video, download pictures, width and height of video, release data and play like, etc.
These improvements may be very beneficial to the project, but I don't have time to deal with them one by one, so please don't send issues for such requirements, and you can directly Pull requests.

There are also some discussions on *as*, *cp* and *mas*, which are not within the scope of our project. Finally, there are some restrictions on fetching on the server side, such as fetching frequency, IP and so on. If you encounter such problems,
You may have downloaded more than **for the purpose of** learning, for which I also refuse to support and I am very sorry.

For the above problems that do not support, welcome everybody to give [issue] (https://github.com/loadchange/amemv-crawler/issues/new), at the same time, it only supports in the *free* feedback problems,
If I use *email* to contact with my classmates, I will not reply to them in the future. Private email is rarely logged in, and the reply is not timely, haha. 😄
Finally, I hope to learn and progress together with you.


## Environmental installation

Configured your Python, node environment, then `pip3 install requests `.

or

```bash
$ git clone https://github.com/loadchange/amemv-crawler.git
$ cd amemv-crawler
$ pip install -r requirements.txt
```

Now that you're done, skip to the next section to configure and run.

## Configure and run

There are two ways to specify you share the link to download the trill, one is the editor `share - url.txt`, 2 it is to specify command line parameters.

### The first method: edit the share-url.txt file

Find a text editor, and then open the file `share-url.txt`, the number you want to download a trill to share links to edit inside, with a comma/space/TAB/form/return character space, can be multiple lines. For example, the file looks like this:

```
https://www.douyin.com/share/user/85860189461?share_type=link&tt_from=weixin&utm_source=weixin&utm_medium=aweme_ios&utm_campaign=client_share&uid=97193379950&did=30337873848,

https://www.iesdouyin.com/share/challenge/1593608573838339?utm_campaign=clien,

https://www.iesdouyin.com/share/music/6536362398318922509?utm_campaign=client_share&app=aweme&utm_medium=ios&iid=30337873848&utm_source=copy
```

### Ways to get users to share links (challenges, music similar)
<p align="center">
<img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/step1.jpg" width="160">
<img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/step2.jpg" width="160">
<img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/step3.png" width="160">
<img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/step4.png" width="160">
<img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/step5.jpg" width="160">
</p>

Then save the file, and then double-click to run `amemv-video-ripper.py` or inside the terminal (terminal)
Run `python amemv-video-ripper.py`

### The second approach: use command-line arguments (only for users who will use operating system terminals)

If you are familiar with the command line of Windows or Unix systems, you can specify the site to download by specifying the command-line parameters of the runtime:

Some platforms pay attention to adding quotes to urls

```bash
python amemv-video-ripper.py --url URL1,URL2
```

Share links separated by commas, without Spaces.

If the user URL does not download like list by default, it needs to be added `--favorite`

```bash
python amemv-video-ripper.py --url URL --favorite
```

### Video download and save

After the program runs, it will generate a folder with the same chattering ID name under the current path by default.
Video is going to be in this folder.

Running this script does not repeat downloading video that you have already downloaded, so you don't have to worry about repeating the download
To help you recover lost or deleted video.

Then rerun the download command.
<p align="center"><img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/end-of-run.jpg" width="800"></p>

## Advanced application

If you want to download the entire challenge topic, please add the challenge's share url in the share-url.txt file

If you want to download and press music to download, please add music's share url in the share-url.txt file

As follows: both for the shake signal, challenge theme and music crawler three ways, it needs to be noted that the crawler only search results for the first result to download, so please try to complete your theme or music name.

```
https://www.douyin.com/share/user/85860189461?share_type=link&tt_from=weixin&utm_source=weixin&utm_medium=aweme_ios&utm_campaign=client_share&uid=97193379950&did=30337873848,

https://www.iesdouyin.com/share/challenge/1593608573838339?utm_campaign=clien,

https://www.iesdouyin.com/share/music/6536362398318922509?utm_campaign=client_share&app=aweme&utm_medium=ios&iid=30337873848&utm_source=copy
```

> Short address case

```
http://v.douyin.com/cDo2P/,

http://v.douyin.com/cFuAN/,

http://v.douyin.com/cMdjU/
```

### Deal with accident

- 2018-04-14 list of users interface _signature new field, the field is a ` douyin_falcon: node_modules/byted - acrawler/dist/runtime ` generated, so we need to first ` fuck byted - acrawler `, get people like, can move on. Please install python environment Conveniently to install node in order to smoothly ` fuck byted - acrawler `

- 2018-06-22 short address appears in sharing. Solution: when __v.douyin.com__ is read, try to request and get the Location in Response Headers in case of 302.

- 2018-07-02 updated __douyin_falcon:node_modules/ byteds-acrawler /dist/runtime__, we keep updating __fux-byteds-acrawler.js__ synchronously!

- 2018-07-12 user video interface __https: / / www.douyin.com/aweme/v1/aweme/post/__ dytk increase parameter, this parameter directly in the page. Fixed user video list interface domain name __douyin. Com__ to __amemv.com__

- 2018-09-25 shake off the original watermark free 720P download address, temporarily downgraded to a watermark scheme

- 2018-10-01 resume watermark free download

- 2018-11-20 `Tik Tok` switch without watermark video source

If you like it, you can get a reward.

If you like this project, then give the author a reward to support it! Thank you very much!

<p align="center"><img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/award.jpg" width="366"></p>
