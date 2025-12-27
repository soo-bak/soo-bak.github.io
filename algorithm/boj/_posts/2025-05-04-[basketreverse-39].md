---
layout: single
title: "[백준 10811] 바구니 뒤집기 (C#, C++) - soo:bak"
date: "2025-05-04 08:30:00 +0900"
description: 주어진 구간의 바구니 순서를 반복적으로 뒤집어 최종 상태를 구하는 시뮬레이션 문제 백준 10811번 바구니 뒤집기의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10811
  - C#
  - C++
  - 알고리즘
  - 구현
  - 시뮬레이션
keywords: "백준 10811, 백준 10811번, BOJ 10811, basketreverse, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10811번 - 바구니 뒤집기](https://www.acmicpc.net/problem/10811)

## 설명
바구니에 적힌 번호들을 조작하는 작업이 여러 번 주어질 때,

**각 작업마다 지정된 범위의 순서를 '역순'으로 뒤집는 과정을 반복한 후** 모든 작업이 끝났을 때 바구니에 적힌 번호들을 출력하는 문제입니다.

<br>

## 접근법

- 먼저 `바구니의 개수`와 `뒤집는 작업의 횟수`를 입력받습니다.
- 바구니에는 처음에 `1`부터 `N`까지의 번호가 순서대로 적혀 있습니다.
- 각 작업마다 `시작 위치`와 `끝 위치`가 주어지면, <br>
  해당 구간의 바구니 순서를 **역순으로 뒤집는 작업**을 수행합니다.
- 모든 작업이 끝난 뒤, 최종적으로 바구니에 적힌 번호를 순서대로 출력합니다.

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split().Select(int.Parse).ToArray();
    int n = input[0], m = input[1];
    var basket = Enumerable.Range(1, n).ToArray();

    for (int t = 0; t < m; t++) {
      var cmd = Console.ReadLine().Split().Select(int.Parse).ToArray();
      int i = cmd[0] - 1, j = cmd[1] - 1;
      Array.Reverse(basket, i, j - i + 1);
    }

    Console.WriteLine(string.Join(" ", basket));
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  vector<int> basket(n);
  for (int i = 0; i < n; i++)
    basket[i] = i + 1;

  while (m--) {
    int i, j; cin >> i >> j;
    reverse(basket.begin() + i - 1, basket.begin() + j);
  }

  for (int i = 0; i < n; i++)
    cout << basket[i] << (i < n - 1 ? " " : "\n");

  return 0;
}
```
