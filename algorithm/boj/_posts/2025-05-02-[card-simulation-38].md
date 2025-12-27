---
layout: single
title: "[백준 2161] 카드1 (C#, C++) - soo:bak"
date: "2025-05-02 19:20:00 +0900"
description: 덱 자료구조를 이용해 카드 버리기와 이동을 시뮬레이션하는 백준 2161번 카드1 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2161
  - C#
  - C++
  - 알고리즘
  - 구현
  - 자료구조
  - 큐
keywords: "백준 2161, 백준 2161번, BOJ 2161, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2161번 - 카드1](https://www.acmicpc.net/problem/2161)

## 설명
`1`부터 `N`까지 번호가 붙은 카드가 한 줄로 쌓여 있을 때,

다음의 과정을 반복하여 카드가 한 장만 남을 때까지 시뮬레이션하는 문제입니다.

1. 제일 위의 카드를 버린다.
2. 그 다음 제일 위의 카드를 맨 아래로 옮긴다.

<br>
이 과정을 반복하며 `버린 카드의 순서`를 출력하고, `마지막에 남은 카드의 번호`도 함께 출력해야 합니다.

<br>

## 접근법

- `덱(Deque)`을 사용해 효율적인 앞/뒤 삽입/삭제를 처리합니다.
- 처음엔 `1`부터 `N`까지의 수를 덱의 앞에서부터 삽입합니다.
- 반복문을 통해:
  - 덱의 맨 뒤(위쪽)의 카드를 출력하고 제거합니다.
  - 그 다음 카드도 뒤에서 꺼내 앞쪽으로 이동시킵니다.
- 덱에 카드가 하나 남을 때까지 반복합니다.

<br>

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var dq = new LinkedList<int>();
    for (int i = 1; i <= n; i++)
      dq.AddLast(i);

    while (dq.Count > 1) {
      Console.Write(dq.First.Value + " ");
      dq.RemoveFirst();
      dq.AddLast(dq.First.Value);
      dq.RemoveFirst();
    }

    Console.WriteLine(dq.First.Value);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef deque<int> di;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  di dq;
  for (int i = 1; i <= n; i++)
    dq.push_front(i);

  while (dq.size() > 1) {
    cout << dq.back() << " ";
    dq.pop_back();
    dq.push_front(dq.back());
    dq.pop_back();
  }

  cout << dq.front() << "\n";

  return 0;
}
```
