+++
title = "scons学习笔记"
date = "2010-05-18T13:47:08+02:00"
tags = ["scons", "gcc"]
categories = ["programming"]
banner = "/images/banners/SCons.png"
draft = false
author = "helight"
authorlink = "https://helight.cn"
summary = "scons是一个python写的用来编译源码的一个工具，类似于make工具，但是支持的语言更多，灵活性更强。 这里来介绍一下scons的使用。"
keywords = ["scons", "gcc", "g++"]
+++

# scons学习笔记

scons是一个python写的用来编译源码的一个工具，类似于make工具，但是支持的语言更多，灵活性更强。 这里来介绍一下scons的使用。下载可以在其官方网站：http://www.scons.org，源码安装就不说了，ubuntu和debian上安装更为方便，直接apt-get install scons就可以了。本文以编译c、c++为例来介绍其使用。

# 编译命令
在源代码目录下直接使用scons命令就可以编译，但是前提是编写好编译规则文件，默认的编译规则文件名是Sconstruct，和make的makefile或者Makefile文件一样。如下所示：
``` sh
helight:stl_test$ ls deque_test.cc SConstruct
```
deque_test.cc是编译源文件，SConstruct是编译默认规则文件，如果没有使用默认文件名，则在编译时要用参数 -f来指定规则文件，这个和make是一样的。直接使用scons命令编译即可，如下
``` sh
helight:stl_test$ scons 
scons: Reading SConscript files ... 
scons: done reading SConscript files. scons: Building targets ... 
g++ -o deque_test.o -c -I. deque_test.cc g++ -o deque_test deque_test.o -L. 
scons: done building targets. 
helight:stl_test$ ls deque_test deque_test.cc deque_test.o SConstruct 
helight:stl_test$
```
deque_test 即为编译出来的二进制程序。使用scons -c 即可clear刚刚的编译，和make clean一样，只不过make clean的规则要自己写或者由其他工具自动生成，scons的不需要写。 一般还会使用的scons参数： scons -Q 不输出scons解析配置文件的信息，只显示编译命令 scons -s 不输出任何信息，静默编译

# 编译规则文件说明
规则文件默认文件名SConstruct ，SConstruct 控制编译过程和编译结果，实际上SConstruct 是一个python脚本，其中可以有函数变量和一些复杂的操作过程。一般使用时里面的规则是比较简单的。SConstruct 文件是一个类似于makefile一样的东西, 告诉 scons做什么，而不是严格的规定soncs做这件事的步骤 scons支持编译多种类型的而进制文件，在c、c++编译中会出现的4种文件，object文件，可运行的二进制程序，静态库文件和动态库文件。在SConstruct中也分别用以下几种变量来标示： Program : generate executable file，可执行文件 Object : generate Object file， 编译中间文件 Library : 静态库， 也可以使用 StaticLibrary替代 SharedLibrary: 动态库 每种类型的文件编译规则都是类似的，所以就先以 Program文件来说明：
## 一般简单写法：
``` c
Program('hello.c')                # 生成 hello
Program('new_hello', 'hello.c')   # 生成 new_hello 
Library("test", "deque_test.o")
```

## 多个文件
``` c
Program(['prog.c', 'file1.c', 'file2.c'])             # 生成 prog
Program('program', ['prog.c', 'file1.c', 'file2.c'])  # 生成program
```

## 多个文件规则Glob匹配
``` c
Program('program', Glob('*.c') )
```

Glob原型为：Glob(self, pattern, ondisk=True, source=False, strings=False) 其中pattern 支持unix系统下的文件名匹配： *(任意多个字符), ?(单个字符) 和 [](括号中的任一字符)

## 使用split切分
``` c
Program('program', Split('main.c file1.c file2.c'))
```
Split以空格为分隔符，将字符串分割

## 使用关键字指明编译对象
``` c
Program(target = 'hello', source = 'hello.c')
``` 
## 下面是一个
``` c
Object("deque_test.cc") 
Library("test", "deque_test.o") 
SharedLibrary("test", "deque_test.cc") 
Program( target = 'deque_test', source = ["deque_test.o", "main.cc"], )
```

## 编译过程如下：
``` sh
helight:stl_test$ ls
deque_test.cc main.cc SConstruct 
helight:stl_test$ scons 
scons: Reading SConscript files ... 
scons: done reading SConscript files. 
scons: Building targets ... 
g++ -o deque_test.o -c deque_test.cc 
g++ -o main.o -c main.cc 
g++ -o deque_test deque_test.o main.o 
g++ -o deque_test.os -c -fPIC deque_test.cc 
ar rc libtest.a deque_test.o 
ranlib libtest.a 
g++ -o libtest.so -shared deque_test.os 
scons: done building targets. 
helight:stl_test$ ls 
deque_test deque_test.cc deque_test.o deque_test.os libtest.a libtest.so main.cc main.o SConstruct 
helight:stl_test$
```

## 多级目录编译：
``` c
SConscript(['test/SConstruct', 'serialize_boost/SConstruct']) #指定多个目录下的编译文件，逐个调用执行编译其它编译相关关键字在下面一一说明
```

# 编译相关关键字说明
## 基本的编译关键字
CPPFLAGS  指定编译选项LINKFLAGS 指定链接选项, 如 /DEBUG CPPDEFINES指定预编译器 
LIBS      指定所需要链接的库文件 
LIBPATH   指定库文件(.lib)的搜索目录 
CPPPATH   指定[.h, .c, .cpp]等文件搜索路径

## 指定编译选项
``` c
Program(target = 'bind_test1', source = ["bind_test1.cc"], LIBS = ['boost_system','boost_filesystem', 'boost_thread'], LIBPATH = ['./', '/usr/local/lib/' ], CPPPATH = ['./', '/usr/local/include/'], CCGLAGS = ['-g','-O3'] , CPPDEFINES={'RELEASE_BUILD' : '1'} )

注：LIBS和LIBPATH若为一个可以使用字符串，若为多个则使用列表

# 使用Environments
首先，如果一个目录下有多个编译目标（多个可执行二进制或者库文件），那么上面这些编译关键字是不是要每一个都要重新指定呢，这感觉上是增加了工作量，所以便有了Environments的出现，一个environment是一个影响程序执行的编译关键字值的集合，可以重复利用编译不同的目标。而环境变量也分为以下几种： 
1. 外部环境 External Environment 外部环境是运行Scons时 用户的环境变量。它们可以通过os.environ获取，这个使用过python或者使用linux程序的人都知道了，这里不详细说明。 
2. 构建环境 Construction Environment 它包含一些变量，这些变量会影响Scons构建目标的行为，包括编译关键字，当然还有其它一些变量。

一个Environment是一个 (name,value)的集合，可以这样查看它的内容：

env = Environment()
for item in env.Dictionary():                
    print '(%s:%s)' % (item, env[item])
## 实用变量
``` python
env['CC'] #查看 CC ，即C语言编译器
env.subst('$CC') # 功能同上 
env['PLATFORM'] == 'win32' #判断是否是windows:环境变量的基本操作
env.Clone #拷贝一个环境变量，详见user guide 7.2.7
env.Replace #替换一个已经存在的环境变量 
env.SetDefault #为一个没有被定义的变量设置默认值 
env.Append(CCFLAGS = '-option -O3 -O1') #为一个已存在的环境变量增加一个值 
env.AppendUnique #为一个环境变量增加一个唯一的值 
env.Prepend #在最前边添加一个值 
env.PrependUnique #在最前边添加一个唯一的值 
env.MergeFlags  # 例如： flags = {'CCFLAGS':'-option -O3 -O1'} 
env.MergeFlags(flags) flags = {'CPPPATH' : ['/user/opt/include', 'user/local/include']} 
env.MergeFlags(flags)
```

## 实例：
``` python
env = Environment() # Initialize the environment 
env.Append(CCFLAGS = ['-g','-O3']) 
env.Append(LIBS = ['boost_system','boost_filesystem', 'boost_thread']) 
env.Append(CPPDEFINES={'RELEASE_BUILD' : '1'}) 
env.Append(LIBPATH = ['/usr/local/lib/']) 
env.Append(CPPDEFINES=['BIG_ENDIAN']) 
env.Append(CPPPATH = ['/usr/local/include/']) #env.ParseConfig( 'pkg-config --cflags glib-2.0' )   
env.Program( target = 'test2', source = ["test2.cc"] )   
env.Program( target = 'test3', source = ["test3.cc"] )   
env.Program( target = 'test4', source = ["test4.cc"] )
```
3. 执行环境 Execution Environment 
执行环境用于Scons执行外部命令(external command), 以构建一个或多个目标。 注意：它与外部环境不相同 当scons构建一个目标文件时，它所使用的外部环境和执行scons时的环境变量是不同的。scons使用$ENV 构建变量 中 存储的目录 作为它执行命令的外部环境变量。 实用变量：PATH，path决定了库的引用，命令的寻找等。 POSIX 系统中默认的PATH是 /user/local/bin:/user/bin Window系统中默认的PATH是 command interpreter在注册表中的值
``` python
path = ['/user/local/bin', '/bin', '/user/bin']           
env = Environment(ENV = {'PATH':path}) 
env = Environment(ENV = {'path' : os.environ['PATH']}) #从 外部环境 初始化 PATH 
env = Environment(ENV = os.environ) #将完整的外部变量传递给执行环境变量 这样做的缺点是：如果环境变量目录中，有多个目录包含编译器如gcc，那么 scons将执行第一个被找到的gcc 
env.PrependENVPath('PATH', '/user/local/bin') #将'/user/local/bin' 插入 $PATH中第一个位置 
env.AppendENVPath('lib', '/user/local/lib') #将'/user/local/bin' 插入 $LIB中最后一个位置 
```

# 控制目标文件的路径
## 安装目录指定： 
``` python
test = env.Program('test.cpp')env.Install('bin', 'test') #表示要将test放到bin目录下 
env.Install('bin', test) 
env.Program('bin/test', 'test.cpp') 
env.InstallAs('bin/testapp', 'test')
```

## obj文件路径 
使用VariantDir函数指定，具体使用见这里：http://www.scons.org/wiki/VariantDir%28%29 主要是把编译的过程文件和源文件分离，让人在编译的时候不感觉源代码路径凌乱。 如下实例：
``` python
VariantDir(".obj/", "./", duplicate=0); 
env = Environment() # Initialize the environment 
test = Environment() # Initialize the environment 
env.Append(CCFLAGS = ['-g','-O3']) 
env.Append(LIBS = ['boost_system','boost_filesystem', 'boost_thread']) 
env.Append(CPPDEFINES={'RELEASE_BUILD' : '1'}) 
env.Append(LIBPATH = ['/usr/local/lib/']) 
env.Append(CPPDEFINES=['BIG_ENDIAN']) 
env.Append(CPPPATH = ['/usr/local/include/']) #env.ParseConfig( 'pkg-config --cflags glib-2.0' )   
env.Program( target = 'test2', source = [".obj/test2.cc"] )   
env.Program( target = 'test3', source = [".obj/test3.cc"] )  
env.Program( target = 'test4', source = [".obj/test4.cc"] )
```

<center>
看完本文有收获？请分享给更多人<br>

关注「黑光技术」，关注大数据+微服务<br>

![](/images/qrcode_helight_tech.jpg)
</center>
