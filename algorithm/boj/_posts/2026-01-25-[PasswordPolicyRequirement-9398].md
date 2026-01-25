---
layout: single
title: "[백준 9398] A Password Policy Requirement (C#, C++) - soo:bak"
date: "2026-01-25 18:20:00 +0900"
description: "백준 9398번 C#, C++ 풀이 - 대문자/소문자/숫자를 모두 포함하고 길이 6 이상인 최소 부분문자열 길이 찾기"
tags:
  - 백준
  - BOJ
  - 9398
  - C#
  - C++
  - 알고리즘
  - 구현
  - 투 포인터
keywords: "백준 9398, 백준 9398번, BOJ 9398, A Password Policy Requirement, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9398번 - A Password Policy Requirement](https://www.acmicpc.net/problem/9398)

## 설명
문자열에서 길이 6 이상이면서 대문자, 소문자, 숫자를 모두 포함하는 가장 짧은 연속 부분문자열의 길이를 찾는 문제입니다. 조건을 만족하는 부분문자열이 없으면 0을 출력합니다.

<br>

## 접근법
투 포인터(슬라이딩 윈도우)로 최소 길이를 찾습니다.

오른쪽 포인터로 문자를 추가하며 대문자/소문자/숫자 개수를 센 뒤, 조건을 만족하면 왼쪽 포인터를 이동시켜 가능한 한 윈도우를 줄입니다.

문자 종류 카운트가 모두 1 이상이고 윈도우 길이가 6 이상일 때 최소 길이를 갱신합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static bool IsUpper(char c) => c >= 'A' && c <= 'Z';
  static bool IsLower(char c) => c >= 'a' && c <= 'z';
  static bool IsDigit(char c) => c >= '0' && c <= '9';

  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var tc = 0; tc < t; tc++) {
      var s = Console.ReadLine()!;
      int n = s.Length;
      int upper = 0, lower = 0, digit = 0;
      int best = n + 1;
      int l = 0;
      for (int r = 0; r < n; r++) {
        char c = s[r];
        if (IsUpper(c)) upper++;
        else if (IsLower(c)) lower++;
        else if (IsDigit(c)) digit++;

        while (l <= r && upper > 0 && lower > 0 && digit > 0 && r - l + 1 >= 6) {
          best = Math.Min(best, r - l + 1);
          char cl = s[l];
          if (IsUpper(cl)) upper--;
          else if (IsLower(cl)) lower--;
          else if (IsDigit(cl)) digit--;
          l++;
        }
      }

      Console.WriteLine(best == n + 1 ? 0 : best);
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

  int t;  cin >> t;
  while (t--) {
    string s; 
    cin >> s;
    int n = s.size();
    int upper = 0, lower = 0, digit = 0;
    int best = n + 1;
    int l = 0;
    for (int r = 0; r < n; r++) {
      char c = s[r];
      if ('A' <= c && c <= 'Z') upper++;
      else if ('a' <= c && c <= 'z') lower++;
      else if ('0' <= c && c <= '9') digit++;

      while (l <= r && upper && lower && digit && (r - l + 1) >= 6) {
        best = min(best, r - l + 1);
        char cl = s[l];
        if ('A' <= cl && cl <= 'Z') upper--;
        else if ('a' <= cl && cl <= 'z') lower--;
        else if ('0' <= cl && cl <= '9') digit--;
        l++;
      }
    }

    cout << (best == n + 1 ? 0 : best) << "\n";
  }

  return 0;
}
```
