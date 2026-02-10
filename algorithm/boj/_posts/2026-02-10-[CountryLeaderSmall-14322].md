---
layout: single
title: "[백준 14322] Country Leader (Small) (C#, C++) - soo:bak"
date: "2026-02-10 21:05:00 +0900"
description: "백준 14322번 C#, C++ 풀이 - 서로 다른 알파벳 종류 수가 가장 많은 이름을 고르는 문제"
tags:
  - 백준
  - BOJ
  - 14322
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 14322, 백준 14322번, BOJ 14322, Country Leader, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14322번 - Country Leader (Small)](https://www.acmicpc.net/problem/14322)

## 설명
리더가 될 사람의 이름을 고르는 문제입니다.

이름에 포함된 서로 다른 알파벳 종류 수가 가장 많은 사람이 리더가 되며, 동률이면 사전순으로 가장 앞선 이름을 선택합니다.

<br>

## 접근법
먼저 각 이름에 대해 대문자 알파벳만 따로 보고, 알파벳별 등장 여부를 26길이 불린 배열로 표시해 서로 다른 알파벳 종류 수를 셉니다.

다음으로 지금까지의 최고 종류 수와 비교해 더 크면 리더 후보를 교체하고, 같으면 사전순으로 더 앞선 이름을 남깁니다.

이 과정을 테스트케이스마다 반복해 각 테스트케이스의 리더 이름을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.IO;

class Program {
  static void Main() {
    using var reader = new StreamReader(Console.OpenStandardInput());
    using var writer = new StreamWriter(Console.OpenStandardOutput());

    var t = int.Parse(reader.ReadLine()!);
    for (var tc = 1; tc <= t; tc++) {
      var n = int.Parse(reader.ReadLine()!);
      var best = "";
      var bestCnt = -1;

      for (var i = 0; i < n; i++) {
        var name = reader.ReadLine()!;
        var seen = new bool[26];
        var cnt = 0;

        foreach (var ch in name) {
          if (ch < 'A' || ch > 'Z')
            continue;

          var idx = ch - 'A';
          if (!seen[idx]) {
            seen[idx] = true;
            cnt++;
          }
        }

        if (cnt > bestCnt || (cnt == bestCnt && string.CompareOrdinal(name, best) < 0)) {
          best = name;
          bestCnt = cnt;
        }
      }

      writer.WriteLine($"Case #{tc}: {best}");
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

  int t; cin >> t;
  for (int tc = 1; tc <= t; tc++) {
    int n; cin >> n;

    string best; int bestCnt = -1;
    for (int i = 0; i < n; i++) {
      string name; getline(cin >> ws, name);

      bool seen[26] = {false};
      int cnt = 0;

      for (char c : name) {
        if (c < 'A' || c > 'Z') continue;

        int idx = c - 'A';
        if (!seen[idx]) {
          seen[idx] = true;
          cnt++;
        }
      }

      if (cnt > bestCnt || (cnt == bestCnt && name < best)) {
        bestCnt = cnt;
        best = name;
      }
    }

    cout << "Case #" << tc << ": " << best << "\n";
  }

  return 0;
}
```
