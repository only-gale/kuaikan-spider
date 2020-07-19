## 考题
在调研过程中，经常需要对一些网站进行定向抓取。由于python包含各种强大的库，使用python做定向抓取比较简单。请使用python开发一个迷你定向抓取器mini_spider.py，实现对种子链接的广度优先抓取，并把URL长相符合特定pattern的网页保存到磁盘上。

## 程序运行
```python
python mini_spider.py
```
## Dependencies

```python
pip3 install beautifulsoup4
pip3 install configparser
pip3 install retrying
```

## 配置文件spider.conf
```
[spider]
url_list_file: ./urls ; 种子文件路径
output_directory: ./output ; 抓取结果存储目录
max_depth: 1 ; 最大抓取深度(种子为0级)
crawl_interval: 1 ; 抓取间隔. 单位：秒
crawl_timeout: 1 ; 抓取超时. 单位：秒
target_url: .*\.(gif|png|jpg|bmp)$ ; 需要存储的目标网页URL pattern(正则表达式)
thread_count: 8 ; 抓取线程数
```

种子文件每行一条快看漫画链接，例如：
```
https://www.kuaikanmanhua.com/web/comic/7047/ 0
https://www.kuaikanmanhua.com/web/comic/278647/
```
链接后面（用至少一个空格隔开）可以跟一个可选数字，表示从当前话之后还需要扒多少话。
如果不写或者是非>=0的数字格式，则默认扒到最后一话。


## 参考库
### re(正则表达式)
- http://docs.python.org/2/library/re.html
- http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html
- http://blog.csdn.net/jgood/article/details/4277902

### gevent/threading(多线程)
- http://docs.python.org/2/library/threading.html
- http://www.cnblogs.com/huxi/archive/2010/06/26/1765808.html

### docopt/getopt/argparse(命令行参数处理)
- https://github.com/docopt/docopt
- http://docs.python.org/2/library/getopt.html
- http://andylin02.iteye.com/blog/845355
- http://docs.python.org/2/howto/argparse.html
- http://www.cnblogs.com/jianboqi/archive/2013/01/10/2854726.html

### ConfigParser(配置文件读取)
- http://docs.python.org/2/library/configparser.html
- http://blog.chinaunix.net/uid-25890465-id-3312861.html

### urllib/urllib2/httplib(网页下载)
- http://docs.python.org/2/library/urllib2.html
- http://blog.csdn.net/wklken/article/details/7364328
- http://www.nowamagic.net/academy/detail/1302872

### pyquery/beautifulsoup4/HTMLParser/SGMLParser(HTML解析)
- http://docs.python.org/2/library/htmlparser.html
- http://cloudaice.com/yong-pythonde-htmlparserfen-xi-htmlye-mian
- http://docs.python.org/2/library/sgmllib.html
- http://pako.iteye.com/blog/592009

### urlparse(URL解析处理)
- http://docs.python.org/2/library/urlparse.html
- http://blog.sina.com.cn/s/blog_5ff7f94f0100qr3c.html

### logging(日志处理)
- http://docs.python.org/2/library/logging.html
- http://kenby.iteye.com/blog/1162698
- http://my.oschina.net/leejun2005/blog/126713
