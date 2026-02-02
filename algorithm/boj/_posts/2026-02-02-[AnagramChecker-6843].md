---
layout: single
title: "[백준 6843] Anagram Checker (C#, C++) - soo:bak"
date: "2026-02-02 21:11:00 +0900"
description: "백준 6843번 C#, C++ 풀이 - 두 문장이 애너그램인지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 6843
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 6843, 백준 6843번, BOJ 6843, Anagram Checker, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6843번 - Anagram Checker](https://www.acmicpc.net/problem/6843)

## 설명
대문자와 공백으로 이루어진 두 문장이 주어질 때, 공백을 무시하고 알파벳 빈도가 같으면 애너그램으로 판정하는 문제입니다.

<br>

## 접근법
알파벳 26개에 대한 빈도를 두 문장 각각 세어 배열을 비교합니다.

공백은 건너뛰고, 하나라도 다르면 "Is not an anagram.", 모두 같으면 "Is an anagram."을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var a = Console.ReadLine()!;
    var b = Console.ReadLine()!;

    var ca = new int[26];
    var cb = new int[26];

    foreach (var ch in a)
      if (ch != ' ') ca[ch - 'A']++;
    foreach (var ch in b)
      if (ch != ' ') cb[ch - 'A']++;

    bool same = true;
    for (int i = 0; i < 26; i++) {
      if (ca[i] != cb[i]) { same = false; break; }
    }

    Console.WriteLine(same ? "Is an anagram." : "Is not an anagram.");
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

  string a, b;
  getline(cin, a);
  getline(cin, b);

  int ca[26] = {0}, cb[26] = {0};
  for (char c : a) if (c != ' ') ca[c - 'A']++;
  for (char c : b) if (c != ' ') cb[c - 'A']++;

  bool same = true;
  for (int i = 0; i < 26; i++) if (ca[i] != cb[i]) { same = false; break; }

  cout << (same ? "Is an anagram." : "Is not an anagram.") << "\n";
  return 0;
}
```
