---
published: true
layout: post
title: 链表的基本操作
categories: Algorithm
---

## 链表的基本操作

链表的基本操作包括创建、销毁、插入、删除、查找、打印。这里附上代码：

####list.h
```C
typedef struct Node {
	int data;
	Node *next;

} PNode;

typedef struct List{

	Node head;
	Node *last;
} List;

void list_init(List *list);
void list_destroy(List *list);
void list_insert(List *list,int data);
void list_erase(List *list,int data);
Node * list_find(List *list,int data);
void list_print(List *list);
int get_list_max(List *list);
int get_list_count(List *list);
int get_list_min(List *list);

```

####list.c

```C

#include "list.h";
#include <stdio.h>;
#include<stdlib.h>;

void list_init(List *list){

	Node node;
	node.data=0;
	node.next=NULL;
	list->head=node;
	list->last=&list->head;


}


void list_insert(List *list,int data){

	Node *node = (Node*)malloc(sizeof(Node));
	node->data=data;
	node->next=NULL;
	list->last->next=node;
	list->last=node;
	
	

}


void list_print(List *list){
	Node * cur =list->head.next;
	printf("head");
	while(cur!=NULL){
		printf("->[%d]",cur->data);
		cur=cur->next;
	}
	printf("\n");

}

void list_print(Node *p){
	while(p!=NULL){
		printf("->[%d]",p->data);
		p=p->next;
	}
}

void list_erase(List *list, int data){
	Node * pre = &list->head;
	Node * cur =list->head.next;

	while(cur!=NULL){
		if(cur->data==data){
			Node *del = cur;
			pre->next=cur->next;
			free(del);
			cur=pre->next;

		}else{
			pre=cur;
			cur=cur->next;

		}


	}


}

Node * list_find(List *list,int data){

	Node *cur = list->head.next;
	while(cur){

		if(cur->data==data){
			return cur;
		}
		cur=cur->next;
	}
	return NULL;

}

int get_list_max(List *list){

	Node *cur = list->head.next;
	int max=0;
	while(cur){

		if(cur->data>=max){
			max=cur->data;
		}
		cur=cur->next;
	}
	return max;
}

int get_list_min(List *list){

	Node *cur = list->head.next;
	int min;
	if(cur)
		min=cur->data;
	while(cur){

		if(cur->data<=min){
			min=cur->data;
		}
		cur=cur->next;
	}
	return min;
}

int get_list_count(List *list){

	Node *cur = list->head.next;
	int count=0;
	
	while(cur){

		
			count+=cur->data;
		
		cur=cur->next;
	}
	return count;

}

void list_destroy(List *list){
	Node * cur = list->head.next;

	while(cur){
	Node * del= cur;
	cur=cur->next;
	free(del);
	}
	list_init(list);
}

```

Enter text in [Markdown](http://daringfireball.net/projects/markdown/). Use the toolbar above, or click the **?** button for formatting help.
