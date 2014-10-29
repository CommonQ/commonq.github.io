---
layout: post
title: 用Pelican和Github Pages在Linux上搭建个人博客
categories: [Blog]
---

### 搭建环境

在`Linux`环境下搭建，采用`ubuntu`，使用其它发行版过程基本相同。

### Github Pages

* 注册`Github`,注册和配置`SSH`密钥过程[help page](http://help.github.com/articles/set-up-git)写得很清楚。
* 不过现在github支持http传输良好，所以也可以不用配置ＳＳＨ，通过用户名密码即可登录。
* 在Github创建一个名为username.github.io的版本库（将username替换成自己的Github账户名）。
* Setting -> Automatic page generator -> Continue to layout，选择一个模板，并发布。

十分钟后在`username.github.io`页面就已经生成了一个页面。访问该网址即可看到。

###配置本地环境

####安装Ｐｅｌｉｃａｎ和Ｍａｒｋｄｏｗｎ：
在这里我没有用`Jekyll`因为它是`Ｒｕｂｙ`写的对它没什么兴趣。所以我采用`Ｐｙｔｈｏｎ`编写的`Ｐｅｌｉｃａｎ`。

####介绍
`Pelican`是一套开源的使用`Python`编写的博客静态生成, 可以添加文章和和创建页面, 可以使用`MarkDown` `reStructuredText` 和 `AsiiDoc` 的格式来抒写, 同时使用 `Disqus`评论系统, 支持 `RSS`和`Atom`输出, 插件, 主题, 代码高亮等功能, 采用`Jajin2`模板引擎, 可以很容易的更改模板
####安装

安装`Ｐｅｌｉｃａｎ`有很多种方法。一种使用`ｐｙｔｈｏｎ`的包管理器`ｐｉｐ`进行安装。
```sh
$sudo apt-get install python-pip
$sudo pip install pelican
$sudo pip install markdown

```

另一种就是从`ｇｉｔｈｕｂ`上克隆`Ｐｅｌｉｃａｎ`。
```sh
git clone git://github.com/getpelican/pelican.git       
cd pelican
python setup.py install

```

###写第一篇博客
####搭建目录
```sh
mkdir blog
cd blog
pelican-quickstart
```
在回答一系列问题过后你的博客就建成的, 主要生成下列文件:
生成的目录结构:

```sh
blog/
├── content
│   └── *.md             # markdown文件
├── output               # 默认的输出目录
├── develop_server.sh
├── Makefile
├── pelicanconf.py       # 主配置文件
└── publishconf.py
```




####写一篇文章
在 `content `目录新建一个 `test.md`文件, 填入一下内容:
```md
Title: 文章标题
Date: 2013-04-18
Category: 文章类别
Tag: 标签1, 标签2
这里是内容
```
然后执行
```sh
make html
```
生成了`ｈｔｍｌ`。然后执行

```sh
./develop_server.sh start
```

开启一个测试服务器, 这会在本地 8000 端口建立一个测试web服务器, 可以使用浏览器打开:`http://localhost:8000`来访问这个测试服务器, 然后就可以欣赏到你的博客了


####创建一个Ａｂｏｕｔ页面





这里以创建 About页面为例

在`content`目录创建pages目录

```sh
mkdir content/pages
```
然后创建`About.md`并填入下面内容
```md
Title: About Me
Date: 2013-04-18

About me content
```
执行 `make html` 生成`html`, 然后打开` http://localhost:8000`查看效果

###使用Ｐｅｌｉｃａｎ支持评论
使用[Disqus](http://disqus.com/)作为评论系统，注册帐号后直接在pelicanconf.conf中添加:
```python
DISQUS_SITENAME = your_shortname
```
然后执行
```sh
make html
```
使用浏览器打开:`http://localhost:8000`来查看效果
### 主题


安装主题：
Ｐｅｌｉｃａｎ本身提供很多主题可供选择，可以从`ｇｉｔｈｕｂ`上`ｃｌｏｎｅ`下来
```sh
git clone https://github.com/getpelican/pelican-themes.git
cd pelican-themes
pelican-themes -i bootstrap2
```
其中`bootstrap2`是选择使用的主题，[pelican主题的Github目录](http://github.com/getpelican/pelican-themes)下几乎每个都提供了预览.

然后，在配置文件`pelicanconf.py`中添加：
```python
THEME = u"bootstrap2'
```

重新make，就生成了带有选定主题的页面。

###使用插件

`Pelican` 一开始是将插件内置的, 但是新版本 `Pelican`将插件隔离了出来, 所以我们要到github上 克隆一份新的插件, 在博客目录执行

```sh
git clone git://github.com/getpelican/pelican-plugins.git    
```
现在我们博客目录就新添了一个 `pelican-plugins`目录, 我们已配置sitemap插件为例, sitemap插件可以生成 sitemap.xml 供搜索引擎使用

在`pelicanconf.py`配置文件里加上如下项:

```python
PLUGIN_PATH = u"pelican-plugins"

PLUGINS = ["sitemap"]
```
配置sitemap 插件
```python
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.7,
        "indexes": 0.5,
        "pages": 0.3,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    }
}
```
然后再执行
```sh
make html
```
打开浏览器请求 `http://localhost:8000/sitemap.xml`即可看到生成的 Sitemap 了

###添加Google Analytics
去Google Analytics申请账号，记下跟踪ID。 在pelicanconf.py添加
```python
GOOGLE_ANALYTICS = 跟踪ID
```
###使用Google Webmasters
在[Google Webmasters](http://www.google.com/webmasters/)上注册即可。
这个就是Google站长工具，使用它的目的是为了让博客被Google更好的收录，比如手动让Googlebot抓取、提交Robots、更新Sitemap等等，各方面完爆百度站长工具。
###上传Ｇｉｔｈｕｂ
最后在你的`ｏｕｔｐｕｔ`文件夹内
```sh
git init
git add .
git commit -m 'first commit' 
git remote add origin git@github.com:yourname/yourname.github.io.git
git push -u origin master
```
这样就大功告成了！


