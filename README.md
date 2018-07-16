amemv-crawler
===============

> 请在Python3下运行

这是一个[Python](https://www.python.org)的脚本,配置运行后可以下载指定抖音用户的全部视频(含收藏)，也可以下载指定主题(挑战)或音乐下的全部视频。

## 怎么样方便地讨论交流

* 直接在[Github](https://github.com/loadchange/amemv-crawler/issues/new)上开新的issue;

## 注意

大家好，这个项目是一个**练手项目**，源码仅作为和大家一起**学习Python**使用，你可以免费: 拷贝、分发和派生当前源码。你不可以用于*商业目的*及其他*恶意用途*。

另外本项目要完成的功能是将视频成功下载，有一些朋友在 **issue** 中提出了一些超预期的需求，比如视频改名、下载图片、视频宽高、发布数据和播放点赞等等，
这些完善可能是对项目十分有利的，但是我没有时间去一一处理，所以对于这样的需求请不要在发issue上来了，可以直接提 Pull requests 上来。

还有一些是对 *as*、 *cp* 、*mas* 的探讨，对于这些也不在我们的项目范围内，最后是服务端对抓取的一些限制，如抓取频率、IP等等，如果你遇到了这样的问题，
可能你的下载量已经超出了**学习目的**，对此我也拒绝支持并表示非常抱歉。

对于上述所不支持的问题以外，欢迎大家多提[issue](https://github.com/loadchange/amemv-crawler/issues/new)，同时也仅支持在 *issues* 中反馈问题，
使用 *email* 和我联系的同学，以后我就不在回复啦，私人邮箱很少登录，回复也不及时，哈哈。😄
最后希望和大家共同学习和进步。


## 环境安装

#### 程序猿和程序媛见这里


配置好你的Python、node环境,然后`pip install requests `.

或者

```bash
$ git clone https://github.com/loadchange/amemv-crawler.git
$ cd amemv-crawler
$ pip install -r requirements.txt
```

大功告成,直接跳到下一节配置和运行.

## 配置和运行

有两种方式来指定你要下载的抖音号分享链接,一是编辑`share-url.txt`,二是指定命令行参数.

### 第一种方法:编辑share-url.txt文件

找到一个文字编辑器,然后打开文件`share-url.txt`,把你想要下载的抖音号分享链接编辑进去,以逗号/空格/tab/表格鍵/回车符分隔,可以多行.例如, 这个文件看起来是这样的:

```
https://www.douyin.com/share/user/85860189461?share_type=link&tt_from=weixin&utm_source=weixin&utm_medium=aweme_ios&utm_campaign=client_share&uid=97193379950&did=30337873848,

https://www.iesdouyin.com/share/challenge/1593608573838339?utm_campaign=clien,

https://www.iesdouyin.com/share/music/6536362398318922509?utm_campaign=client_share&app=aweme&utm_medium=ios&iid=30337873848&utm_source=copy
```

### 获取用户分享链接的方法（挑战、音乐 类似）
<p align="center">
<img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/step1.jpg" width="160">
<img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/step2.jpg" width="160">
<img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/step3.png" width="160">
<img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/step4.png" width="160">
<img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/step5.jpg" width="160">
</p>

然后保存文件,双击运行`amemv-video-ripper.py`或者在终端(terminal)里面
运行`python amemv-video-ripper.py`

### 第二种方法:使用命令行参数(仅针对会使用操作系统终端的用户)

如果你对Windows或者Unix系统的命令行很熟悉,你可以通过指定运行时的命令行参数来指定要下载的站点:

某些平台下注意给URL增加引号

```bash
python amemv-video-ripper.py URL1,URL2
```

分享链接以逗号分隔,不要有空格.

### 视频的下载与保存

程序运行后,会默认在当前路径下面生成一个跟抖音ID名字相同的文件夹,
视频都会放在这个文件夹下面.

运行这个脚本,不会重复下载已经下载过的视频,所以不用担心重复下载的问题.同时,多次运行可以
帮你找回丢失的或者删除的视频.

然后重新运行下载命令.
<p align="center"><img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/end-of-run.jpg" width="800"></p>

## 高级应用

如果你想下载整个挑战主题，请在 share-url.txt 文件中添加 挑战的分享URL

如果你想下载按音乐去下载，请在 share-url.txt 文件中添加 音乐的分享URL

如下: 既为抖音号、挑战主题和音乐的三种爬虫方式，需要注意的是，爬虫只对搜索结果第一的结果进行下载，所以请尽量完整的写出你的 主题或音乐名称。

```
https://www.douyin.com/share/user/85860189461?share_type=link&tt_from=weixin&utm_source=weixin&utm_medium=aweme_ios&utm_campaign=client_share&uid=97193379950&did=30337873848,

https://www.iesdouyin.com/share/challenge/1593608573838339?utm_campaign=clien,

https://www.iesdouyin.com/share/music/6536362398318922509?utm_campaign=client_share&app=aweme&utm_medium=ios&iid=30337873848&utm_source=copy
```

> 短地址的情况

```
http://v.douyin.com/cDo2P/,

http://v.douyin.com/cFuAN/,

http://v.douyin.com/cMdjU/
```

### 处理意外

2018-04-14 用户列表接口新增字段_signature，该字段是由`douyin_falcon:node_modules/byted-acrawler/dist/runtime` 生成的，所以我们需要先`fuck byted-acrawler`一下，拿到signature，才能继续前行。请安装好python的环境之后 顺手安装node 以便顺利的`fuck byted-acrawler`

2018-06-22 分享出现短地址，解决办法：读取到 __v.douyin.com__ 的任务时，尝试请求，在302的情况下取Response Headers中Location。

2018-07-02 更新了 __douyin_falcon:node_modules/byted-acrawler/dist/runtime__，我们保持同步更新 __fuck-byted-acrawler.js__ !

2018-07-12 用户视频接口 __https://www.douyin.com/aweme/v1/aweme/post/__ 增加参数dytk, 这个参数在页面中直接取。

## 喜欢就打赏吧!

如果您喜欢这个项目, 那就打个赏支持一下作者吧! 非常感谢!

<p align="center"><img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/picture/award.jpg" width="550"></p>
