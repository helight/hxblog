+++
title = "golua虚拟机的使用"
date = "2018-11-18T13:47:08+02:00"
tags = ["golang", "lua"]
categories = ["golang"]
banner = "/images/banners/golua.jpg"
draft = false
author = "helight"
authorlink = "https://helight.cn"
summary = "[gopher-lua](https://github.com/yuin/gopher-lua)这个组件，这个是使用golang重写的支持Lua5.1的虚拟机，在执行上可以直接golang无缝结合，有非常好的go的api接口，在使用上也流畅很多，在实现思路上也采用golang的一些思路，和golang结合更好。"
keywords = ["go","golang", "lua", "gopher-lua"]
+++

# 前言
​      之前一直想把openflow这样的分布式流程系统做起来，但是时间和应用场景的问题所以都是做了一个半拉子工程，而且之前想的也有点简单了，认为只要有同学愿意，在开发上应该没问题，但是最终还是出现了项目管理和开发能力的问题，最终搁浅了。但是我想做一个分布式流程调度系统的想法一直没有断，其实在公司内和另外一个同学做过一个flow系统，也在线上使用了，直到现在还在使用。前一段时间就想把这个系统再优化梳理一下，目标是做一个小巧的开源可用版本。经过一段时间的梳理目前已经初步完成了，后台+前端代码的重新梳理也已经完成了。

# lua虚拟机的使用

​      而今天主要想写的是其中使用到的一个技术点：lua。内部版本我们使用的是golang开发，但是在执行中为了保证流程之间不会互相影响，我们使用lua虚拟机技术；让每个流程在执行的时候在一个独立的lua虚拟机中执行。内部版本使用golua这个组件，但是这个组件有个问题，它其实是一个cgo的版本，就是它其实上是调用本地lua库来执行，所在在编译部署和执行上都有一定的效率问题。

​	所以在新开发的版本上我想使用其它的方式，在研究了一段时间后决定使用[gopher-lua](https://github.com/yuin/gopher-lua)这个组件，这个是使用golang重写的支持Lua5.1的虚拟机，在执行上可以直接golang无缝结合，有非常好的go的api接口，在使用上也流畅很多，在实现思路上也采用golang的一些思路，和golang结合更好。也通过这次学习了一把lua，才发现这个技术确实很牛，据统计lua的c实现代码才1w行左右，但是执行非常高效，而且lua的预留关键字也非常少。可以说是一个非常简洁又高效的语言。

# gopher-lua的一些特点

​	在我这个flow项目非常合适，所以用gopher-lua替换了golua，因为gopher-lua的api和类型支持比golua要好很多，所以在替换后精简了不少代码。下面就介绍一下项目中使用到的一些关键点。

## lua虚拟机的创建使用

​	在使用上api非常简单，主要有以下几步：

1. 引入gopher-lua
2. 创建虚拟机
3. 使用虚拟机执行lua语句或lua脚本文件
4. 关闭虚拟机

```go
package main

import lua "github.com/yuin/gopher-lua" // 1.引入gopher-lua

func main() {
	L := lua.NewState() // 2.创建一个lua解释器实例
	defer L.Close()    // 4.关闭虚拟机
	if err := L.DoString(`print("hello")`); err != nil { // 3.用创建的虚拟机来执行lua语句   
     // if err := L.DoFile("hello.lua"); err != nil { // 3.用创建的虚拟机来执行lua脚本文件
		panic(err)
	}
}
```

​	api在使用上还是非常简单的。其它关于基本数据类型的这里就不多介绍了，在其github站点上有非常详细的介绍。

​	下面将主要介绍2个在flow项目中用到的非常有用的功能点。

## go中调用lua函数

​	用golang写的服务，如果我们要使用lua脚本中定义的函数怎么办呢？在gopher-lua提供了响应的方法，在其站点也有非常好的例子来说明：

1. 首先用DoFile方法来加载lua脚本，在脚本中定义需要lua函数
2. 其次使用CallByParam函数进行调用

```go
L := lua.NewState()
defer L.Close()
if err := L.DoFile("double.lua"); err != nil {
    panic(err)
}
if err := L.CallByParam(lua.P{
    Fn: L.GetGlobal("double"), 	  // 获取double这个函数的引用
    NRet: 1,					// 指定返回值数量
    Protect: true,                // 如果出现异常，是panic还是返回err
    }, lua.LNumber(10)); err != nil { // 传递输入参数：10
    panic(err)
}
ret := L.Get(-1) // 获取返回结果值
L.Pop(1)  // 从堆栈中扔掉返回结果
```

​	GopherLua的函数调用是通过堆栈来进行的，调用前把需要传递给函数的参数压到栈里，函数执行完成之后再将结果放入堆栈中，调用方通过在堆栈顶部拿函数执行结果。 

# lua脚本中调用go函数

​	go调用lua函数在flow项目中用的相对较少，用的较多的是下面一种：lua脚本中调用go函数；因为很多复杂操作其实用lua来做还是有点复杂和不安全，尤其有些公共操作或者复杂的db操作。所以好的做法是在go中把函数封装好，再在外部写lua脚本，执行的时候可以调用go函数，这样既可以满足lua脚本的灵活性，也极大的扩展了lua的能力和减低了编写复杂度。

​	先看看其基本使用方法，也是通过官网的例子来说明。	

```go
func Double(L *lua.LState) int {
    lv := L.ToInt(1)             // 获取七个参数
    L.Push(lua.LNumber(lv * 2))  // 把计算结果压栈
    return 1                     // 返回计算返回参数的个数
}

func main() {
    L := lua.NewState()
    defer L.Close()
    L.SetGlobal("double", L.NewFunction(Double)) // 注册函数
}
```

​	首先再gopher-lua中有一个类型[lua.LGFunction ](https://godoc.org/github.com/yuin/gopher-lua#LGFunction)，这个类型就是一个函数类型，它固定了函数的入参和出参，入参就是lua.LState的一个引用，返回值就是一个int。如下面的定义，如果需要跟多的参数就需要使用堆栈或者对lua.LState扩展成员的方式。在执行完成之后也是通过堆栈或者对lua.LState扩展成员的方式把返回值传递出去。

​	函数的注册有多种方式，上面是一种方式，另外我从网上还看到一种方式，就是使用lua的table的方式。

```
	myfuns := L.NewTable()
	L.SetGlobal("myfuns", myfuns)
	// 注册函数
	L.SetField(myfuns, "gofun1", L.NewFunction(gofun1))
	....
	// 调用方式
	err := L.DoString(`
		test = myfuns:gofun1("test")
	`)
```

​	这里面不方便的一点就是参数的传递和获取不是很直观，很多时候需要二次分装调用函数。这一点有点不方便。其它还好。

​	GopherLua可以创建一个非常干净的Lua解释器实例，不加载任何系统模块。然后由程序员自己提供的模块注册进去，给内嵌脚本提供一个安全的沙箱运行环境。 

# 参考文档

1. https://github.com/yuin/gopher-lua
2. https://zhuanlan.zhihu.com/p/33471484
3. https://segmentfault.com/a/1190000011527968
4. http://www.runoob.com/lua/lua-tutorial.html

<center> 
看完本文有收获？请分享给更多人 <br> 关注「黑光技术」，关注大数据+微服务 <br> 

![](/images/qrcode_helight_tech.jpg) 
</center>
