+++
title = "git使用总结"
date = "2010-05-18T13:47:08+02:00"
tags = ["git", "开源"]
categories = ["programming"]
banner = "/images/banners/banner-2.jpg"
draft = false
author = "helight"
authorlink = "https://helight.cn"
summary = "git使用总结"
keywords = ["git", "nm", "开源", "linux"]
+++

# git使用总结

作者：<a href="mailto:zhwenxu@gmail.com">许振文</a>
## Git 介绍
最近的小项目想使用git来管理，应为git可以不需要服务器而在任意的Linux机器上管理代码，相对svn和cvs还是有它的优势的，所以我选用了git来管理我的小项目，以后在提供svn的管理。

在使用了一段时间后想写一点总结，可能也是和网络上其其它的git的文章差不多。但是作为我的使用总结还是很有必要的。

git安lixnus的解释是－－The stupid content tracker, 傻瓜内容跟踪器。呵呵！其实一点也不傻了，相当的智能化，也许应该这样说是”content tracker for stupid guy”,呵呵！

git的管理是在本地建立存储仓库，代码的所有变化的记录都在本地存储。也就是代码和管理仓库是形影不理的。不想svn分为客户端和服务器端。客户端只有一些简单的仓库信息，而真正的代码和代码的变化信息全都在服务器上保存。客户端一般只能得到代码文件（只是一般情况，如果非要得到当然也还是可以的）。所以git的这种方式可以减轻服务器的负担－－不用担心服务器坏了或是连接不到怎么办。

## git的配置
所以首先我应当先说git的配置：

Git命令的使用，一般有两种两种形式，一种是git后面带参数(如：git add），另一种是直接减号连接的一条命令（如：git-add），后面讲解全部使用后者，这样可以避免空格的使用带来的问题。
``` sh
helight@helight:~/mywork/zhwen.org$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/helight/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/helight/.ssh/id_rsa.
Your public key has been saved in /home/helight/.ssh/id_rsa.pub.
The key fingerprint is:
e0:4a:ba:d9:ba:b9:7a:0a:e4:aa:86:6c:a7:d8:85:c0 helight@helight
The key's randomart image is:
+--[ RSA 2048]----+
|                 |
|                 |
|      .          |
|.    . .         |
|.E  . . S        |
|o. + .           |
|+.o o            |
|==.B             |
|X=@+.            |
+-----------------+
helight@helight:~/mywork/zhwen.org$ vim /home/helight/.ssh/
id_rsa       id_rsa.pub   known_hosts

```
生成密钥，用户通信加解密。如果接受默认设置，那么生成2048bits RAS的密钥，私钥和公钥文件分别位于：~/.ssh/id_rsa和~/.ssh/id_rsa.pub。用户需要向服务器管理员提供公钥(id_rsa.pub)，在用户同步版本库时对用户进行身份认证。用户必须妥善保管私钥。
``` sh
helight@helight:~/kernel-mod/hello$ git-config user.name Zhwen Xu
helight@helight:~/kernel-mod/hello$ git-config user.email Helight.Xu@gmail.com
```
配置用户名，在生成补丁、日志时使用。git-config命令带--global选项是对所有用户信息进行配置，默认只针对对当前用户。
git-config中写入配置信息。 如果git-config加了--global选项，配置信息就会写入到~/.gitconfig文件中。 因为你可能用不同的身份参与不同的项目，而多个项目都用git管理，所以建议不用global配置。

用户可以通过git-config的其他选项来对git做其他配置，--list可以查看用户已经选项。如：
``` sh
helight@helight:~/kernel-mod/hello$ git-config --list
user.name=Zhwen Xu
user.email=Helight.Xu@gmail.com
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
helight@helight:~/kernel-mod/hello$
```
## git的使用

命令：git-init-db
在我们要管理的目录中执行这条命令即可建立相关的git数据库文件。
我们首先以一个小例子来说，如下在hello这个文件夹中有两个文件，一个c程序和一个Makefile文件。
``` sh
helight@helight:~/kernel-mod/hello$ ls -a
.  ..  hello.c  Makefile
helight@helight:~/kernel-mod/hello$
```
接着执行上面所说的命令：
``` sh
helight@helight:~/kernel-mod/hello$ git-init-db
Initialized empty Git repository in /home/helight/kernel-mod/hello/.git/
helight@helight:~/kernel-mod/hello$ ls -a
.  ..  .git  hello.c  Makefile
helight@helight:~/kernel-mod/hello$
```
执行完上面的命令之后用“ls －a”来看，就会发现多了一个“.git”的文件，这个文件就是hello个小项目的git仓库。关于这个仓库有兴趣的读者可以进入该文件夹继续分析。
接下来介绍如何将项目中的文件添加到仓库中，让git来作版本管理。将文件添加到git仓库中的命令是git-add,当然这并不是真的将文件copy到git的仓库文件夹中。只是在仓库中标识它，以示要用它git来管理它了。具体操作如下：
``` sh
helight@helight:~/kernel-mod/hello$ git-add hello.c
helight@helight:~/kernel-mod/hello$ git-add *
helight@helight:~/kernel-mod/hello$
```
可以看到添加可以是单个文件添加，也可以是多个文件一起添加。接下来是提交和项目状态的查看。相信有了前面的一点说明大家对git的管理也多少有点感觉了吧！

### 项目的提交和状态查看：
命令：git-commit, git-status
``` sh
helight@helight:~/kernel-mod/hello$ git-status
# On branch master
#
# Initial commit
#
# Changes to be committed:
#   (use "git rm --cached <file>..." to unstage)
#
#       new file: Makefile
#       new file: hello.c
#
helight@helight:~/kernel-mod/hello$ git-commit -m "init the project" ./*
Created initial commit f4808f0: init the project
 2 files changed, 27 insertions(+), 0 deletions(-)
 create mode 100644 Makefile
 create mode 100644 hello.c
helight@helight:~/kernel-mod/hello$ git-status
# On branch master
nothing to commit (working directory clean)
helight@helight:~/kernel-mod/hello$
```
第一个“git-status”的提示信息告诉我们版本库中加入了两个新的文件（这是和上一个版本的变化），并且 git 提示我们提交这些文件，我们可以通过 git-commit 命令来提交。提交后再次使用就会提示没有变化需要提交了。

### 分支管理：git主要提倡的一种管理方式就是分支管理，所以这应该是每一个学习git的人应该掌握的。
分支查看，分支建立和分支切换：
``` sh
helight@helight:~/kernel-mod/hello$ git-branch
* master
helight@helight:~/kernel-mod/hello$ git-branch helight
helight@helight:~/kernel-mod/hello$ git-branch
  helight
* master
helight@helight:~/kernel-mod/hello$ git-checkout helight
Switched to branch "helight"
helight@helight:~/kernel-mod/hello$ git-branch
* helight
  master
helight@helight:~/kernel-mod/hello$
```
可以看出“git-branch”是查看分支情况和创建分支，”git-checkout”个用来切换分支。其中“＊”表示当前工作的分支。

### 删除分支：git-branch -D xxx
``` sh
helight@helight:~/kernel-mod/hello$ git-branch xux
helight@helight:~/kernel-mod/hello$ git-branch
* helight
  master
  xux
helight@helight:~/kernel-mod/hello$ git-branch -D xux
Deleted branch xux.
helight@helight:~/kernel-mod/hello$ git-branch
* helight
  master
helight@helight:~/kernel-mod/hello$
```

### 分支差异查看：git-show-branch，git-diff，git-whatchanged
我们对文件修改一下后在查看。
``` sh
helight@helight:~/kernel-mod/hello$ git-show-branch
* [helight] init the project
 ! [master] init the project
--
*+ [helight] init the project
```

### git-diff:上次提交到现在的变化差异
``` sh
helight@helight:~/kernel-mod/hello$ git-diff
diff --git a/hello.c b/hello.c
index 843a6b8..c762de7 100644
--- a/hello.c
+++ b/hello.c
@@ -14,6 +14,7 @@ static int __init hello_init(void)
 static void __exit hello_exit(void)
 {
        printk("kernel: %s\n","Bey world!");
+       printk("kernel: %s\n","Bey world!");
 }

 module_init(hello_init);
```

### git-commit:提交
``` sh
helight@helight:~/kernel-mod/hello$ git-commit -m "some change" ./*
Created commit 2d900d9: some change
 1 files changed, 1 insertions(+), 0 deletions(-)
```

### git-whatchanged:查看本分支的修改情况
``` sh
helight@helight:~/kernel-mod/hello$ git-whatchanged
commit 2d900d918d24943b32f3d41b1974e0375be02c9e
Author: Zhenwen Xu <Helight.Xu@gmail.com>
Date:   Wed Nov 12 22:09:45 2008 +0800

    some change

:100644 100644 843a6b8... c762de7... M  hello.c

commit f4808f013f44e815831a3830a19925472be83424
Author: Zhenwen Xu <Helight.Xu@gmail.com>
Date:   Wed Nov 12 21:53:52 2008 +0800

    init the project

:000000 100644 0000000... c151955... A  Makefile
:000000 100644 0000000... 843a6b8... A  hello.c
helight@helight:~/kernel-mod/hello$
```
譬如我们要查看标号为 master和helight的版本的差异情况， 我们可以使用这样的命令：
``` sh
helight@helight:~/kernel-mod/hello$ git-diff helight  master
diff --git a/hello.c b/hello.c
index c762de7..843a6b8 100644
--- a/hello.c
+++ b/hello.c
@@ -14,7 +14,6 @@ static int __init hello_init(void)
 static void __exit hello_exit(void)
 {
        printk("kernel: %s\n","Bey world!");
-       printk("kernel: %s\n","Bey world!");
 }

 module_init(hello_init);
helight@helight:~/kernel-mod/hello$
补丁制作： git-format-patch
helight@helight:~/kernel-mod/hello$ vim hello.c
helight@helight:~/kernel-mod/hello$ git-commit -m "change by helight" hello.c
Created commit 4772773: change by helight
 1 files changed, 1 insertions(+), 0 deletions(-)
```
### 制作用于邮件发送的补丁：
``` sh
helight@helight:~/kernel-mod/hello$ git-format-patch -s master
0001-change-by-helight.patch
helight@helight:~/kernel-mod/hello$ cat 0001-change-by-helight.patch
From 4772773ecbbde66b8febc1d8aed0da67d480f1e4 Mon Sep 17 00:00:00 2001
From: Zhenwen Xu <Helight.Xu@gmail.com>
Date: Thu, 13 Nov 2008 10:30:10 +0800
Subject: [PATCH] change by helight


Signed-off-by: Zhenwen Xu <Helight.Xu@gmail.com>
---
 hello.c |    1 +
 1 files changed, 1 insertions(+), 0 deletions(-)

diff --git a/hello.c b/hello.c
index 89795d2..2cbf9ee 100644
--- a/hello.c
+++ b/hello.c
@@ -6,6 +6,7 @@ MODULE_LICENSE("GPL");
 static int __init hello_init(void)
 {
 	printk("kernel: %s\n","Hello world!");
+	printk("kernel: %s\n","This is Helight.Xu!");
         return 0;
 }

--
1.5.6.5

helight@helight:~/kernel-mod/hello$
```

### 分支合并：git-merge
现在我们看看怎么将helight分支上的工作合并到master分支中。现在转移我们当前的工作分支到 master，并且将helight分支上的工作合并进来。
``` sh
helight@helight:~/kernel-mod/hello$ git-checkout master
Switched to branch "master"
helight@helight:~/kernel-mod/hello$ git-merge "merge helight" HEAD helight
Updating f4808f0..2d900d9
Fast forward
 hello.c |    1 +
 1 files changed, 1 insertions(+), 0 deletions(-)
helight@helight:~/kernel-mod/hello$
```
但是更多的是将现在的工作pull到主分支上去，如下命令：
``` sh
helight@helight:~/kernel-mod/hello$ vim hello.c
helight@helight:~/kernel-mod/hello$ git-commit -m "another change" ./*
Created commit 1d6b878: another change
 1 files changed, 0 insertions(+), 3 deletions(-)
```
git-pull：将工作更新到分支上
``` sh
helight@helight:~/kernel-mod/hello$ git-checkout master
Switched to branch "master"
helight@helight:~/kernel-mod/hello$ git-pull . helight
From .
 * branch            helight    -> FETCH_HEAD
Updating 2d900d9..1d6b878
Fast forward
 hello.c |    3 ---
 1 files changed, 0 insertions(+), 3 deletions(-)
```
现在来看看如何退回到上一个版本：git-reset

命令形式：

git-reset [ --soft | --hard] [<commit-ish>]

命令的选项：

--soft : 恢复到 git-commit命令之前，但是所作的修改是不会发生变化的。

--hard :
将工作树中的内容和头索引都切换至指定的版本位置中，也就是说自上上一个git-commit命令之后的所有的跟踪内容和工作树中的内容都会全部丢失。 因此，这个选项要慎用，除非你已经非常确定你的确不想再看到那些东西了。

## git信息查看和日志查看：
* git-log
* git-show
* git-show-branch
* git-show-index
* git-show-ref


<center>
看完本文有收获？请分享给更多人<br>

关注「黑光技术」，关注大数据+微服务<br>

![](/images/qrcode_helight_tech.jpg)
</center>
