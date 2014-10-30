---
published: true
layout: post
title: 链表之逆转链表
categories: Algorithm
---

## 链表之逆转链表

传入一个Node指针，将它指向的链表进行逆置，返回逆置后的新链表，注意操作过程中不要额外申请空间，即在传入的链表中进行节点逆置.
  
代码：

```C
Node * reverse_list(Node *head){

	Node * pre=NULL;
	Node * cur=head;
	while(cur!=NULL){
		Node * back = cur->next;
		cur->next=pre;
		pre=cur;
		cur=back;
	}
	return pre;

}

```
