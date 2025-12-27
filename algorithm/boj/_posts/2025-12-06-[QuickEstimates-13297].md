---
layout: single
title: "[백준 13297] Quick Estimates (C#, C++) - soo:bak"
date: "2025-12-06 21:05:00 +0900"
description: 정수 견적의 자릿수 길이만 출력하는 백준 13297번 Quick Estimates 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 13297
  - C#
  - C++
  - 알고리즘
  - 문자열
keywords: "백준 13297, 백준 13297번, BOJ 13297, QuickEstimates, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[13297번 - Quick Estimates](https://www.acmicpc.net/problem/13297)

## 설명
작업 견적 금액이 문자열로 주어집니다. 값의 범위가 매우 커서 정수로 처리할 수 없습니다.

각 견적에 대해 필요한 자릿수만 출력하는 문제입니다.

<br>

## 접근법
먼저, 정수 범위가 매우 크므로 문자열로 입력을 받습니다.

다음으로, 문자열의 길이가 곧 자릿수이므로 각 견적마다 길이를 구해 바로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      for (var i = 0; i < n; i++) {
        var s = Console.ReadLine()!;
        Console.WriteLine(s.Length);
      }
    }
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

  int n; cin >> n;
  while (n--) {
    string s; cin >> s;
    cout << s.size() << "\n";
  }

  return 0;
}
```
