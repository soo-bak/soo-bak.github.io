---
layout: single
title: "[백준 29716] 풀만한문제 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 29716번 C#, C++ 풀이 - 문제 문자열 크기가 잡초보다 크지 않은 개수를 세는 문제"
tags:
  - 백준
  - BOJ
  - 29716
  - C#
  - C++
  - 알고리즘
keywords: "백준 29716, 백준 29716번, BOJ 29716, SolvableProblem, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[29716번 - 풀만한문제](https://www.acmicpc.net/problem/29716)

## 설명
각 문제 문자열의 크기를 계산해 잡초 크기 이하인 문제의 개수를 출력하는 문제입니다.

<br>

## 접근법
문자별 크기를 더해 한 줄의 크기를 계산합니다.  
크기가 J 이하인 줄의 개수를 세면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var j = int.Parse(first[0]);
    var n = int.Parse(first[1]);

    var cnt = 0;
    for (var i = 0; i < n; i++) {
      var line = Console.ReadLine()!;
      var size = 0;
      foreach (var ch in line) {
        if (ch >= 'A' && ch <= 'Z') size += 4;
        else if ((ch >= 'a' && ch <= 'z') || (ch >= '0' && ch <= '9')) size += 2;
        else size += 1;
      }
      if (size <= j) cnt++;
    }

    Console.WriteLine(cnt);
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

  int j, n; cin >> j >> n;
  string line;
  getline(cin, line);

  int cnt = 0;
  for (int i = 0; i < n; i++) {
    getline(cin, line);
    int size = 0;
    for (char ch : line) {
      if ('A' <= ch && ch <= 'Z') size += 4;
      else if (('a' <= ch && ch <= 'z') || ('0' <= ch && ch <= '9')) size += 2;
      else size += 1;
    }
    if (size <= j) cnt++;
  }

  cout << cnt << "\n";

  return 0;
}
```
