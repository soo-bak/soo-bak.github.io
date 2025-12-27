---
layout: single
title: "[백준 5100] Jean and Joe’s Clothes (C#, C++) - soo:bak"
date: "2025-12-27 13:25:00 +0900"
description: "백준 5100번 C#, C++ 풀이 - 의류 사이즈에 따라 주인별 개수를 집계하는 문제"
tags:
  - 백준
  - BOJ
  - 5100
  - C#
  - C++
  - 알고리즘
keywords: "백준 5100, 백준 5100번, BOJ 5100, JeanAndJoesClothes, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5100번 - Jean and Joe’s Clothes](https://www.acmicpc.net/problem/5100)

## 설명
의류 사이즈가 주어질 때 주인을 분류하는 문제입니다. 사이즈에 따라 각 주인에게 배정하고, 각 주인별 의류 개수를 출력합니다.

<br>

## 접근법
각 사이즈를 읽어 조건에 맞게 해당 주인의 카운트를 증가시킵니다.

문자 사이즈와 숫자 사이즈를 구분하여 규칙에 따라 분류합니다.

<br>

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;
      var n = int.Parse(line);
      if (n == 0) break;

      int joe = 0, jean = 0, jane = 0, james = 0, unknown = 0;
      for (var i = 0; i < n; i++) {
        var s = Console.ReadLine()!;
        if (s == "M" || s == "L") joe++;
        else if (s == "S") james++;
        else if (s == "X") unknown++;
        else {
          var v = int.Parse(s);
          if (v >= 12) jean++;
          else jane++;
        }
      }
      Console.WriteLine($"{joe} {jean} {jane} {james} {unknown}");
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

  int n;
  while (cin >> n) {
    if (n == 0) break;
    int joe = 0, jean = 0, jane = 0, james = 0, unknown = 0;
    for (int i = 0; i < n; i++) {
      string s; cin >> s;
      if (s == "M" || s == "L") joe++;
      else if (s == "S") james++;
      else if (s == "X") unknown++;
      else {
        int v = stoi(s);
        if (v >= 12) jean++;
        else jane++;
      }
    }
    cout << joe << " " << jean << " " << jane << " " << james << " " << unknown << "\n";
  }

  return 0;
}
```
