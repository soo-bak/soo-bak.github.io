---
layout: single
title: "[백준 9443] Arrangement of Contest (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: "백준 9443번 C#, C++ 풀이 - 제목의 첫 글자가 A, B, C...로 이어지는 최대 길이를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 9443
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 9443, 백준 9443번, BOJ 9443, ArrangementOfContest, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9443번 - Arrangement of Contest](https://www.acmicpc.net/problem/9443)

## 설명
문제 제목들의 첫 글자를 이용해 A부터 연속으로 몇 개의 문제를 만들 수 있는지 구하는 문제입니다.

<br>

## 접근법
각 제목의 첫 글자가 어떤 알파벳인지 표시해둡니다.

이후, A부터 시작해서 연속으로 존재하는 알파벳의 개수를 세어 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var seen = new bool[26];
    for (var i = 0; i < n; i++) {
      var s = Console.ReadLine()!;
      var idx = s[0] - 'A';
      if (idx >= 0 && idx < 26) seen[idx] = true;
    }

    var ans = 0;
    while (ans < 26 && seen[ans])
      ans++;
    Console.WriteLine(ans);
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
  bool seen[26] = {0, };
  for (int i = 0; i < n; i++) {
    string s; cin >> s;
    int idx = s[0] - 'A';
    if (0 <= idx && idx < 26) seen[idx] = true;
  }

  int ans = 0;
  while (ans < 26 && seen[ans])
    ans++;
  cout << ans << "\n";

  return 0;
}
```
