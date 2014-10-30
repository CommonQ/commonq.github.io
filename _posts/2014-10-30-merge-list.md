---
published: true
layout: post
title: merge_list
categories: Algorithm
---

## 链表之归并有序链表

传入两个Node指针ptr1与ptr2，它们指向的链表中的元素有序递增，将它们合并为一个新的有序链表newptr，注意操作过程中不要额外申请空间.

代码：

```C
Node *merge_list(Node *ptr1,Node *ptr2){

	if(ptr1==NULL&&ptr2==NULL)
		return NULL;
	if(ptr1==NULL&&ptr2!=NULL)
		return ptr2;
	if(ptr2==NULL&&ptr1!=NULL)
		return ptr1;
	Node * base,*other;
	if(ptr1->data>=ptr2->data){
		base=ptr2;
		other=ptr1;
	}else{
		base=ptr1;
		other=ptr2;
	}

	//Node *current = NULL;

	Node *current=base;
	Node * new_ptr=base;
	base=base->next;

	while(base!=NULL&&other!=NULL){
	if(base->data<=other->data){
		current->next=base;
		current=base;
		base=base->next;
	}else{
		current->next=other;
		current=other;
		other=other->next;
	}
	}
	if(other!=NULL){
		current->next=other;
	}else if(base!=NULL){
		current->next=base;
	}
	return new_ptr;

}

```