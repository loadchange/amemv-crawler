amemv-crawler
===============

这是一个[Python](https://www.python.org)的脚本,配置运行后可以从某些你指定的tumblr博客
下载图片和视频.

## 怎么样方便地讨论交流

* 我们现在有了[Slack](https://amemv-crawler.slack.com), 欢迎大家加入, 讨论并解决问题.
* 或者直接在[Github](https://github.com/loadchange/amemv-crawler/issues/new)上开新的issue;

## 环境安装

#### 程序猿和程序媛见这里

配置好你的Python环境,然后`pip install requests `.

或者

```bash
$ git clone https://github.com/loadchange/amemv-crawler.git
$ cd amemv-crawler
$ pip install -r requirements.txt
```

大功告成,直接跳到下一节配置和运行.

#### 小白见这里

1. 首先你需要一个Python的环境,安装方法请
参照[这里](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001374738150500472fd5785c194ebea336061163a8a974000).

2. 安装`pip`(主要是希望通过`pip`来安装Python的一些依赖包)

    * 当然也可以通过其他方式来安装这些包(此处自行百度),推荐通过`pip`来安装依赖包;
    * 如果你是Windows用户,按照上面第一个步骤来安装的Python,那么请忽略这一步,
    因为已经安装过了; 如果忘记勾选,安装教程见[这里](http://www.tuicool.com/articles/eiM3Er3/)
    * Mac用户,请参照[这个教程](http://blog.csdn.net/fancylovejava/article/details/39140373)
    * 然后在终端(terminal)里面运行 `pip install xmltodict six "requests>=2.10.0" "PySocks>=1.5.6"`;


3. 下载[amemv-crawler](https://github.com/loadchange/amemv-crawler/archive/master.zip)并解压缩;


## 配置和运行

有两种方式来指定你要下载的抖音号,一是编辑`user-number.txt`,二是指定命令行参数.

### 第一种方法:编辑user-number.txt文件

找到一个文字编辑器,然后打开文件`user-number.txt`,把你想要下载的抖音号编辑进去,以逗号/空格/tab/表格鍵/回车符分隔,可以多行.例如,如果你要下载 _64075666_ and _9565982_,这个文件看起来是这样的:

```
64075666,9565982
```

然后保存文件,双击运行`amemv-video-ripper.py`或者在终端(terminal)里面
运行`python amemv-video-ripper.py`

### 第二种方法:使用命令行参数(仅针对会使用操作系统终端的用户)

如果你对Windows或者Unix系统的命令行很熟悉,你可以通过指定运行时的命令行参数来指定要下载的站点:

```bash
python amemv-video-ripper.py 抖音号1,抖音号2
```

站点的名字以逗号分隔,不要有空格.

### 视频的下载与保存

程序运行后,会默认在当前路径下面生成一个跟抖音号名字相同的文件夹,
视频都会放在这个文件夹下面.

运行这个脚本,不会重复下载已经下载过的视频,所以不用担心重复下载的问题.同时,多次运行可以
帮你找回丢失的或者删除的视频.

然后重新运行下载命令.

## 喜欢就打赏吧!

如果您喜欢这个项目, 那就打个赏支持一下作者吧! 非常感谢!

<p align="center"><img src="https://raw.githubusercontent.com/loadchange/amemv-crawler/master/award.jpg" width="250"></p>
