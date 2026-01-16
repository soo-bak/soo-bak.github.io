---
layout: single
title: "[백준 17795] Ballpark Estimate (C#, C++) - soo:bak"
date: "2026-01-16 21:30:00 +0900"
description: "백준 17795번 C#, C++ 풀이 - 주어진 수를 가장 가까운 한 자리 유효숫자 형태로 반올림해 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 17795
  - C#
  - C++
  - 알고리즘
  - 구현
  - 수학
keywords: "백준 17795, 백준 17795번, BOJ 17795, Ballpark Estimate, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17795번 - Ballpark Estimate](https://www.acmicpc.net/problem/17795)

## 설명
주어진 수를 첫 자릿수만 남기고 나머지를 0으로 만든 형태로 반올림하는 문제입니다.

예를 들어 745는 700 또는 800 중 더 가까운 값으로 반올림됩니다. 거리가 같으면 더 큰 값을 선택합니다.

## 접근법
먼저 n을 문자열로 읽어 길이와 첫 자릿수를 확인합니다. 길이가 1이면 그대로 출력합니다.

다음으로 첫 자릿수만 남긴 값과 올림한 값을 두 후보로 만듭니다. 예를 들어 745라면 700과 800만 비교하면 됩니다.

이후 두 후보와 n의 차이를 비교해 더 가까운 값을 고릅니다. 거리가 같으면 더 큰 후보를 선택합니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var len = s.Length;
    if (len == 1) {
      Console.WriteLine(s);
      return;
    }

    var n = long.Parse(s);
    var d = s[0] - '0';
    var pow = 1L;
    for (var i = 1; i < len; i++)
      pow *= 10L;

    var c1 = (long)d * pow;
    var c2 = d == 9 ? pow * 10L : (long)(d + 1) * pow;

    var diff1 = n > c1 ? n - c1 : c1 - n;
    var diff2 = n > c2 ? n - c2 : c2 - n;

    var ans = (diff2 < diff1 || diff1 == diff2) ? c2 : c1;
    Console.WriteLine(ans);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s; cin >> s;
  int l = (int)s.size();
  if (l == 1) {
    cout << s << "\n";
    return 0;
  }

  ll n = 0;
  for (char c : s)
    n = n * 10 + (c - '0');

  int d = s[0] - '0';
  ll pow = 1;
  for (int i = 1; i < l; i++)
    pow *= 10LL;

  ll c1 = (ll)d * pow;
  ll c2 = (d == 9) ? pow * 10LL : (ll)(d + 1) * pow;

  ll diff1 = (n > c1) ? (n - c1) : (c1 - n);
  ll diff2 = (n > c2) ? (n - c2) : (c2 - n);

  ll ans = (diff2 < diff1 || diff1 == diff2) ? c2 : c1;
  cout << ans << "\n";

  return 0;
}
```
