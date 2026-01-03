---
layout: single
title: "연결 리스트(Linked List)의 원리와 구현 - soo:bak"
date: "2026-01-03 05:00:00 +0900"
description: 노드와 포인터로 구성된 연결 리스트의 개념, 단일/이중 연결 리스트의 구현, 배열과의 비교를 다룹니다
---

## 연결 리스트란?

**연결 리스트(Linked List)**는 노드(Node)들이 포인터로 연결된 선형 자료구조입니다.

각 노드는 **데이터**와 **다음 노드를 가리키는 포인터**를 포함하며, 이 포인터를 통해 노드들이 순차적으로 연결됩니다.

<br>

배열은 연속된 메모리 공간에 데이터를 저장하지만, 연결 리스트는 메모리 공간이 분산되어 있어도 포인터로 연결할 수 있습니다.

이러한 특성 덕분에 크기를 미리 정할 필요가 없고, 삽입과 삭제가 효율적입니다.

```
[데이터|다음] → [데이터|다음] → [데이터|다음] → NULL
    ↑
   Head
```

---

## 연결 리스트의 종류

연결 리스트는 노드 간 연결 방식에 따라 크게 세 가지로 나뉩니다.

<br>

### 단일 연결 리스트 (Singly Linked List)

각 노드가 다음 노드만 가리킵니다. 가장 기본적인 형태입니다.

```
[A|→] → [B|→] → [C|→] → NULL
```

<br>

### 이중 연결 리스트 (Doubly Linked List)

각 노드가 이전 노드와 다음 노드를 모두 가리킵니다.

양방향 탐색이 가능하고, 이전 노드로의 접근이 $$O(1)$$에 가능합니다.

```
NULL ← [←|A|→] ↔ [←|B|→] ↔ [←|C|→] → NULL
```

<br>

### 원형 연결 리스트 (Circular Linked List)

마지막 노드가 첫 번째 노드를 가리킵니다.

끝에서 처음으로 돌아가는 순환 구조가 필요할 때 사용됩니다.

```
[A|→] → [B|→] → [C|→] ─┐
  ↑                     │
  └─────────────────────┘
```

---

## 단일 연결 리스트 구현

### 노드 구조

```cpp
struct Node {
  int data;
  Node* next;

  Node(int val) : data(val), next(nullptr) {}
};
```

<br>

### 기본 연산 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Node {
  int data;
  Node* next;
  Node(int val) : data(val), next(nullptr) {}
};

class LinkedList {
private:
  Node* head;
  int size;

public:
  LinkedList() : head(nullptr), size(0) {}

  // 맨 앞에 삽입 - O(1)
  void pushFront(int val) {
    Node* newNode = new Node(val);
    newNode->next = head;
    head = newNode;
    size++;
  }

  // 맨 뒤에 삽입 - O(n)
  void pushBack(int val) {
    Node* newNode = new Node(val);
    if (!head) {
      head = newNode;
    } else {
      Node* cur = head;
      while (cur->next) {
        cur = cur->next;
      }
      cur->next = newNode;
    }
    size++;
  }

  // 특정 위치에 삽입 - O(n)
  void insertAt(int idx, int val) {
    if (idx == 0) {
      pushFront(val);
      return;
    }

    Node* cur = head;
    for (int i = 0; i < idx - 1 && cur; i++) {
      cur = cur->next;
    }

    if (cur) {
      Node* newNode = new Node(val);
      newNode->next = cur->next;
      cur->next = newNode;
      size++;
    }
  }

  // 맨 앞 삭제 - O(1)
  void popFront() {
    if (!head) return;
    Node* temp = head;
    head = head->next;
    delete temp;
    size--;
  }

  // 특정 값 삭제 - O(n)
  void remove(int val) {
    if (!head) return;

    if (head->data == val) {
      popFront();
      return;
    }

    Node* cur = head;
    while (cur->next && cur->next->data != val) {
      cur = cur->next;
    }

    if (cur->next) {
      Node* temp = cur->next;
      cur->next = cur->next->next;
      delete temp;
      size--;
    }
  }

  // 값 검색 - O(n)
  bool find(int val) {
    Node* cur = head;
    while (cur) {
      if (cur->data == val) return true;
      cur = cur->next;
    }
    return false;
  }

  // 출력
  void print() {
    Node* cur = head;
    while (cur) {
      cout << cur->data;
      if (cur->next) cout << " -> ";
      cur = cur->next;
    }
    cout << " -> NULL\n";
  }

  int getSize() { return size; }
};

int main() {
  LinkedList list;

  list.pushBack(1);
  list.pushBack(2);
  list.pushBack(3);
  list.print();  // 1 -> 2 -> 3 -> NULL

  list.pushFront(0);
  list.print();  // 0 -> 1 -> 2 -> 3 -> NULL

  list.insertAt(2, 10);
  list.print();  // 0 -> 1 -> 10 -> 2 -> 3 -> NULL

  list.remove(10);
  list.print();  // 0 -> 1 -> 2 -> 3 -> NULL

  return 0;
}
```

---

## 이중 연결 리스트 구현

이중 연결 리스트는 `tail` 포인터를 함께 관리하면 맨 뒤 삽입과 삭제도 $$O(1)$$에 수행할 수 있습니다.

```cpp
struct DNode {
  int data;
  DNode* prev;
  DNode* next;
  DNode(int val) : data(val), prev(nullptr), next(nullptr) {}
};

class DoublyLinkedList {
private:
  DNode* head;
  DNode* tail;
  int size;

public:
  DoublyLinkedList() : head(nullptr), tail(nullptr), size(0) {}

  // 맨 앞에 삽입 - O(1)
  void pushFront(int val) {
    DNode* newNode = new DNode(val);
    if (!head) {
      head = tail = newNode;
    } else {
      newNode->next = head;
      head->prev = newNode;
      head = newNode;
    }
    size++;
  }

  // 맨 뒤에 삽입 - O(1)
  void pushBack(int val) {
    DNode* newNode = new DNode(val);
    if (!tail) {
      head = tail = newNode;
    } else {
      newNode->prev = tail;
      tail->next = newNode;
      tail = newNode;
    }
    size++;
  }

  // 맨 앞 삭제 - O(1)
  void popFront() {
    if (!head) return;
    DNode* temp = head;
    head = head->next;
    if (head) head->prev = nullptr;
    else tail = nullptr;
    delete temp;
    size--;
  }

  // 맨 뒤 삭제 - O(1)
  void popBack() {
    if (!tail) return;
    DNode* temp = tail;
    tail = tail->prev;
    if (tail) tail->next = nullptr;
    else head = nullptr;
    delete temp;
    size--;
  }

  // 역순 출력 - O(n)
  void printReverse() {
    DNode* cur = tail;
    while (cur) {
      cout << cur->data;
      if (cur->prev) cout << " <- ";
      cur = cur->prev;
    }
    cout << "\n";
  }
};
```

---

## 배열과의 비교

배열과 연결 리스트는 각각 장단점이 있어, 상황에 맞게 선택해야 합니다.

<br>

**배열이 적합한 경우**:
- 인덱스를 통한 빠른 접근이 필요할 때 (배열은 $$O(1)$$, 연결 리스트는 $$O(n)$$)
- 크기가 고정되거나 변경이 드문 경우
- 캐시 효율이 중요한 경우 (연속된 메모리 배치)

<br>

**연결 리스트가 적합한 경우**:
- 삽입/삭제가 빈번한 경우 (특히 맨 앞)
- 크기를 미리 알 수 없는 경우
- 중간 위치를 이미 알고 있을 때 삽입/삭제가 필요한 경우

<br>

단일 연결 리스트는 맨 앞 삽입/삭제가 $$O(1)$$이고, 이중 연결 리스트는 맨 앞과 맨 뒤 모두 $$O(1)$$입니다.

다만 인덱스로 특정 위치에 접근하는 것은 배열이 $$O(1)$$인 반면 연결 리스트는 $$O(n)$$이므로, 랜덤 접근이 빈번하다면 배열이 더 적합합니다.

---

## C++ STL의 연결 리스트

C++ STL은 `std::list`(이중 연결 리스트)와 `std::forward_list`(단일 연결 리스트)를 제공합니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  list<int> myList;

  // 삽입
  myList.push_back(1);
  myList.push_back(2);
  myList.push_front(0);

  // 순회
  for (int x : myList) {
    cout << x << " ";  // 0 1 2
  }
  cout << "\n";

  // 삭제
  myList.pop_front();
  myList.pop_back();

  // 중간 삽입
  auto it = myList.begin();
  myList.insert(it, 5);

  return 0;
}
```

> 참고: `std::list`는 양방향 반복자를 제공하고, `std::forward_list`는 단방향 반복자만 제공합니다.

---

## 연결 리스트의 활용

### 리스트 뒤집기

포인터의 방향을 하나씩 바꿔가며 뒤집습니다.

```cpp
Node* reverse(Node* head) {
  Node* prev = nullptr;
  Node* cur = head;

  while (cur) {
    Node* next = cur->next;
    cur->next = prev;
    prev = cur;
    cur = next;
  }

  return prev;
}
```

<br>

### 중간 노드 찾기 (러너 기법)

`slow`는 한 칸씩, `fast`는 두 칸씩 이동하면 `fast`가 끝에 도달했을 때 `slow`는 중간에 위치합니다.

```cpp
Node* findMiddle(Node* head) {
  Node* slow = head;
  Node* fast = head;

  while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
  }

  return slow;
}
```

<br>

### 사이클 탐지

플로이드의 토끼와 거북이 알고리듬을 사용합니다.

`slow`와 `fast`가 같은 지점에서 만나면 사이클이 존재합니다.

```cpp
bool hasCycle(Node* head) {
  Node* slow = head;
  Node* fast = head;

  while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
    if (slow == fast) return true;
  }

  return false;
}
```

> 참고: [플로이드의 토끼와 거북이 알고리듬 - soo:bak](https://soo-bak.github.io/algorithm/theory/floyd-cycle-detection/)

<br>

### 두 정렬된 리스트 병합

병합 정렬의 병합 과정과 동일한 원리입니다.

```cpp
Node* mergeSorted(Node* l1, Node* l2) {
  if (!l1) return l2;
  if (!l2) return l1;

  if (l1->data < l2->data) {
    l1->next = mergeSorted(l1->next, l2);
    return l1;
  } else {
    l2->next = mergeSorted(l1, l2->next);
    return l2;
  }
}
```

> 참고: [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)

---

## 마무리

연결 리스트는 노드와 포인터로 구성된 기본적인 자료구조입니다.

<br>

배열과 달리 메모리가 분산되어 있어 동적인 크기 변경이 자유롭고, 삽입/삭제 연산이 효율적입니다.

다만 인덱스를 통한 랜덤 접근이 불가능하고, 포인터를 저장하기 위한 추가 메모리가 필요합니다.

<br>

연결 리스트는 스택, 큐, 그래프의 인접 리스트 등 다양한 자료구조의 기반이 됩니다.

또한 연결 리스트를 활용한 문제는 면접에서도 자주 출제되므로, 기본 연산과 활용 기법을 익혀두면 도움이 됩니다.

<br>

**관련 글**:
- [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)
- [플로이드의 토끼와 거북이 알고리듬 - soo:bak](https://soo-bak.github.io/algorithm/theory/floyd-cycle-detection/)

<br>

**관련 문제**:
- [[백준 1406] 에디터](https://www.acmicpc.net/problem/1406)
- [[백준 5397] 키로거](https://www.acmicpc.net/problem/5397)
