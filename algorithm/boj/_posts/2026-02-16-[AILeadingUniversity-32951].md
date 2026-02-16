---
layout: single
title: "[백준 32951] AI 선도대학 (C#, C++) - soo:bak"
date: "2026-02-16 21:03:00 +0900"
description: "백준 32951번 C#, C++ 풀이 - 2024년으로부터 N년까지 지난 연수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 32951
  - C#
  - C++
  - 알고리즘
  - 구현
  - 사칙연산
keywords: "백준 32951, 백준 32951번, BOJ 32951, AI 선도대학, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32951번 - AI 선도대학](https://www.acmicpc.net/problem/32951)

## 설명
연도 N이 주어질 때 2024년을 기준으로 몇 년이 지났는지 구하는 문제입니다.

<br>

## 접근법
정답은 `N - 2024`입니다. 입력을 읽어 바로 뺄셈 결과를 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    Console.WriteLine(n - 2024);
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
  cout << (n - 2024) << "\n";

  return 0;
}
```
