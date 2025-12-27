---
layout: single
title: "스택과 큐 - 기본 자료구조의 원리 - soo:bak"
date: "2025-12-27 01:30:00 +0900"
description: 스택의 LIFO 원리와 큐의 FIFO 원리, 각각의 구현 방법과 활용 예시를 통해 기본 자료구조를 설명합니다.
---

## 스택(Stack)이란?

**스택(Stack)** 은 **LIFO(Last In, First Out)** 원리를 따르는 자료구조입니다.

<br>
가장 나중에 들어온 데이터가 가장 먼저 나갑니다.

<br>
접시를 쌓아 올리는 것을 생각하면 됩니다.

새 접시는 맨 위에 올리고, 꺼낼 때도 맨 위에서 꺼냅니다.

<br>

---

<br>

## 스택의 기본 연산

### push

스택의 맨 위에 데이터를 추가합니다.

시간 복잡도: **O(1)**

<br>

### pop

스택의 맨 위 데이터를 제거하고 반환합니다.

시간 복잡도: **O(1)**

<br>

### top (peek)

스택의 맨 위 데이터를 제거하지 않고 확인합니다.

시간 복잡도: **O(1)**

<br>

### empty

스택이 비어있는지 확인합니다.

시간 복잡도: **O(1)**

<br>

---

<br>

## 스택의 동작 예시

```
push(1): [1]
push(2): [1, 2]
push(3): [1, 2, 3]
top():   3 반환
pop():   3 반환, [1, 2]
pop():   2 반환, [1]
push(4): [1, 4]
```

<br>

---

<br>

## 스택 구현 (C++)

### STL stack 사용

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    stack<int> st;

    st.push(1);
    st.push(2);
    st.push(3);

    cout << st.top() << "\n";  // 3
    st.pop();
    cout << st.top() << "\n";  // 2

    while (!st.empty()) {
        cout << st.top() << " ";
        st.pop();
    }
    // 출력: 2 1

    return 0;
}
```

<br>

### 배열로 직접 구현

```cpp
class Stack {
private:
    int arr[10000];
    int topIdx = -1;

public:
    void push(int x) {
        arr[++topIdx] = x;
    }

    int pop() {
        return arr[topIdx--];
    }

    int top() {
        return arr[topIdx];
    }

    bool empty() {
        return topIdx == -1;
    }
};
```

<br>

---

<br>

## 큐(Queue)란?

**큐(Queue)** 는 **FIFO(First In, First Out)** 원리를 따르는 자료구조입니다.

<br>
가장 먼저 들어온 데이터가 가장 먼저 나갑니다.

<br>
은행 대기줄을 생각하면 됩니다.

먼저 온 사람이 먼저 서비스를 받습니다.

<br>

---

<br>

## 큐의 기본 연산

### push (enqueue)

큐의 뒤쪽에 데이터를 추가합니다.

시간 복잡도: **O(1)**

<br>

### pop (dequeue)

큐의 앞쪽 데이터를 제거하고 반환합니다.

시간 복잡도: **O(1)**

<br>

### front

큐의 맨 앞 데이터를 확인합니다.

시간 복잡도: **O(1)**

<br>

### back

큐의 맨 뒤 데이터를 확인합니다.

시간 복잡도: **O(1)**

<br>

---

<br>

## 큐의 동작 예시

```
push(1): [1]
push(2): [1, 2]
push(3): [1, 2, 3]
front(): 1 반환
pop():   1 반환, [2, 3]
pop():   2 반환, [3]
push(4): [3, 4]
```

<br>

---

<br>

## 큐 구현 (C++)

### STL queue 사용

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    queue<int> q;

    q.push(1);
    q.push(2);
    q.push(3);

    cout << q.front() << "\n";  // 1
    q.pop();
    cout << q.front() << "\n";  // 2

    while (!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    // 출력: 2 3

    return 0;
}
```

<br>

---

<br>

## 덱(Deque)

**덱(Deque, Double-Ended Queue)** 은 양쪽 끝에서 삽입과 삭제가 가능한 자료구조입니다.

<br>
스택과 큐의 기능을 모두 가지고 있습니다.

<br>

### 덱의 연산

- `push_front`: 앞에 삽입
- `push_back`: 뒤에 삽입
- `pop_front`: 앞에서 제거
- `pop_back`: 뒤에서 제거

<br>
모든 연산이 **O(1)** 에 수행됩니다.

<br>

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    deque<int> dq;

    dq.push_back(1);   // [1]
    dq.push_front(2);  // [2, 1]
    dq.push_back(3);   // [2, 1, 3]

    cout << dq.front() << "\n";  // 2
    cout << dq.back() << "\n";   // 3

    dq.pop_front();  // [1, 3]
    dq.pop_back();   // [1]

    return 0;
}
```

<br>

---

<br>

## 스택과 큐의 활용

### 스택 활용 예시

- **괄호 검사**: 여는 괄호는 push, 닫는 괄호는 pop하여 짝 확인
- **후위 표기식 계산**: 피연산자는 push, 연산자는 pop하여 계산
- **DFS (깊이 우선 탐색)**: 방문할 노드를 스택에 저장
- **함수 호출 스택**: 재귀 호출 시 호출 정보 저장
- **뒤로 가기**: 브라우저 히스토리 관리

<br>

### 큐 활용 예시

- **BFS (너비 우선 탐색)**: 방문할 노드를 큐에 저장
- **작업 스케줄링**: 먼저 들어온 작업을 먼저 처리
- **버퍼**: 데이터를 순서대로 처리
- **프린터 대기열**: 먼저 요청한 문서를 먼저 출력

<br>

---

<br>

## 스택으로 괄호 검사하기

```cpp
#include <bits/stdc++.h>
using namespace std;

bool isValidParentheses(string s) {
    stack<char> st;

    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push(c);
        } else {
            if (st.empty()) return false;
            char top = st.top();
            st.pop();
            if (c == ')' && top != '(') return false;
            if (c == ']' && top != '[') return false;
            if (c == '}' && top != '{') return false;
        }
    }

    return st.empty();
}
```

<br>

---

<br>

## 관련 문제 유형

스택과 큐는 다음과 같은 문제에서 활용됩니다:

- 괄호 유효성 검사
- 후위 표기식 변환 및 계산
- 히스토그램에서 가장 큰 직사각형
- 슬라이딩 윈도우 최댓값 (덱 활용)
- BFS / DFS 구현
- 요세푸스 문제

<br>

