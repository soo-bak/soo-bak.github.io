---
layout: single
title: "[백준 23544] Kinder Surprise (C#, C++) - soo:bak"
date: "2026-01-24 22:22:00 +0900"
description: "백준 23544번 C#, C++ 풀이 - n종 수집품 중 중복이 있을 때 아직 모으지 못한 개수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 23544
  - C#
  - C++
  - 알고리즘
  - 구현
  - 해시
keywords: "백준 23544, 백준 23544번, BOJ 23544, Kinder Surprise, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23544번 - Kinder Surprise](https://www.acmicpc.net/problem/23544)

## 설명
총 n종의 하마 피규어가 있으며, n개의 달걀에서 얻은 피규어 설명이 주어집니다.

중복이 있을 때 아직 모으지 못한 피규어의 개수, 즉 n - (서로 다른 설명의 수)를 구하는 문제입니다.

<br>

## 접근법
문자열을 해시셋에 넣어 서로 다른 설명의 개수를 세면 됩니다.

최종 답은 n - distinct입니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var set = new HashSet<string>();
    for (var i = 0; i < n; i++)
      set.Add(Console.ReadLine()!);
    Console.WriteLine(n - set.Count);
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

  int n; 
  cin >> n;
  unordered_set<string> s;
  s.reserve(n * 2);
  string str;
  for (int i = 0; i < n; i++) {
    cin >> str;
    s.insert(str);
  }
  cout << n - (int)s.size() << "\n";

  return 0;
}
```
