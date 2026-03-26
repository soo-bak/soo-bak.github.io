---
layout: single
title: "[백준 20735] Fifty Shades of Pink (C#, C++) - soo:bak"
date: "2026-03-26 20:17:00 +0900"
description: "백준 20735번 C#, C++ 풀이 - 문자열을 소문자로 바꾼 뒤 pink 또는 rose 포함 여부를 세는 문제"
tags:
  - 백준
  - BOJ
  - 20735
  - C#
  - C++
  - 알고리즘
  - 문자열
  - 구현
keywords: "백준 20735, 백준 20735번, BOJ 20735, Fifty Shades of Pink, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[20735번 - Fifty Shades of Pink](https://www.acmicpc.net/problem/20735)

## 설명
색 이름이 적힌 문자열들 중에서, 대소문자를 무시하고 `pink` 또는 `rose`가 포함된 문자열의 개수를 구하는 문제입니다.

<br>

## 접근법
각 문자열을 소문자로 바꾼 뒤 `pink` 또는 `rose`가 부분 문자열로 들어 있는지 확인합니다.

조건을 만족하는 문자열의 개수를 세고, 그 개수가 0이면 문제에서 요구한 문장을 출력합니다. 아니면 개수를 그대로 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine()!);
    int count = 0;

    for (int i = 0; i < n; i++) {
      string s = Console.ReadLine()!.ToLower();
      if (s.Contains("pink") || s.Contains("rose"))
        count++;
    }

    if (count == 0)
      Console.WriteLine("I must watch Star Wars with my daughter");
    else
      Console.WriteLine(count);
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
  cin >> n;

  int count = 0;
  for (int i = 0; i < n; i++) {
    string s;
    cin >> s;

    for (char& ch : s)
      ch = (char)tolower(ch);

    if (s.find("pink") != string::npos || s.find("rose") != string::npos)
      count++;
  }

  if (count == 0)
    cout << "I must watch Star Wars with my daughter\n";
  else
    cout << count << "\n";

  return 0;
}
```
