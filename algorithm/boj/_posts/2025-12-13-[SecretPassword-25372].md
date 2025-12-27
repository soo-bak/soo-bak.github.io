---
layout: single
title: "[백준 25372] 성택이의 은밀한 비밀번호 (C#, C++) - soo:bak"
date: "2025-12-13 00:03:00 +0900"
description: 비밀번호 문자열 길이가 6~9 사이인지 판별해 yes/no를 출력하는 백준 25372번 성택이의 은밀한 비밀번호 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 25372
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 25372, 백준 25372번, BOJ 25372, SecretPassword, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25372번 - 성택이의 은밀한 비밀번호](https://www.acmicpc.net/problem/25372)

## 설명
비밀번호 문자열이 주어질 때, 사용 가능한지 판별하는 문제입니다.

<br>

## 접근법
비밀번호 길이가 6 이상 9 이하이면 사용할 수 있습니다.

각 문자열의 길이만 확인하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < n; i++) {
      var s = Console.ReadLine()!;
      var len = s.Length;
      Console.WriteLine(len >= 6 && len <= 9 ? "yes" : "no");
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

  int n; cin >> n;
  string s;
  while (n--) {
    cin >> s;
    int len = (int)s.size();
    cout << ((len >= 6 && len <= 9) ? "yes" : "no") << "\n";
  }

  return 0;
}
```
