---
published: true
layout: post
title: 根据深度优先算法(DFS)和标记数组求全排列
categories: Algorithm
---

## 根据深度优先算法(DFS)和标记数组求全排列

####问题描述：
输入正整数n，输出所有形如abcd/efg = n的表达式，其中a~g恰好为数字1~7的一个排列

####输入格式
首先是一个整数t，代表测试数据的组数，每组测试数据包括一个整数n，且1<=n<=100

####输出格式
输出全部满足要求的结果（任意顺序），如果没有满足要求的，输出"NULL"

####解答
对输入的7个数字进行全排列，再对排列后的数字进行4、3的拆分并对其取模，若能整除且结果等于输入，则输出答案。此题的关键在于如何去遍历数字的全排列，在这里我用DFS遍历。

```C

#include<stdio.h>
#include<stdlib.h>
#define GET_ARRAY_LEN(array,len){len = (sizeof(array) / sizeof(array[0]));}
int visit[10]={0};
int numbers[7]={1,2,3,4,5,6,7};
int result[7]={0};
int lengths=6;
int input;
int is_find=0;

 
void dfs(int depth){
     
    int i;
    for(i=0;i<7;i++){
        if(visit[i]==0){
            visit[i]=1;
             
            result[depth]=numbers[i];
 
            if(depth==lengths){
 
                int before=result[0]*1000+result[1]*100+result[2]*10+result[3]*1;
                int after=result[4]*100+result[5]*10+result[6]*1;
 
                if(before%after==0){
                    if(before/after==input){
                        printf("%d/%d=%d\n",before,after,input);
                        is_find=1;
                    }
                }
 
            }else{
                dfs(depth+1);
            }
            visit[i]=0;
        }
    } 
}

 
int main(void){
     
    int loop;
    scanf("%d",&loop);
    int m;
    for(m=0;m<loop;m++){
        scanf("%d",&input);
        is_find=0;
        dfs(0);
        if(is_find==0)
            printf("NULL\n");
    }
}

```
