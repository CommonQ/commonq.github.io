---
published: true
layout: post
title: Android JNI和NDK学习(1)--搭建开发环境
categories: Android
---

###NDK简介
NDK的好处:
```
1. 代码的保护，由于apk的java层代码很容易被反编译，而C/C++库反汇难度较大。

2. 在NDK中调用第三方C/C++库，因为大部分的开源库都是用C/C++代码编写的。

3. 便于移植，用C/C++写得库可以方便在其他的嵌入式平台上再次使用。
```
###Linux下NDK环境搭建
android的NDK开发需要在linux下进行： 因为需要把C/C++编写的代码生成能在arm上运行的.so文件，这就需要用到交叉编译环境，而交叉编译需要在linux系统下才能完成。
安装`android-ndk`开发包，在google android 官网下载： 通过这个开发包的工具才能将android jni 的C/C++的代码编译成库
android应用程序开发环境： 包括eclipse、java、 android sdk、 adt等。
安装完之后，需要将android-ndk的路劲加到环境变量PATH中：
```
sudo gedit /etc/environment
```
在environment的PATH环境变量中添加你的`android-ndk`的安装路劲，然后再让这个更改的环境变量立即生效：
```
 source  /etc/environment
```
经过了上述步骤，在命令行下敲：
```
ndk-bulid
```
弹出如下的错误，而不是说`ndk-build not found`，就说明ndk环境已经安装成功了。
###Windows下NDK环境搭建
在NDKr7开始，google的windos版NDK提供了一个ndk-build.cmd的脚本，这样就可以直接利用这个脚本编译，而不需要cygwin了。前面章节我介绍了NDK利用cygwin来进行配置（《NDK利用cygwin环境配置》），现在开始我们要与时俱进了,其实不同之处就是设置c/c++编译器的不同了。  
1. 选择你的android工程，右击选择Properties，弹出配置界面，之后再点击Builders，弹出项目的编译编译工具        列表，之后点击new，新添加一个编译器，点击之后出现添加界面，选择Program，点击ok。
2. 出现了添加界面，我们先给编译器设置名称，如XXX_builder。
3. 设置Location为<NDK安装目录>\ndk-build.cmd
4. 设置Working Directory为${workspace_loc:/项目名称}  
截图如下：  
![ndk_configure.jpg](/images/ndk_configure.jpg)
5. 切换到Refersh选项卡，给Refersh resources upon completion打上勾，选择The entire resource选项。  
截图如下：  
![ndk_configure2.jpg](/images/ndk_configure2.jpg)
6. 切换到Build Options选项卡，勾选上最后三项。再点击Specify Resource按钮，选择你的android工程的jni目录。  
截图如下：  
![ndk_configure3.jpg](/images/ndk_configure3.jpg)
7. 在编译工具列表，我们最好将我们新建的编译器置顶。选中点击Up按钮置顶。避免重复编译两次


```java
public static void main(String[] args){
    System.out.println("hello");

}

```

