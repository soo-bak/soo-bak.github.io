---
layout: single
title: "[백준 11005] 진법 변환 2 (C#, C++) - soo:bak"
date: "2025-05-04 09:04:00 +0900"
description: 주어진 10진법 수를 B진법으로 변환하는 과정을 구현하는 백준 11005번 진법 변환 2 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11005
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 11005, 백준 11005번, BOJ 11005, baseconversion2, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11005번 - 진법 변환 2](https://www.acmicpc.net/problem/11005)

## 설명
10진법 수가 주어졌을 때, **주어진 기수 B에 맞추어 B진법으로 변환한 결과를 출력하는 문제**입니다.

<br>

---

## 접근법

10진법 수를 B진법으로 바꾸기 위해서는:

- `N`을 `B`로 나눈 나머지를 구하고, 몫을 다시 나누는 과정을 반복합니다.
- 나머지는 B진법의 **각 자리에 해당하는 값**이며, 이 값들을 **역순으로 나열한 것이 B진법 표현**입니다.
- 숫자 `10` 이상은 알파벳 대문자 `A`부터 순서대로 변환합니다. (`A = 10, B = 11, ..., Z = 35`)

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    int n = int.Parse(input[0]);
    int b = int.Parse(input[1]);
    var sb = new StringBuilder();

    while (n > 0) {
      int r = n % b;
      char c = (char)(r < 10 ? r + '0' : r - 10 + 'A');
      sb.Insert(0, c);
      n /= b;
    }

    Console.WriteLine(sb.ToString());
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef deque<char> dc;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, b; cin >> n >> b;

  dc dq;
  while (n) {
    int r = n % b;
    dq.push_front(r < 10 ? r + '0' : r - 10 + 'A');
    n /= b;
  }

  for (char c : dq)
    cout << c;
  cout << "\n";

  return 0;
}
```
