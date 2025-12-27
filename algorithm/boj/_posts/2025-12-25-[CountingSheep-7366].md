---
layout: single
title: "[백준 7366] Counting Sheep (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 7366번 C#, C++ 풀이 - 단어 목록에서 sheep의 등장 횟수를 세는 문제"
tags:
  - 백준
  - BOJ
  - 7366
  - C#
  - C++
  - 알고리즘
keywords: "백준 7366, 백준 7366번, BOJ 7366, CountingSheep, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[7366번 - Counting Sheep](https://www.acmicpc.net/problem/7366)

## 설명
각 테스트에서 단어 목록 중 정확히 "sheep"과 일치하는 개수를 세어 출력하는 문제입니다.

<br>

## 접근법
목록을 그대로 읽으면서 "sheep"과 같은 단어만 세면 됩니다.  
출력은 케이스마다 한 줄을 찍고, 케이스 사이에 빈 줄을 한 줄 추가합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var caseNo = 1; caseNo <= t; caseNo++) {
      var m = int.Parse(parts[idx++]);
      var cnt = 0;
      for (var i = 0; i < m; i++) {
        if (parts[idx++] == "sheep") cnt++;
      }
      sb.AppendLine($"Case {caseNo}: This list contains {cnt} sheep.");
      if (caseNo < t) sb.AppendLine();
    }

    Console.Write(sb);
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
  for (int caseNo = 1; caseNo <= t; caseNo++) {
    int m; cin >> m;
    int cnt = 0;
    for (int i = 0; i < m; i++) {
      string w; cin >> w;
      if (w == "sheep") cnt++;
    }
    cout << "Case " << caseNo << ": This list contains " << cnt << " sheep.\n";
    if (caseNo < t) cout << "\n";
  }

  return 0;
}
```
