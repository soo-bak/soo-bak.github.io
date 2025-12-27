---
layout: single
title: "[백준 32384] 사랑은 고려대입니다 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 32384번 C#, C++ 풀이 - 문장을 N번 공백으로 구분해 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 32384
  - C#
  - C++
  - 알고리즘
keywords: "백준 32384, 백준 32384번, BOJ 32384, LoveIsKoreaUniversity, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32384번 - 사랑은 고려대입니다](https://www.acmicpc.net/problem/32384)

## 설명
지정된 문구를 N번 공백으로 구분해 출력하는 문제입니다.

<br>

## 접근법
지정된 문구를 N번 반복합니다.

각 문구 사이에 공백을 넣어 이어 출력하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = "LoveisKoreaUniversity";
    for (var i = 0; i < n; i++) {
      if (i > 0) Console.Write(" ");
      Console.Write(s);
    }
    Console.WriteLine();
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
  string s = "LoveisKoreaUniversity";
  for (int i = 0; i < n; i++) {
    if (i) cout << " ";
    cout << s;
  }
  cout << "\n";

  return 0;
}
```
