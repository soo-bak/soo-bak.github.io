---
layout: single
title: "[백준 30684] 모르고리즘 회장 정하기 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 30684번 C#, C++ 풀이 - 길이가 3인 이름 중 사전순으로 가장 앞선 이름을 찾는 문제"
tags:
  - 백준
  - BOJ
  - 30684
  - C#
  - C++
  - 알고리즘
keywords: "백준 30684, 백준 30684번, BOJ 30684, MororhythmPresident, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30684번 - 모르고리즘 회장 정하기](https://www.acmicpc.net/problem/30684)

## 설명
이름 목록에서 길이가 3인 이름만 고려해 사전 순으로 가장 앞선 이름을 출력하는 문제입니다.

<br>

## 접근법
입력된 이름 중 길이가 3인 것만 골라 최솟값을 갱신합니다.  
사전 순 비교는 문자열 비교로 충분합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    string? best = null;

    for (var i = 0; i < n; i++) {
      var name = Console.ReadLine()!;
      if (name.Length != 3) continue;
      if (best == null || string.Compare(name, best) < 0) best = name;
    }

    Console.WriteLine(best);
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
  string best = "";

  for (int i = 0; i < n; i++) {
    string name; cin >> name;
    if ((int)name.size() != 3) continue;
    if (best.empty() || name < best) best = name;
  }

  cout << best << "\n";

  return 0;
}
```
