---
layout: single
title: "[백준 27329] Repeating String (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 27329번 C#, C++ 풀이 - 문자열이 같은 절반 두 개로 이뤄져 있는지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 27329
  - C#
  - C++
  - 알고리즘
keywords: "백준 27329, 백준 27329번, BOJ 27329, RepeatingString, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[27329번 - Repeating String](https://www.acmicpc.net/problem/27329)

## 설명
길이가 짝수인 문자열이 주어질 때, 앞 절반과 뒤 절반이 동일하면 Yes, 아니면 No를 출력하는 문제입니다. 문자는 J, O, I만 사용됩니다.

<br>

## 접근법
문자열이 같은 패턴의 반복으로 이루어져 있다면, 앞 절반과 뒤 절반이 정확히 일치해야 합니다. 문자열 길이의 절반을 기준으로 두 구간을 나눈 뒤, 각 위치의 문자를 비교하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    Console.ReadLine();
    var s = Console.ReadLine()!;
    var half = s.Length / 2;

    var isRepeat = true;
    for (var i = 0; i < half; i++) {
      if (s[i] != s[i + half]) { isRepeat = false; break; }
    }

    Console.WriteLine(isRepeat ? "Yes" : "No");
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
  int half = n / 2;

  bool ok = true;
  for (int i = 0; i < half; i++) {
    if (s[i] != s[i + half]) { ok = false; break; }
  }

  cout << (ok ? "Yes" : "No") << "\n";

  return 0;
}
```
