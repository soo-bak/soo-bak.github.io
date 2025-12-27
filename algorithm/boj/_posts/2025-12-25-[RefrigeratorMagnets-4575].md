---
layout: single
title: "[백준 4575] Refrigerator Magnets (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 4575번 C#, C++ 풀이 - 중복 알파벳이 없는 문장만 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 4575
  - C#
  - C++
  - 알고리즘
keywords: "백준 4575, 백준 4575번, BOJ 4575, RefrigeratorMagnets, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4575번 - Refrigerator Magnets](https://www.acmicpc.net/problem/4575)

## 설명
각 문장에 같은 알파벳이 두 번 이상 등장하지 않을 때만 그대로 출력하는 문제입니다.

<br>

## 접근법
한 줄씩 읽다가 END가 나오면 종료합니다.  
공백을 제외하고 알파벳의 등장 여부를 확인해 중복이 없으면 그 줄을 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var sb = new StringBuilder();
    string? line;
    while ((line = Console.ReadLine()) != null) {
      if (line == "END") break;
      var seen = new bool[26];
      var ok = true;
      foreach (var ch in line) {
        if (ch == ' ') continue;
        var idx = ch - 'A';
        if (seen[idx]) { ok = false; break; }
        seen[idx] = true;
      }
      if (ok) sb.AppendLine(line);
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

  string line;
  while (getline(cin, line)) {
    if (line == "END") break;
    bool seen[26] = {};
    bool ok = true;
    for (char ch : line) {
      if (ch == ' ') continue;
      int idx = ch - 'A';
      if (seen[idx]) { ok = false; break; }
      seen[idx] = true;
    }
    if (ok) cout << line << "\n";
  }

  return 0;
}
```
