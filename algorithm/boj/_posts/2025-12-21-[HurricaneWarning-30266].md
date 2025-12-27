---
layout: single
title: "[백준 30266] Hurricane Warning (C#, C++) - soo:bak"
date: "2025-12-21 09:00:00 +0900"
description: "백준 30266번 C#, C++ 풀이 - 경로 문자 집합과 사람별 소비 매체 집합의 교집합 유무로 경고 수신 인원 수를 세는 문제"
tags:
  - 백준
  - BOJ
  - 30266
  - C#
  - C++
  - 알고리즘
keywords: "백준 30266, 백준 30266번, BOJ 30266, HurricaneWarning, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30266번 - Hurricane Warning](https://www.acmicpc.net/problem/30266)

## 설명
당국이 사용한 매체와 각 사람이 소비하는 매체가 겹치는 경우 경고를 받은 것으로 보고, 경고를 받은 사람 수를 세는 문제입니다.

<br>

## 접근법
당국이 사용한 매체를 배열에 표시해둡니다. 각 사람의 소비 매체 문자열을 순회하면서 당국 매체와 겹치는 문자가 하나라도 있으면 그 사람은 경고를 받은 것으로 처리합니다. 모든 사람을 확인한 뒤 경고를 받은 인원 수를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var k = int.Parse(Console.ReadLine()!);

    for (var tc = 1; tc <= k; tc++) {
      var n = int.Parse(Console.ReadLine()!);
      var usedStr = Console.ReadLine()!;
      var used = new bool[26];
      foreach (var ch in usedStr) used[ch - 'A'] = true;

      var count = 0;
      for (var i = 0; i < n; i++) {
        var s = Console.ReadLine()!;
        var ok = false;
        foreach (var ch in s) {
          if (used[ch - 'A']) { ok = true; break; }
        }
        if (ok) count++;
      }

      Console.WriteLine($"Data Set {tc}:");
      Console.WriteLine(count);
      Console.WriteLine();
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

  int k; cin >> k;

  for (int tc = 1; tc <= k; tc++) {
    int n; cin >> n;
    string usedStr; cin >> usedStr;
    bool used[26] = {};
    for (char c : usedStr)
      used[c - 'A'] = true;

    int cnt = 0;
    for (int i = 0; i < n; i++) {
      string s; cin >> s;
      bool ok = false;
      for (char c : s) {
        if (used[c - 'A']) { ok = true; break; }
      }
      if (ok) cnt++;
    }

    cout << "Data Set " << tc << ":\n" << cnt << "\n\n";
  }

  return 0;
}
```
