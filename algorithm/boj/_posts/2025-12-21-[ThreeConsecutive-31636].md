---
layout: single
title: "[백준 31636] 三連続 (Three Consecutive) (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 31636번 C#, C++ 풀이 - 문자열에 o가 3번 연속 등장하는지 확인해 Yes/No를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 31636
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 31636, 백준 31636번, BOJ 31636, ThreeConsecutive, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31636번 - 三連続 (Three Consecutive)](https://www.acmicpc.net/problem/31636)

## 설명
문자열 S에서 o가 3번 연속 등장하는 구간이 있는지 판별하는 문제입니다.

<br>

## 접근법
문자열을 순회하며 연속된 o의 개수를 세고, 3에 도달하면 Yes를 출력합니다. 끝까지 도달하지 못하면 No를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;

    var cnt = 0;
    for (var i = 0; i < n; i++) {
      if (s[i] == 'o') cnt++;
      else cnt = 0;
      if (cnt == 3) {
        Console.WriteLine("Yes");
        return;
      }
    }

    Console.WriteLine("No");
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
  string s; cin >> s;

  int cnt = 0;
  for (int i = 0; i < n; i++) {
    if (s[i] == 'o') cnt++;
    else cnt = 0;
    if (cnt == 3) {
      cout << "Yes\n";
      return 0;
    }
  }

  cout << "No\n";

  return 0;
}
```
