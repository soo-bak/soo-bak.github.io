---
layout: single
title: "[백준 13587] huaauhahhuahau (C#, C++) - soo:bak"
date: "2025-12-27 11:05:00 +0900"
description: "백준 13587번 C#, C++ 풀이 - 문자열에서 모음만 추출해 회문인지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 13587
  - C#
  - C++
  - 알고리즘
keywords: "백준 13587, 백준 13587번, BOJ 13587, huaauhahhuahau, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[13587번 - huaauhahhuahau](https://www.acmicpc.net/problem/13587)

## 설명
소문자 문자열에서 모음만 추출한 뒤, 그 문자열이 회문인지 판별하는 문제입니다.

<br>

## 접근법
모음만 모아 새로운 문자열을 만든 후 앞뒤를 비교해 회문 여부를 판정합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static bool IsVowel(char c) => c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';

  static void Main() {
    var s = Console.ReadLine()!;
    var sb = new StringBuilder();
    foreach (var c in s)
      if (IsVowel(c)) sb.Append(c);
    var v = sb.ToString();

    var ok = true;
    for (int l = 0, r = v.Length - 1; l < r; l++, r--) {
      if (v[l] != v[r]) { ok = false; break; }
    }

    Console.WriteLine(ok ? "S" : "N");
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

bool isVowel(char c) {
  return c=='a'||c=='e'||c=='i'||c=='o'||c=='u';
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s; cin >> s;
  string v;
  for (char c : s)
    if (isVowel(c)) v += c;

  bool ok = true;
  for (int l = 0, r = (int)v.size()-1; l < r; l++, r--) {
    if (v[l] != v[r]) { ok = false; break; }
  }

  cout << (ok ? "S" : "N") << "\n";

  return 0;
}
```
