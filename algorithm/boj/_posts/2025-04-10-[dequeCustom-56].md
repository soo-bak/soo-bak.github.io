---
layout: single
title: "[백준 10866] 덱 (C#, C++) - soo:bak"
date: "2025-04-10 15:41:00 +0900"
description: 구현 문제에서 직접 덱 구조를 만들어 처리하는 백준 10866번 덱 문제의 C# 및 C++ 풀이와 상세한 설명
---

## 문제 링크
[10866번 - 덱](https://www.acmicpc.net/problem/10866)

## 설명
자료구조들 중 `deque`를 흉내 내는 방식으로 **직접 덱 구조를 구현**하고, 문제에서 주어진 명령을 처리하는 문제입니다.
큐(Queue)와 스택(Stack)을 결합한 자료구조인 **덱(Deque)** 은 **양방향에서 삽입과 삭제가 가능한 선형 자료구조**입니다.

### 구현 포인트
- 덱의 양 끝에서 삽입/삭제가 가능해야 하므로, 배열의 중앙을 기준으로 `head`, `tail` 포인터를 사용합니다.
- 정수의 개수가 많아질 수 있으므로, 충분히 큰 배열을 선언하여 좌우 양방향 이동을 처리합니다.
- 모든 명령어는 문자열로 주어지므로, 조건에 맞게 로직을 분기해야 합니다.

### 시간 복잡도
- 각 연산은 **O(1)**에 수행됩니다.
- 전체 명령 수 `n`이 최대 `10,000`개이므로 총 수행 시간은 **O(n)**으로 충분합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System.Text;

namespace Solution {
  class Program {
    const int MAX = 20_001;
    static int[] dq = new int[MAX];
    static int head = MAX / 2;
    static int tail = MAX / 2;

    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var sb = new StringBuilder();

      while (n-- > 0) {
        var input = Console.ReadLine()!.Split();
        var cmd = input[0];

        if (cmd == "push_front") {
          var x = int.Parse(input[1]);
          dq[--head] = x;
        } else if (cmd == "push_back") {
          var x = int.Parse(input[1]);
          dq[tail++] = x;
        } else if (cmd == "pop_front") {
          sb.AppendLine(head == tail ? "-1" : dq[head++].ToString());
        } else if (cmd == "pop_back") {
          sb.AppendLine(head == tail ? "-1" : dq[--tail].ToString());
        } else if (cmd == "size") {
          sb.AppendLine((tail - head).ToString());
        } else if (cmd == "empty") {
          sb.AppendLine(head == tail ? "1" : "0");
        } else if (cmd == "front") {
          sb.AppendLine(head == tail ? "-1" : dq[head].ToString());
        } else if (cmd == "back") {
          sb.AppendLine(head == tail ? "-1" : dq[tail - 1].ToString());
        }
      }

      Console.Write(sb.ToString());
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>
#define MAX 20'001

using namespace std;

class MyDeque {
  int data[MAX];
  int head, tail;

public:
  MyDeque() {
    head = tail = MAX / 2;
  }

  void push_front(int value) {
    data[--head] = value;
  }

  void push_back(int value) {
    data[tail++] = value;
  }

  int pop_front() {
    if (empty()) return -1;
    return data[head++];
  }

  int pop_back() {
    if (empty()) return -1;
    return data[--tail];
  }

  int size() const {
    return tail - head;
  }

  int empty() const {
    return head == tail ? 1 : 0;
  }

  int front() const {
    if (empty()) return -1;
    return data[head];
  }

  int back() const {
    if (empty()) return -1;
    return data[tail - 1];
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  MyDeque dq;
  while (n--) {
    string cmd; cin >> cmd;

    if (cmd == "push_front") {
      int x; cin >> x;
      dq.push_front(x);
    }
    else if (cmd == "push_back") {
      int x; cin >> x;
      dq.push_back(x);
    }
    else if (cmd == "pop_front") {
      cout << dq.pop_front() << "\n";
    }
    else if (cmd == "pop_back") {
      cout << dq.pop_back() << "\n";
    }
    else if (cmd == "size") {
      cout << dq.size() << "\n";
    }
    else if (cmd == "empty") {
      cout << dq.empty() << "\n";
    }
    else if (cmd == "front") {
      cout << dq.front() << "\n";
    }
    else if (cmd == "back") {
      cout << dq.back() << "\n";
    }
  }

  return 0;
}
```
