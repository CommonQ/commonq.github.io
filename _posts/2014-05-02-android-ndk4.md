---
published: true
layout: post
title: Android JNI和NDK学习(4)--编译与预编译
categories: Android
---

###打包so文件

在apk里打包进.so文件的方法

1. 是在Android.mk文件里增加
LOCAL_JNI_SHARED_LIBRARIES := libxxx
这样在编译的时候，NDK自动会把这个libxxx打包进apk；
放在youapk/lib/目录下。

2. 是在应用的目录下手工建
libs/armeabi
目录，然后把libxxx.so拷贝到这个目录下，
这样NDK就会自动把这个libxxx.so打包进apk，位置还是在
放在yourapk/lib/目录下。
          
在代码里，使用
`System.loadLibrary("xxx");`
就可以加载这个动态库了。
这里要注意，参数只写xxx就可以了，不需要写libxxx，也不需要写libxxx.so。

还有一点要说明，System.loadLibrary这个函数会在如下路径搜索libxxx.so文件：
``` 
/system/lib
/data/data/you apk package/lib
``` 
但，如果libxxx.so还依赖其它.so文件，比如libyyy.so，则System.loadLibrary**只会
在/system/lib目录下去找，如果没找到，它不会自动到/data/data/you apk package/lib
下去找**，这个时候就会报动态库没找到的错；
解决方法是在load libxxx.so之前，先load libyyy.so，如下：  
```
System.loadLibrary("yyy");  
System.loadLibrary("xxx");  
```

###声明一个预编译库的模块

对于Android编译工具而言，每个预编译库必须声明为一个独立的模块。这里举一个例子，假设 libfoo.so 文件与 Android.mk 位于同一个目录：
```
LOCAL_PATH := $(call my-dir)  
include $(CLEAR_VARS)  
LOCAL_MODULE := foo-prebuilt  
LOCAL_SRC_FILES := libfoo.so  
include $(PREBUILT_SHARED_LIBRARY)  
```
按以下步骤声明这样一个模块：

1. 给该模块取一个名字（这里是 foo-prebuilt）。这个名字不需要与预编译库自身的名字相同。
2. 将 LOCAL_SRC_FILES 指定为你要提供的共享库的路径。通常，该路径是相对于 LOCAL_PATH 的路径。注意：必须保证共享库ABI的兼容性。
3. 如果你的库是共享库，则包含 PREBUILT_SHARED_LIBRARY 而不是 BUILD_SHARED_LIBRARY；如果是静态库，则包含 PREBUILT_STATIC_LIBRARY。
预编译模块不需要编译。该预编译模块会被拷贝到 $PROJECT/obj/local 下面，还会被拷贝到 $PROJECT/libs/<abi> 下面（这里的库被strip过）。

###在其他模块中引用这个预编译库
在依赖该预编译库的模块对应的Android.mk中，将预编译库的名字（前面取的）加入到 LOCAL_STATIC_LIBRARIES 或 LOCAL_SHARED_LIBRARIES 声明中。例如，一个使用上面libfoo.so的简单例子如下：
```
include $(CLEAR_VARS)  
LOCAL_MODULE := foo-user  
LOCAL_SRC_FILES := foo-user.c  
LOCAL_SHARED_LIBRARIES := foo-prebuilt  
include $(BUILD_SHARED_LIBRARY)  
```
