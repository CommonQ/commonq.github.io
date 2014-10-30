---
published: true
layout: post
title: copy list with random pointer
categories: Algorithm
---

## 拷贝带随机指针的链表

此题关键在于深层拷贝，尤其要注意随机指针的拷贝问题。
代码如下：

```C++

class Solution {
public:
    RandomListNode *copyRandomList(RandomListNode *head) {
	
		if(head==NULL){
			return NULL;
		}

		RandomListNode * copyNode;
		RandomListNode * cur=head;
        
		while(cur!=NULL){
			copyNode= new RandomListNode(cur->label);
			copyNode->next=cur->next;
			cur->next=copyNode;
			cur=copyNode->next;
		}

		cur=head;

		while(cur!=NULL){
			if(cur->random!=NULL){
				cur->next->random=cur->random->next;
			}
			cur=cur->next->next;
		}
		cur=head;
		RandomListNode *phead= new RandomListNode(0);
		RandomListNode* new_list=phead;
		while(cur!=NULL){
			phead->next=cur->next;
			cur->next=cur->next->next;
			phead=phead->next;
			cur=cur->next;
		}
		return new_list->next;
    }
};

```
