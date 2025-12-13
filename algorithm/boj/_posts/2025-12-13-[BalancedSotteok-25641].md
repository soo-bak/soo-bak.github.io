---
layout: single
title: "[백준 25641] 균형 잡힌 소떡소떡 (C#, C++) - soo:bak"
date: "2025-12-13 22:20:00 +0900"
description: 왼쪽에서만 떼어낼 수 있을 때 남은 접두사를 제거하며 s와 t 개수가 같아지는 지점부터 출력하는 백준 25641번 균형 잡힌 소떡소떡 문제의 C#/C++ 풀이
---

## 문제 링크
[25641번 - 균형 잡힌 소떡소떡](https://www.acmicpc.net/problem/25641)

## 설명
왼쪽에서만 문자를 제거할 때, s와 t 개수가 같은 가장 긴 접미 문자열을 구하는 문제입니다.

<br>

## 접근법
먼저 전체 s와 t 개수를 셉니다.

왼쪽부터 하나씩 제거하며 개수를 조정합니다.

s와 t 개수가 같아지는 순간의 접미 문자열이 답입니다.

<br>

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    Console.ReadLine();
    var s = Console.ReadLine()!;

    var cntS = 0;
    var cntT = 0;
    foreach (var ch in s) {
      if (ch == 's') cntS++;
      else cntT++;
    }

    var idx = 0;
    while (cntS != cntT) {
      if (s[idx] == 's') cntS--;
      else cntT--;
      idx++;
    }

    Console.WriteLine(s.Substring(idx));
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
  if (!(cin >> n)) return 0;
  string s; cin >> s;

  int cntS = 0, cntT = 0;
  for (char c : s) {
    if (c == 's') cntS++; else cntT++;
  }

  int idx = 0;
  while (cntS != cntT) {
    if (s[idx] == 's') cntS--;
    else cntT--;
    idx++;
  }

  cout << s.substr(idx) << "\n";

  return 0;
}
```
