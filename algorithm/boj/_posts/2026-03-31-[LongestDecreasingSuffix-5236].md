---
layout: single
title: "[백준 5236] Longest Decreasing Suffix (C#, C++) - soo:bak"
date: "2026-03-31 19:51:00 +0900"
description: "백준 5236번 C#, C++ 풀이 - 문자열 뒤에서부터 감소 관계가 유지되는 가장 긴 접미사를 찾는 문제"
tags:
  - 백준
  - BOJ
  - 5236
  - C#
  - C++
  - 알고리즘
  - 문자열
  - 구현
keywords: "백준 5236, 백준 5236번, BOJ 5236, Longest Decreasing Suffix, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5236번 - Longest Decreasing Suffix](https://www.acmicpc.net/problem/5236)

## 설명
문자열마다 가장 긴 감소 접미사를 찾아 출력하는 문제입니다. 접미사 안에서는 왼쪽 문자가 바로 오른쪽 문자보다 커야 합니다.

<br>

## 접근법
감소 접미사는 문자열의 맨 뒤에서 시작하므로, 뒤에서부터 확인하면 됩니다.

끝 문자에서 시작해서 왼쪽으로 한 칸씩 보면서 `s[i - 1] > s[i]`가 성립하는 동안만 범위를 넓힙니다. 이 조건이 처음 끊기는 위치 다음부터가 가장 긴 감소 접미사입니다.

찾은 시작 위치부터 문자열 끝까지 잘라서 문제에서 요구한 형식대로 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine()!);

    for (int tc = 0; tc < t; tc++) {
      string s = Console.ReadLine()!;
      int start = s.Length - 1;

      while (start > 0 && s[start - 1] > s[start]) {
        start--;
      }

      string suffix = s.Substring(start);
      Console.WriteLine($"The longest decreasing suffix of {s} is {suffix}");
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

  int t;
  cin >> t;

  while (t--) {
    string s;
    cin >> s;

    int start = (int)s.size() - 1;
    while (start > 0 && s[start - 1] > s[start]) {
      start--;
    }

    string suffix = s.substr(start);
    cout << "The longest decreasing suffix of " << s << " is " << suffix << "\n";
  }

  return 0;
}
```
