+++
title = "golang grpc简单使用"
date = "2019-05-18T13:47:08+02:00"
tags = ["grpc", "golang"]
categories = ["golang"]
banner = "/images/banners/grpc.jpg"
draft = false
author = "helight"
authorlink = "https://helight.cn"
summary = "golang grpc简单使用"
keywords = ["golang","grpc", "proto"]
+++

# 前言
上一篇文章简单体验了一下grpc的golang使用，从环境安装到简单demo的编写，编译和测试，感觉还不错，今天再进一步学习分析其用法和一些要注意的坑。

# grpc介绍
grpc一开始由 google 开发，是一款语言中立、平台中立、开源的远程过程调用(RPC)系统。是一个高性能、开源和通用的 RPC 框架，面向移动和 HTTP/2 设计。目前提供 C、Java 和 Go 语言版本。而且gRPC 基于 HTTP/2 标准设计，带来诸如双向流、流控、头部压缩、单 TCP 连接上的多复用请求等特。这些特性使得其在移动设备上表现更好，更省电和节省空间占用。

从学习上来说，grpc的文档真是很全面了，https://grpc.io/docs/ 官网这里各种语言版本的都可以找到，golang的可以看这几篇，这篇的大部分内容都是来自这里的梳理。

[Quick Start Guide][1]
[gRPC Basics Tutorial][2]
[API Reference][3]
[Generated Code Reference][4]
另外还有一个中文版的教程：[gRPC 官方文档中文版][5]

# proto
首先要说一下的还是proto文件的定义，这个定义才是最关键的，这个里面定义了grpc所需要的所有数据结构和服务。

proto文件在其[网站][6]也有非常详细的说明，这里我就不展开了，在proto文件中有两种必要的类型，一种就是消息体：message，另外一种就是service。
message的定义和我们以前使用的proto的定义方式和含义是一样的。

service就是定义一个服务，这个对于client和server端代码都需要用，主要作用就是生成服务端和客户端的stub。这里以route_guide.proto这个文件中的例子来说明：
``` proto
	service RouteGuide {
		rpc GetFeature(Point) returns (Feature) {}
  		rpc ListFeatures(Rectangle) returns (stream Feature) {}
  		rpc RecordRoute(stream Point) returns (RouteSummary) {}
  		rpc RouteChat(stream RouteNote) returns (stream RouteNote) {}
	}
```
这里定义了一个service：RouteGuide，这个服务里面有4个rpc服务：

第一个rpc服务是最简单的一种就是给一个参数Point获取一个Feature。这种也是非常常见的一种rpc服务。

第二个rpc服务是给一个参数Point，获取多个Feature，返回值是以repeated field message的形式返回，实际上就是以数据流形式返回一个数组。

第三个rpc服务是给一个message输入流，获取一个返回message

第四个rpc服务是给一个message输入流，获取一个message返回流

# 使用proto定义一个服务
这个proto文件编译之后会生成一个xx.pb.go的文件，这文件是proto编译之后生成的，主要是针对其中message序列化方法的实现，还有就是生成我们定义的server和client的stub文件，其实在go中就是一个interface。比如官方例子中的就生成了type RouteGuideServer interface和type RouteGuideClient interface，另外两个比较重要的方法，一个是针对客户端的，一个是针对服务端的：
## 服务端定义
``` go
type routeGuideClient struct { 
    // 是对type RouteGuideClient interface的具体实现，routeGuideClient实现了RouteGuideClient的所有方法
	cc *grpc.ClientConn  
}

func NewRouteGuideClient(cc *grpc.ClientConn) RouteGuideClient {
	return &routeGuideClient{cc} // 这里返回的就是一个RouteGuideClient类型的实现了，后面就可以用这个客户端中的方法先server端发起调用了
}
...
func RegisterRouteGuideServer(s *grpc.Server, srv RouteGuideServer) { // 这个函数提供了一个RouteGuideServer注册到grpc.Server上。
	s.RegisterService(&_RouteGuide_serviceDesc, srv) // 是对这个服务的一个grpc.Server的描述，详细的可以看下面的代码
...
var _RouteGuide_serviceDesc = grpc.ServiceDesc{
	ServiceName: "routeguide.RouteGuide",
	HandlerType: (*RouteGuideServer)(nil),
	Methods: []grpc.MethodDesc{ // 单纯的函数调用接口描述
		{
			MethodName: "GetFeature",
			Handler:    _RouteGuide_GetFeature_Handler,
		},
	},
	Streams: []grpc.StreamDesc{ // 有流式数据调用的接口描述
		{
			StreamName:    "ListFeatures",
			Handler:       _RouteGuide_ListFeatures_Handler,
			ServerStreams: true,
		},
		{
			StreamName:    "RecordRoute",
			Handler:       _RouteGuide_RecordRoute_Handler,
			ClientStreams: true,
		},
		{
			StreamName:    "RouteChat",
			Handler:       _RouteGuide_RouteChat_Handler,
			ServerStreams: true,
			ClientStreams: true,
		},
	},
	Metadata: "route_guide.proto",
}
``` 
## server端关键的几句代码可以看看
``` go
type routeGuideServer struct {} //定义一个实现体，后面还有具体服务方法的实现
...
func newServer() *routeGuideServer {
	s := &routeGuideServer{}
	return s
}
...
lis, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", *port))
...
grpcServer := grpc.NewServer(opts...) // opts是安全证书之类的参数
pb.RegisterRouteGuideServer(grpcServer, newServer()) // 注册到grpcServer
grpcServer.Serve(lis) // 把监听端口传给server
```
## 客户端的关键代码
``` go
conn, err := grpc.Dial(*serverAddr, opts...) // 创建连接
....
client := pb.NewRouteGuideClient(conn) // 传连接返回实例化的客户端，这样就可以直接调用rpc方法了
...
feature, err := client.GetFeature(context.Background(), point)
...
```
# 总结
简单来说grpc的开发还是有点原始，在proto的定义和转换为框架代码上都还比较粗。在内部项目中使用的话还是要自己开发不少中间件来补充功能，但是在一般简单服务中grpc是已经足够使用了。

[1]: https://grpc.io/docs/quickstart/go.html
[2]: https://grpc.io/docs/tutorials/basic/go.html
[3]: https://godoc.org/google.golang.org/grpc
[4]: https://grpc.io/docs/reference/go/generated-code.html
[5]: http://doc.oschina.net/grpc
[6]: https://developers.google.com/protocol-buffers/docs/proto3


<center>
看完本文有收获？请分享给更多人

关注「黑光技术」，关注大数据+微服务

![](/images/qrcode_helight_tech.jpg)
</center>