---
layout: single
title: "[백준 17903] Counting Clauses (C#, C++) - soo:bak"
date: "2025-12-13 13:02:00 +0900"
description: 절 수가 8 이상이면 satisfactory, 미만이면 unsatisfactory를 출력하는 백준 17903번 Counting Clauses 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17903
  - C#
  - C++
  - 알고리즘
keywords: "백준 17903, 백준 17903번, BOJ 17903, CountingClauses, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17903번 - Counting Clauses](https://www.acmicpc.net/problem/17903)

## 설명
절의 수에 따라 satisfactory 또는 unsatisfactory를 판단하는 문제입니다.

<br>

## 접근법
절의 수가 8 이상이면 satisfactory, 미만이면 unsatisfactory를 출력합니다.

실제 리터럴 내용은 결과에 영향을 주지 않으므로 첫 줄만 읽으면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
    var m = line[0];
    Console.WriteLine(m >= 8 ? "satisfactory" : "unsatisfactory");
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

  int m, n;
  if (!(cin >> m >> n)) return 0;
  cout << (m >= 8 ? "satisfactory" : "unsatisfactory") << "\n";

  return 0;
}
```
```
