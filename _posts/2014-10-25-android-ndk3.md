---
published: true
layout: post
title: Android ndk3
categories: Android
---

###参数解析
以刚才的`Android.mk`为例.
```makefile

# Copyright (C) 2009 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE    := hello-jni
LOCAL_SRC_FILES := hello-jni.c

include $(BUILD_SHARED_LIBRARY)
```

**LOCAL_PATH := $(call my-dir)**
```
一个Android.mk 文件首先必须定义好LOCAL_PATH变量。它用于在开发树中查找源文件。在这个例子中，宏函数’my-dir’, 由编译系统提供，用于返回当前路径（即包含Android.mk file文件的目录）。
```

**include $( CLEAR_VARS)**
```
CLEAR_VARS由编译系统提供，指定让GNU MAKEFILE为你清除许多LOCAL_XXX变量（例如 LOCAL_MODULE, LOCAL_SRC_FILES, LOCAL_STATIC_LIBRARIES, 等等...), 
除LOCAL_PATH 。这是必要的，因为所有的编译控制文件都在同一个GNU MAKE执行环境中，所有的变量都是全局的。
```

**LOCAL_MODULE := hello-jni**
```
编译的目标对象，LOCAL_MODULE变量必须定义，以标识你在Android.mk文件中描述的每个模块。名称必须是唯一的，而且不包含任何空格。

注意：编译系统会自动产生合适的前缀和后缀，换句话说，一个被命名为'hello-jni'的共享库模块，将会生成'libhello-jni.so'文件。

重要注意事项：

如果你把库命名为‘libhello-jni’，编译系统将不会添加任何的lib前缀，也会生成 'libhello-jni.so'，这是为了支持来源于Android平台的源代码的Android.mk文件，如果你确实需要这么做的话。
```
**LOCAL_SRC_FILES := hello-jni.c**
```
LOCAL_SRC_FILES变量必须包含将要编译打包进模块中的C或C++源代码文件。注意，你不用在这里列出头文件和包含文件，因为编译系统将会自动为你找出依赖型的文件；仅仅列出直接传递给编译器的源代码文件就好。

注意，默认的C++源码文件的扩展名是’.cpp’. 指定一个不同的扩展名也是可能的，只要定义LOCAL_DEFAULT_CPP_EXTENSION变量，不要忘记开始的小圆点（也就是’.cxx’,而不是’cxx’）
```
**include $(BUILD_SHARED_LIBRARY)**
```
BUILD_SHARED_LIBRARY表示编译生成共享库，是编译系统提供的变量，指向一个GNU Makefile脚本，负责收集自从上次调用'include $(CLEAR_VARS)'以来，定义在LOCAL_XXX变量中的所有信息，并且决定编译什么，如何正确地去做。还有 BUILD_STATIC_LIBRARY变量表示生成静态库：lib$(LOCAL_MODULE).a， BUILD_EXECUTABLE 表示生成可执行文件。
```

在这里详细叙述一下Android.mk语法规范

###Android.mk文件的用途
一个android子项目中会存在一个或多个Android.mk文件   
**1、单一的Android.mk文件 **  
直接参考NDK的sample目录下的hello-jni项目，在这个项目中只有一个Android.mk文件   
**2、多个Android.mk文件   **
如果需要编译的模块比较多，我们可能会将对应的模块放置在相应的目录中， 
这样，我们可以在每个目录中定义对应的Android.mk文件（类似于上面的写法）， 
最后，在根目录放置一个Android.mk文件，内容如下： 
```
include $(call all-subdir-makefiles) 
```
只需要这一行就可以了，它的作用就是包含所有子目录中的Android.mk文件    
**3、多个模块共用一个Android.mk **  
这个文件允许你将源文件组织成模块，这个模块中含有：   
  -静态库(.a文件)   
  -动态库(.so文件)   
只有共享库才能被安装/复制到您的应用软件（APK）包中   
`include $(BUILD_STATIC_LIBRARY)`，编译出的是静态库   
`include $(BUILD_SHARED_LIBRARY)`，编译出的是动态库   

###自定义变量 
以下是在 Android.mk中依赖或定义的变量列表，可以定义其他变量为自己使用，但是NDK编译系统保留下列变量名：  
-以 LOCAL_开头的名字（例如 LOCAL_MODULE）   
-以 PRIVATE_, NDK_ 或 APP_开头的名字（内部使用）   
-小写名字（内部使用，例如‘my-dir’）   
如果为了方便在 Android.mk 中定义自己的变量，建议使用 MY_前缀，一个小例子： 
```
MY_SOURCES := foo1.c 
ifneq ($(MY_CONFIG_BAR),) 
MY_SOURCES += bar.c 
endif 
LOCAL_SRC_FILES += $(MY_SOURCES) 
```
注意：‘:=’是赋值的意思；'+='是追加的意思；‘$’表示引用某变量的值。 

###GNU Make系统变量 
这些 GNU Make变量在你的 Android.mk 文件解析之前，就由编译系统定义好了。注意在某些情况下，NDK可能分析 Android.mk 几次，每一次某些变量的定义会有不同。   



1. CLEAR_VALS  
指向一个编译脚本，几乎所有未定义的 LOCAL_XXX 变量都在"Module-description"节中列出。必须在开始一个新模块之前包含这个脚本：include$(CLEAR_VARS)，用于重置除LOCAL_PATH变量外的，所有LOCAL_XXX系列变量

2. BUILD_SHARED_LIBRARY:  
指向编译脚本，根据所有的在 LOCAL_XXX 变量把列出的源代码文件编译成一个共享库。   
注意，必须至少在包含这个文件之前定义 LOCAL_MODULE 和 LOCAL_SRC_FILES。   

3. BUILD_STATIC_LIBRARY:   
一个 BUILD_SHARED_LIBRARY 变量用于编译一个静态库。静态库不会复制到的APK包中，但是能够用于编译共享库。 
示例：include $(BUILD_STATIC_LIBRARY) 
注意，这将会生成一个名为 lib$(LOCAL_MODULE).a 的文件 
4. TARGET_ARCH: 目标 CPU平台的名字 
5. TARGET_PLATFORM: Android.mk 解析的时候，目标 Android 平台的名字.详情可考/development/ndk/docs/stable- apis.txt. 
       android-3 -> Official Android 1.5 system images 
       android-4 -> Official Android 1.6 system images 
       android-5 -> Official Android 2.0 system images 
6. TARGET_ARCH_ABI:  暂时只支持两个 value，armeabi 和 armeabi-v7a。。 
7. TARGET_ABI: 目标平台和 ABI 的组合， 

###模块描述变量 
下面的变量用于向编译系统描述你的模块。应该定义在'include  $(CLEAR_VARS)'和'include $(BUILD_XXXXX)'之间。$(CLEAR_VARS)是一个脚本，清除所有这些变量。   

1. LOCAL_PATH:  这个变量用于给出当前文件的路径。
       必须在 Android.mk 的开头定义，可以这样使用：LOCAL_PATH := $(call my-dir) 
       如当前目录下有个文件夹名称 src，则可以这样写 $(call src)，那么就会得到 src 目录的完整路径 
       这个变量不会被$(CLEAR_VARS)清除，因此每个 Android.mk 只需要定义一次(即使在一个文件中定义了几个模块的情况下)。 
2. LOCAL_MODULE: 这是模块的名字，它必须是唯一的，而且不能包含空格。 
       必须在包含任一的$(BUILD_XXXX)脚本之前定义它。模块的名字决定了生成文件的名字。 
3. LOCAL_SRC_FILES:  这是要编译的源代码文件列表。 
       只要列出要传递给编译器的文件，因为编译系统自动计算依赖。注意源代码文件名称都是相对于 LOCAL_PATH的，你可以使用路径部分，例如： 
        LOCAL_SRC_FILES := foo.c toto/bar.c\ 
        Hello.c 
       文件之间可以用空格或Tab键进行分割,换行请用"\" 
       如果是追加源代码文件的话，请用LOCAL_SRC_FILES += 
       注意：可以LOCAL_SRC_FILES := $(call all-subdir-java-files)这种形式来包含local_path目录下的所有java文件。 
4. LOCAL_C_INCLUDES:  可选变量，表示头文件的搜索路径。 
        默认的头文件的搜索路径是LOCAL_PATH目录。 
5. LOCAL_STATIC_LIBRARIES: 表示该模块需要使用哪些静态库，以便在编译时进行链接。 
6. LOCAL_SHARED_LIBRARIES:  表示模块在运行时要依赖的共享库（动态库），在链接时就需要，以便在生成文件时嵌入其相应的信息。 
       注意：它不会附加列出的模块到编译图，也就是仍然需要在Application.mk 中把它们添加到程序要求的模块中。 
7. LOCAL_LDLIBS:  编译模块时要使用的附加的链接器选项。这对于使用‘-l’前缀传递指定库的名字是有用的。 
       例如，LOCAL_LDLIBS := -lz表示告诉链接器生成的模块要在加载时刻链接到/system/lib/libz.so 
       可查看 docs/STABLE-APIS.TXT 获取使用 NDK发行版能链接到的开放的系统库列表。 
8. LOCAL_MODULE_PATH 和 LOCAL_UNSTRIPPED_PATH 
       在 Android.mk 文件中， 还可以用LOCAL_MODULE_PATH 和LOCAL_UNSTRIPPED_PATH指定最后的目标安装路径. 
       不同的文件系统路径用以下的宏进行选择： 
       TARGET_ROOT_OUT：表示根文件系统。 
       TARGET_OUT：表示 system文件系统。 
       TARGET_OUT_DATA：表示 data文件系统。 
       用法如：LOCAL_MODULE_PATH :=$(TARGET_ROOT_OUT) 
       至于LOCAL_MODULE_PATH 和LOCAL_UNSTRIPPED_PATH的区别，暂时还不清楚。 
9. LOCAL_JNI_SHARED_LIBRARIES：定义了要包含的so库文件的名字，如果程序没有采用jni，不需要 
        LOCAL_JNI_SHARED_LIBRARIES := libxxx 这样在编译的时候，NDK自动会把这个libxxx打包进apk； 放在youapk/lib/目录下 

###NDK提供的函数宏 
GNU Make函数宏，必须通过使用'$(call  )'来调用，返回值是文本化的信息。   

1. my-dir:返回当前 Android.mk 所在的目录的路径，相对于 NDK 编译系统的顶层。这是有用的，在 Android.mk 文件的开头如此定义： 
        LOCAL_PATH := $(call my-dir) 
2. all-subdir-makefiles: 返回一个位于当前'my-dir'路径的子目录中的所有Android.mk的列表。 
       例如，某一子项目的目录层次如下： 
            src/foo/Android.mk 
            src/foo/lib1/Android.mk 
            src/foo/lib2/Android.mk 
      如果 src/foo/Android.mk 包含一行： 
           include $(call all-subdir-makefiles) 
      那么它就会自动包含 src/foo/lib1/Android.mk 和 src/foo/lib2/Android.mk。 
      这项功能用于向编译系统提供深层次嵌套的代码目录层次。 
      注意，在默认情况下，NDK 将会只搜索在 src/*/Android.mk 中的文件。 
3. this-makefile:  返回当前Makefile 的路径(即这个函数调用的地方) 
4. parent-makefile:  返回调用树中父 Makefile 路径。即包含当前Makefile的Makefile 路径。 
5. grand-parent-makefile：返回调用树中父Makefile的父Makefile的路径 
###Android.mk示例


```makefile
#编译静态库  
LOCAL_PATH := $(call my-dir)  
include $(CLEAR_VARS)  
LOCAL_MODULE = libhellos  
LOCAL_CFLAGS = $(L_CFLAGS)  
LOCAL_SRC_FILES = hellos.c  
LOCAL_C_INCLUDES = $(INCLUDES)  
LOCAL_SHARED_LIBRARIES := libcutils  
LOCAL_COPY_HEADERS_TO := libhellos  
LOCAL_COPY_HEADERS := hellos.h  
include $(BUILD_STATIC_LIBRARY)  
  
#编译动态库  
LOCAL_PATH := $(call my-dir)  
include $(CLEAR_VARS) 
LOCAL_MODULE = libhellod 
LOCAL_CFLAGS = $(L_CFLAGS) 
LOCAL_SRC_FILES = hellod.c 
LOCAL_C_INCLUDES = $(INCLUDES) 
LOCAL_SHARED_LIBRARIES := libcutils 
LOCAL_COPY_HEADERS_TO := libhellod 
LOCAL_COPY_HEADERS := hellod.h 
include $(BUILD_SHARED_LIBRARY) 

```


