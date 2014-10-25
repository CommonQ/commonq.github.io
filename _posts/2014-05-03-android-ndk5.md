---
published: true
layout: post
title: Android JNI和NDK学习(5)--JNI分析API
categories: Android
---

Date: 2014-05-01
Title: Android JNI和NDK学习(5)--JNI分析API
Category: Android
Tags: Android, NDK
Slug: Android_ndk_5

###Java类型和本地类型对应
在如下情况下，需要在本地方法中应用java对象的引用，就会用到类型之间的转换：

1. java方法里面将参数传入本地方法；
2. 在本地方法里面创建java对象；
3. 在本地方法里面return结果给java程序。

####Java基本类型

像booleans、integers、floats等从Java程序中传到本地方法中的原始类型可以直接使用，下面是java中的原始类型和本地方法中的类型的对应：

Java 类型本地类型说明

	boolean jboolean 无符号，8 位  
	byte jbyte 无符号，8 位  
	char jchar 无符号，16 位    
	short jshort 有符号，16 位  
	int jint 有符号，32 位  
	long jlong 有符号，64 位  
	float jfloat 32 位  
	double jdouble 64 位  
	void void N/A  


也就是说如果我在方法中传进去了一个boolean的参数的话，那么我在本地方法中就有jboolean类型与之对应。同理，如果在本地方法中return一个jint的话，那么在java中就返回一个int类型。

为了使用方便，特提供以下定义。

	#define JNI_FALSE 0
	#define JNI_TRUE 1


jsize 整数类型用于描述主要指数和大小：
typedef jint jsize;

###Java String类型
在java中，使用的字符串String对象是Unicode码，即每个字符不论是中文还是英文或是符号，一个字符总是占用两个字节。
在c/c++本地代码中创建java的String对象
.java通过JNI接口可以将java的字符串转换到c/c++中的宽字符串(wchar_t *),或是传回一个UTF-8的字符串（char *）到c/c++。反过来，c/c++可以通过一个宽字符串，或是一个UTF-8编码的字符串来创建一个java端的String对象。

	GetStringChars/GetStringUTFChars

.这两个函数用来取得与某个jstring对象相关的java字符串。分别可以取得UTF-16编码的宽字符串（jchar*）跟UTF-8编码的字符串（char*）。

	Const jchar* GetStringChars(jstring str, jboolean* copied)
	Const char* GetStringUTFChars(jstring str, jboolean* copied)

第一个参数传入一个指向java中的String对象的jstring变量  
第二个参数传入的是一个jboolean的指针。  
这两个函数分别都会有两个不同的动作：  
**第一个参数：**  
1.  开新内存，然后把java中的String拷贝到这个内存中，然后返回这个内存地址的指针。  
2.  直接返回指向java中string的内存的指针，这个时候千万不要改变这个内存的内容，这将破坏String在java中始终是常量这个原则。  
**第二个参数：**  
是用来标示是否对java的string对象进行了拷贝的。
如果传入的这个jboolean指针不是null,则他会给该指针指向的内存传入JNI_TRUE或JNI_FALSE标示是否进行了拷贝。
传入null标示不关心是否拷贝字符串，它就不会给jboolean*指向的内存赋值。
使用这两个函数取得的字符串，在不使用的时候，要使用`ReleaseStringChars/ReleaseStringUTFChars`来释放拷贝的内存，或是释放对java的String对象的引用。

	ReleaseStringChars(jstring jstr, const jchar* str);
	ReleaseStringUTFChars(jstring jstr, const char* str);

第一个参数指定一个jstring变量，即是要释放的本地字符串的来源。  
第二个参数就是要释放的本地字符串  


###访问类对象的属性

env 为 JNIEnv,obj的类型为jobject


	JAVA_FieldAccessTest_accessField(JNIEnv *env,jobject obj){
     
     	jfieldID fid;
     	jclass cls = (*env)->GetObjectClass(env, obj);
     	//类FieldAccessTest中有个String类型的属性s
     
     	//获取要访问的属性的id
     	fid = (*env)->GetFieldID(evn,cls,"s","Ljava/lang/String;");
    	//读取属性值
    	jstring jstr = (*env)->GetObjectField(env,obj,fid);
    	char* str  = (*evn)->GetStringUTFChars(env,jstr,NULL);
   
	 //释放资源
   	（*env)->ReleaseStringUTFChars(env,jstr,str);

    	//现在反过来，改变调用该本地方法的java对象的属性值
    	jstr = (*env)->NewStringUTF(env,"88888");
	 (*env)->SetObjectField(env,obj,fid,jstr);

	}


总结：

	1. jfieldID fid = (*env)->GetFieldID(env,对象所属的类的jclass,
        	    属性名,
            	属性对应的属性描述符号);
	2. (*env)->GetObjectField(env,对象,属性id);


####访问静态属性：
  假如有个类如下：

 	class StaticFielcTest {
       	private static int si;
       	private native void accessField();
 	}
 

那么实现为:


  	JNIEXPORT void JNICALL
   	Java_StaticFieldTest_accessField(JNIEnv *env, jobject obj)
   	{
	
       	jfieldID fid;   /* store the field ID */
       	jint si;
       	jclass cls = (*env)->GetObjectClass(env, obj);   //获取类class
       	fid = (*env)->GetStaticFieldID(env, cls, "si", "I");  //获取静态属性id
       	si = (*env)->GetStaticIntField(env, cls, fid);   //读去属性的值
      	(*env)->SetStaticIntField(env, cls, fid, 200);  //设置静态属性的值
   	}
   
   
   
   
   
   
###访问实例方法
假如有个这样的类：

 	class MethodCall {
       	private native void nativeMethod();
       	private void callback() {
           	System.out.println("In Java CallBack");
       	}
       	public static void main(String args[]) {
           	MethodCall c = new MethodCall();
           	c.nativeMethod();
	} static {
           	System.loadLibrary("InstanceMethodCall");
       	}
	}

jni实现:

	JNIEXPORT void JNICALL
   	Java_MethodCall_nativeMethod(JNIEnv *env, jobject obj)
   	{
       	//1.拿到class
       	jclass cls = (*env)->GetObjectClass(env, obj);                         
       	//2.拿到方法id
       	jmethodID mid = (*env)->GetMethodID(env, cls, "callback", "()V");           
        	//3.根据obj,和方法id 调用方法
      	(*env)->CallVoidMethod(env, obj, mid);   
   	}



根据方法的返回值来决定调用哪个方法：
    Call<Type>Method
如果返回int  那么最后一步就调用  `(*env)->CallIntMethod(env,obj,mid)`;


最后那个参数 "()V"   是方法描述符:


>	(I)V   带一个int 类型的参数，返回值类型为void
>	()D     没有参数，返回double   //注意！！没有参数并不是  (V)D

方法public static void main(String[] args) 对应的方法描的符为:

  	([Ljava/lang/String;)V



####访问静态方法

	jclass cls = (*env)->GetObjectClass(env, obj);
	jmethodID mid =
        	   (*env)->GetStaticMethodID(env, cls, "callback", "()V");
	(*env)->CallStaticVoidMethod(env, cls, mid);    //注意，这里跟访问实例方法的区别是 第二个参数不是obj,而是cls
 
   
