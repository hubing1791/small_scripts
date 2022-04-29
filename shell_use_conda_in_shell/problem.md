**编写shell脚本调用**

在项目开发中，需要把一个python脚本融入进后端。这个脚本只能在特定的python版本和对应的包下才能跑对，记录一下学习过程.因为这个python脚本需要先激活环境才能跑，想到通过写一个shell来调用它，结果写入文件，php调shell读文件即可。

发现shell不能空行，会报not found 行号 得错误。进一步多次研究，发现需要在shell脚本里登录用户，因此得安装except和tcl

[参考文章链接](https://blog.csdn.net/shimadear/article/details/93972559)

命令记录一下

```shell
sudo ./configure
sudo make
sudo make install
sudo ./configure --with-tclinclude=/home/pengpai/pengyuan/tcl8.4.19/generic/ --with-tclconfig=/usr/local/lib/
sudo make
sudo make install
```

**继续改进方案**

最大的问题现在是，linux服务器划分了很细的权限，一个shell脚本必须先登录适当的用户。最终写出了下面这个版本的shell，注意一定别忘了写\r

``` shell
spawn su - 需要的用户名
expect "*密码*"
send "密码\r"
expect "*$*"
## 等待提示符出现
send "cd 需要的版本的环境目录\r"
expect "*$*"
send "./python 目标python和参数\r"
expect "*$*"
exit
```

**继续改进方案1.0**

上面的可行，但是从完成的代码的视角实在是不好看，主要是很多目录贼长，实际的代码可读性变得很差，并且是直接用环境对应的python进行运行的。此外还要让脚本从外界接收参数。

``` shell
set text [lindex $argv 0]  
## 获取参数
spawn su - 用户名
expect "*密码*"
send "密码\r"
## 登录有对应权限的用户
expect "*$*"
send "source ~/conda.sh\r"
expect "*$*"
send "conda activate py35\r"
## 激活环境
expect "*$*"
send "cd  脚本所在目录\r"
expect "*$*"
send "python extract_demo.py $text\r"
expect "*$*"
## 执行
exit
```

**写php**

写个php调shell，然后用php处理结果返回。任务完成。注意system会返回执行过程，因此用system调试很方便，最后再用exec。

**其他参考资料**

[linux expect spawn 的用法](https://www.cnblogs.com/jason2013/articles/4356352.html)

[使用expect脚本登录到root账号并执行命令](https://blog.csdn.net/vah101/article/details/6335242)

[php的system使用](https://blog.csdn.net/shj_php/article/details/103634567)

[访问控制FileMatch](https://blog.51cto.com/jacksoner/1980632)

[apache直接打开文件而不下载的问题](