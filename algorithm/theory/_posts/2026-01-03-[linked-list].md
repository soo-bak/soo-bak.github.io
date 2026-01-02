---
layout: single
title: "연결 리스트(Linked List)의 원리와 구현 - soo:bak"
date: "2026-01-03 05:00:00 +0900"
description: 노드와 포인터로 구성된 연결 리스트의 개념, 단일/이중 연결 리스트의 구현, 배열과의 비교를 다룹니다
---

## 연결 리스트란?

**연결 리스트(Linked List)**는 노드(Node)들이 포인터로 연결된 선형 자료구조입니다.

각 노드는 **데이터**와 **다음 노드를 가리키는 포인터**를 포함합니다.

<br>

**연결 리스트 구조**

```
[데이터|다음] → [데이터|다음] → [데이터|다음] → NULL
    ↑
   Head
```

<br>

**배열과의 차이점**:
- 배열: 연속된 메모리 공간, 고정 크기
- 연결 리스트: 분산된 메모리 공간, 동적 크기

<br>

## 연결 리스트의 종류

<br>

### 1. 단일 연결 리스트 (Singly Linked List)

각 노드가 다음 노드만 가리킵니다.

```
[A|→] → [B|→] → [C|→] → NULL
```

<br>

### 2. 이중 연결 리스트 (Doubly Linked List)

각 노드가 이전 노드와 다음 노드를 모두 가리킵니다.

```
NULL ← [←|A|→] ↔ [←|B|→] ↔ [←|C|→] → NULL
```

<br>

### 3. 원형 연결 리스트 (Circular Linked List)

마지막 노드가 첫 번째 노드를 가리킵니다.

```
[A|→] → [B|→] → [C|→] ─┐
  ↑                     │
  └─────────────────────┘
```

<br>

## 단일 연결 리스트 구현

<br>

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
      if (cur->next) cout << " → ";
      cur = cur->next;
    }
    cout << " → NULL\n";
  }

  int getSize() { return size; }
};

int main() {
  LinkedList list;

  list.pushBack(1);
  list.pushBack(2);
  list.pushBack(3);
  list.print();  // 1 → 2 → 3 → NULL

  list.pushFront(0);
  list.print();  // 0 → 1 → 2 → 3 → NULL

  list.insertAt(2, 10);
  list.print();  // 0 → 1 → 10 → 2 → 3 → NULL

  list.remove(10);
  list.print();  // 0 → 1 → 2 → 3 → NULL

  return 0;
}
```

<br>

## 이중 연결 리스트 구현

이중 연결 리스트는 양방향 탐색과 효율적인 삭제가 가능합니다.

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
      if (cur->prev) cout << " ← ";
      cur = cur->prev;
    }
    cout << "\n";
  }
};
```

<br>

## 시간 복잡도 비교

<br>

| 연산 | 배열 | 단일 연결 리스트 | 이중 연결 리스트 |
|------|------|----------------|----------------|
| 맨 앞 삽입 | $$O(n)$$ | $$O(1)$$ | $$O(1)$$ |
| 맨 뒤 삽입 | $$O(1)$$ | $$O(n)$$ | $$O(1)$$ |
| 중간 삽입 | $$O(n)$$ | $$O(n)$$ | $$O(n)$$ |
| 맨 앞 삭제 | $$O(n)$$ | $$O(1)$$ | $$O(1)$$ |
| 맨 뒤 삭제 | $$O(1)$$ | $$O(n)$$ | $$O(1)$$ |
| 인덱스 접근 | $$O(1)$$ | $$O(n)$$ | $$O(n)$$ |
| 검색 | $$O(n)$$ | $$O(n)$$ | $$O(n)$$ |

<br>

## 연결 리스트 vs 배열

<br>

| 특성 | 배열 | 연결 리스트 |
|------|------|------------|
| 메모리 배치 | 연속 | 분산 |
| 크기 변경 | 비용 높음 | 비용 낮음 |
| 랜덤 접근 | $$O(1)$$ | $$O(n)$$ |
| 삽입/삭제 (중간) | $$O(n)$$ | $$O(1)$$ (위치 알면) |
| 메모리 효율 | 좋음 | 포인터 오버헤드 |
| 캐시 효율 | 좋음 | 나쁨 |

<br>

**배열이 적합한 경우**:
- 인덱스를 통한 빠른 접근이 필요할 때
- 크기가 고정되거나 변경이 드문 경우
- 캐시 효율이 중요한 경우

<br>

**연결 리스트가 적합한 경우**:
- 삽입/삭제가 빈번한 경우
- 크기를 미리 알 수 없는 경우
- 맨 앞/뒤 삽입 삭제가 주로 발생하는 경우

<br>

## C++ STL의 연결 리스트

C++ STL은 `list`(이중 연결 리스트)와 `forward_list`(단일 연결 리스트)를 제공합니다.

<br>

### std::list 사용

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

<br>

## 연결 리스트의 활용

<br>

**1. 리스트 뒤집기**

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

**2. 중간 노드 찾기 (러너 기법)**

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

**3. 사이클 탐지**

[플로이드의 토끼와 거북이 알고리듬](https://soo-bak.github.io/algorithm/theory/floyd-cycle-detection/)을 사용합니다.

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

<br>

**4. 두 정렬된 리스트 병합**

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

<br>

## 마무리

연결 리스트는 삽입과 삭제가 빈번한 상황에서 효율적인 자료구조입니다.

<br>

**핵심 포인트**
- **노드 구조**: 데이터와 포인터로 구성
- **종류**: 단일, 이중, 원형 연결 리스트
- **장점**: 동적 크기, 효율적인 삽입/삭제
- **단점**: 랜덤 접근 불가, 포인터 오버헤드

<br>

연결 리스트는 스택, 큐, 그래프 인접 리스트 등 다양한 자료구조의 기반이 되며, 면접에서도 자주 출제되는 중요한 주제입니다.

<br>

### 관련 글
- [스택과 큐(Stack and Queue)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/stack-queue/)
- [플로이드의 토끼와 거북이 알고리듬 - soo:bak](https://soo-bak.github.io/algorithm/theory/floyd-cycle-detection/)

<br>

### 관련 문제
- [[백준 1406] 에디터](https://www.acmicpc.net/problem/1406)

