---
layout: single
title: "[백준 31608] ハミング距離 (Hamming Distance) (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 31608번 C#, C++ 풀이 - 길이 N인 두 문자열의 같은 위치 문자가 다른 개수를 세는 문제"
tags:
  - 백준
  - BOJ
  - 31608
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 31608, 백준 31608번, BOJ 31608, HammingDistance, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31608번 - ハミング距離 (Hamming Distance)](https://www.acmicpc.net/problem/31608)

## 설명
두 문자열의 같은 위치 문자가 서로 다른 위치의 개수를 출력하는 문제입니다.

<br>

## 접근법
두 문자열을 입력받고 0부터 N-1까지 순회하며 문자가 다르면 카운트를 증가시킵니다. 최종 카운트를 출력하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;
    var t = Console.ReadLine()!;

    var cnt = 0;
    for (var i = 0; i < n; i++) {
      if (s[i] != t[i]) cnt++;
    }

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

  int n; cin >> n;
  string s, t;
  cin >> s >> t;

  int cnt = 0;
  for (int i = 0; i < n; i++) {
    if (s[i] != t[i]) cnt++;
  }

  cout << cnt << "\n";

  return 0;
}
```
