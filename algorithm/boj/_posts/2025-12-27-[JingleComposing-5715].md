---
layout: single
title: "[백준 5715] Jingle Composing (C#, C++) - soo:bak"
date: "2025-12-27 12:35:00 +0900"
description: 슬래시로 구분된 마디 중 길이가 1이 되는 개수를 세는 문제
---

## 문제 링크
[5715번 - Jingle Composing](https://www.acmicpc.net/problem/5715)

## 설명
악보가 주어지며 슬래시로 마디가 구분됩니다. 각 음표는 길이를 가지며, 마디 내 음표 길이의 합이 정확히 1인 마디의 개수를 세어 출력하는 문제입니다.

<br>

## 접근법
각 음표 길이를 정수로 변환합니다. 가장 짧은 음표를 1로 두면 전체가 정수 계산이 됩니다.

슬래시 사이를 한 마디로 보고, 합이 기준값과 같으면 개수를 셉니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var val = new Dictionary<char, int> {
      ['W'] = 64, ['H'] = 32, ['Q'] = 16, ['E'] = 8,
      ['S'] = 4,  ['T'] = 2,  ['X'] = 1
    };

    string? line;
    while ((line = Console.ReadLine()) != null) {
      if (line == "*") break;
      var cur = 0;
      var good = 0;
      foreach (var ch in line) {
        if (ch == '/') {
          if (cur == 64) good++;
          cur = 0;
        } else cur += val[ch];
      }
      Console.WriteLine(good);
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

  unordered_map<char, int> val{
    {'W',64},{'H',32},{'Q',16},{'E',8},
    {'S',4},{'T',2},{'X',1}
  };

  string line;
  while (cin >> line) {
    if (line == "*") break;
    int cur = 0, good = 0;
    for (char c : line) {
      if (c == '/') {
        if (cur == 64) good++;
        cur = 0;
      } else cur += val[c];
    }
    cout << good << "\n";
  }

  return 0;
}
```
