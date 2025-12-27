---
layout: single
title: "[백준 25630] 팰린드롬 소떡소떡 (C#, C++) - soo:bak"
date: "2025-12-13 22:20:00 +0900"
description: 양끝에서 비교해 다른 쌍의 개수를 세면 필요한 최소 변환 횟수가 되는 백준 25630번 팰린드롬 소떡소떡 문제의 C#/C++ 풀이
tags:
  - 백준
  - BOJ
  - 25630
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 25630, 백준 25630번, BOJ 25630, PalindromeSotteok, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25630번 - 팰린드롬 소떡소떡](https://www.acmicpc.net/problem/25630)

## 설명
문자열을 팰린드롬으로 만들기 위한 최소 변환 횟수를 구하는 문제입니다.

<br>

## 접근법
양끝에서 대칭되는 위치의 문자를 비교합니다.

서로 다른 쌍마다 한 번의 변환이 필요하므로, 다른 쌍의 개수가 답입니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;
    var diff = 0;
    for (var i = 0; i < n / 2; i++) {
      if (s[i] != s[n - 1 - i]) diff++;
    }
    Console.WriteLine(diff);
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
  string s; cin >> s;
  int diff = 0;
  for (int i = 0; i < n / 2; i++) {
    if (s[i] != s[n - 1 - i]) ++diff;
  }
  cout << diff << "\n";

  return 0;
}
```
