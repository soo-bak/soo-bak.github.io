---
layout: single
title: "[백준 11269] Cryptographer’s Conundrum (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 11269번 C#, C++ 풀이 - 문자열을 PER 반복으로 바꾸기 위해 다른 글자 수를 세는 문제"
tags:
  - 백준
  - BOJ
  - 11269
  - C#
  - C++
  - 알고리즘
keywords: "백준 11269, 백준 11269번, BOJ 11269, CryptographersConundrum, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11269번 - Cryptographer’s Conundrum](https://www.acmicpc.net/problem/11269)

## 설명
문자열을 PERPER... 형태로 만들기 위해 바꿔야 하는 글자 수를 세는 문제입니다.

<br>

## 접근법
목표 문자열은 PER이 반복되는 형태입니다.  
각 위치의 기대 문자를 비교해 다르면 카운트를 증가시키면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var pattern = "PER";
    var cnt = 0;
    for (var i = 0; i < s.Length; i++) {
      if (s[i] != pattern[i % 3]) cnt++;
    }
    Console.WriteLine(cnt);
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

  string s; cin >> s;
  string pattern = "PER";
  int cnt = 0;
  for (int i = 0; i < (int)s.size(); i++) {
    if (s[i] != pattern[i % 3]) cnt++;
  }
  cout << cnt << "\n";

  return 0;
}
```
