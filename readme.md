1、创建一个鸿蒙模拟器mcp服务，支持各agent使用鸿蒙模拟器，鸿蒙模拟器文档：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-emulator-command-line
2、mcp服务器会读取两个环境变量：instancePath:实例路径，imageRoot：镜像路径
3、鸿蒙模拟器启动命令：Emulator -hvd ”Mate 80 Pro Max“ -path {实例路径} -imageRoot {镜像路径} 
其中实例路径取自环境变量instancePath；镜像路径取自环境变量中imageRoot
当不存在对应环境变量时提示开发者配置环境变量
4、鸿蒙模拟器停止命令：Emulator -stop ”Mate 80 Pro Max“
5、鸿蒙应用安装命令：hdc install {应用路径} 
应用路径由开发者输入
6、将启动命令、停止命令、安装命令包装成mcp服务
7、mcp服务通过python编写，提供实现和测试脚本，可发布到Smithery上，可参考https://github.com/isdaniel/mcp_weather_server工程