---
layout: single
title: "[백준 14909] 양수 개수 세기 (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 한 줄에 주어진 정수들 중 양수의 개수를 세는 백준 14909번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 14909
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 14909, 백준 14909번, BOJ 14909, CountPositives, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14909번 - 양수 개수 세기](https://www.acmicpc.net/problem/14909)

## 설명
주어진 정수들 중 양수의 개수를 세는 문제입니다.

<br>

## 접근법
입력 라인을 공백으로 분리하여 각 숫자를 확인합니다.

0보다 큰 경우만 카운트하여 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var tokens = Console.ReadLine()!.Split(' ', StringSplitOptions.RemoveEmptyEntries);
    var cnt = 0;
    foreach (var s in tokens)
      if (int.Parse(s) > 0) cnt++;
    Console.WriteLine(cnt);
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

  int x, cnt = 0;
  while (cin >> x)
    if (x > 0) cnt++;
  cout << cnt << "\n";

  return 0;
}
```
