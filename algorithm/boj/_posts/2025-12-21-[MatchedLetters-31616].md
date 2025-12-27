---
layout: single
title: "[백준 31616] 揃った文字 (Matched Letters) (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 31616번 C#, C++ 풀이 - 문자열이 모두 같은 문자로 이루어졌는지 확인해 Yes/No를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 31616
  - C#
  - C++
  - 알고리즘
keywords: "백준 31616, 백준 31616번, BOJ 31616, MatchedLetters, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31616번 - 揃った文字 (Matched Letters)](https://www.acmicpc.net/problem/31616)

## 설명
길이 N의 문자열이 모두 같은 문자로 이루어졌는지 판별하는 문제입니다.

<br>

## 접근법
첫 글자를 기준으로 나머지 문자들을 비교합니다. 하나라도 다르면 No, 끝까지 같으면 Yes를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;

    var ok = true;
    for (var i = 1; i < n; i++) {
      if (s[i] != s[0]) {
        ok = false;
        break;
      }
    }

    Console.WriteLine(ok ? "Yes" : "No");
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

  bool ok = true;
  for (int i = 1; i < n; i++) {
    if (s[i] != s[0]) {
      ok = false;
      break;
    }
  }

  cout << (ok ? "Yes" : "No") << "\n";

  return 0;
}
```
