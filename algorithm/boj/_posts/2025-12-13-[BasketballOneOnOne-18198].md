---
layout: single
title: "[백준 18198] Basketball One-on-One (C#, C++) - soo:bak"
date: "2025-12-13 13:02:00 +0900"
description: 점수 기록 문자열을 순서대로 누적해 최종 득점이 높은 쪽을 출력하는 백준 18198번 Basketball One-on-One 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 18198
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 18198, 백준 18198번, BOJ 18198, BasketballOneOnOne, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18198번 - Basketball One-on-One](https://www.acmicpc.net/problem/18198)

## 설명
농구 1대1 경기 기록을 보고 최종 승자를 구하는 문제입니다.

<br>

## 접근법
기록 문자열은 두 글자씩 선수와 득점을 나타냅니다.

문자열을 순회하며 A와 B의 점수를 각각 누적합니다.

최종적으로 더 높은 점수를 가진 선수를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var a = 0; var b = 0;
    for (var i = 0; i < s.Length; i += 2) {
      var val = s[i + 1] - '0';
      if (s[i] == 'A') a += val;
      else b += val;
    }
    Console.WriteLine(a > b ? "A" : "B");
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

  string s;
  if (!(cin >> s)) return 0;
  int a = 0, b = 0;
  for (size_t i = 0; i + 1 < s.size(); i += 2) {
    int val = s[i + 1] - '0';
    if (s[i] == 'A') a += val;
    else b += val;
  }
  cout << (a > b ? 'A' : 'B') << "\n";

  return 0;
}
```
