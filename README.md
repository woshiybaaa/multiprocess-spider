Python多进程网页爬虫
====
##功能

- 正则记录网址的标题，如果标题为空则也记录，标识为error
- 记录网站的HTTP状态
- 记录网页源代码中，是否包含有百家乐、太阳城这两个关键字
- 小功能：
  - 运行日志:进程开始和结束时间

##使用方法
- 文本保存名为`self`,其中网址一行一个，且不带http://
- `python m-spider.py p l`
  - p:进程数(根据机器性能调整，详见效率)
  - l:行数
  - 想要任务数为60，每个进程处理10行数据
  - `python m-spider.py 60 10`
  - 运行结果会保存为`*-result`(星号指匹配，这边为第N任务数)

##注意

- 需要安装python模块chardet

##效率

- 1核VPS(Vultr.com)，36个进程左右
- 2核VPS(directspace.net)，60进程左右。

##升级计划

- httplib2

##联系方式

[我的维基][likunyan]
*******************
[likunyan]:https://www.likunyan.com
