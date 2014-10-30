---
published: true
layout: post
title: reverse_list
categories: Algorithm
---

## 链表之逆转链表

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
