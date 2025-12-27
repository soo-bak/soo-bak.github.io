---
layout: single
title: "[백준 29713] 브실이의 띠부띠부씰 컬렉션 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 29713번 C#, C++ 풀이 - BRONZESILVER를 만들 수 있는 최대 개수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 29713
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 29713, 백준 29713번, BOJ 29713, BbeusilStickerCollection, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[29713번 - 브실이의 띠부띠부씰 컬렉션](https://www.acmicpc.net/problem/29713)

## 설명
모은 알파벳 스티커로 "BRONZESILVER"를 만들 때, 배송받을 수 있는 최대 개수를 구하는 문제입니다.

<br>

## 접근법
알파벳 빈도를 센 뒤, 필요한 글자별 개수로 나눈 몫의 최솟값이 정답입니다.  
필요한 개수는 B(1), R(2), O(1), N(1), Z(1), E(2), S(1), I(1), L(1), V(1)입니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;

    var cnt = new int[26];
    foreach (var ch in s)
      cnt[ch - 'A']++;

    var ans = int.MaxValue;
    ans = Math.Min(ans, cnt['B' - 'A'] / 1);
    ans = Math.Min(ans, cnt['R' - 'A'] / 2);
    ans = Math.Min(ans, cnt['O' - 'A'] / 1);
    ans = Math.Min(ans, cnt['N' - 'A'] / 1);
    ans = Math.Min(ans, cnt['Z' - 'A'] / 1);
    ans = Math.Min(ans, cnt['E' - 'A'] / 2);
    ans = Math.Min(ans, cnt['S' - 'A'] / 1);
    ans = Math.Min(ans, cnt['I' - 'A'] / 1);
    ans = Math.Min(ans, cnt['L' - 'A'] / 1);
    ans = Math.Min(ans, cnt['V' - 'A'] / 1);

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
  string s; cin >> s;

  int cnt[26] = {};
  for (char ch : s) cnt[ch - 'A']++;

  int ans = 1e9;
  ans = min(ans, cnt['B' - 'A'] / 1);
  ans = min(ans, cnt['R' - 'A'] / 2);
  ans = min(ans, cnt['O' - 'A'] / 1);
  ans = min(ans, cnt['N' - 'A'] / 1);
  ans = min(ans, cnt['Z' - 'A'] / 1);
  ans = min(ans, cnt['E' - 'A'] / 2);
  ans = min(ans, cnt['S' - 'A'] / 1);
  ans = min(ans, cnt['I' - 'A'] / 1);
  ans = min(ans, cnt['L' - 'A'] / 1);
  ans = min(ans, cnt['V' - 'A'] / 1);

  cout << ans << "\n";

  return 0;
}
```
