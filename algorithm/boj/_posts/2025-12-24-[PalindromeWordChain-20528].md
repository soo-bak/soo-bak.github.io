---
layout: single
title: "[백준 20528] 끝말잇기 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: "백준 20528번 C#, C++ 풀이 - 모든 팰린드롬 문자열의 첫 글자가 같은지 확인하는 문제"
tags:
  - 백준
  - BOJ
  - 20528
  - C#
  - C++
  - 알고리즘
  - 문자열
  - 애드혹
keywords: "백준 20528, 백준 20528번, BOJ 20528, PalindromeWordChain, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[20528번 - 끝말잇기](https://www.acmicpc.net/problem/20528)

## 설명
주어진 팰린드롬 문자열들을 모두 사용해 끝말잇기가 가능한지 판단하는 문제입니다.

<br>

## 접근법
팰린드롬 문자열은 첫 글자와 마지막 글자가 같습니다.

따라서 각 문자열은 시작 글자 하나로만 구분되며, 끝말잇기가 가능하려면 모든 문자열의 시작 글자가 같아야 합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var data = Console.In.ReadToEnd();
    var parts = data.Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);

    var first = parts[idx++][0];
    var ok = true;
    for (var i = 1; i < n; i++) {
      var s = parts[idx++];
      if (s[0] != first) ok = false;
    }

    Console.WriteLine(ok ? 1 : 0);
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
  char first = s[0];
  bool ok = true;

  for (int i = 1; i < n; i++) {
    cin >> s;
    if (s[0] != first) ok = false;
  }

  cout << (ok ? 1 : 0) << "\n";

  return 0;
}
```
