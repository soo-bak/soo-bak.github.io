---
layout: single
title: "[백준 25755] 거울반사 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 25755번 C#, C++ 풀이 - 배열을 방향에 맞게 뒤집고 숫자를 대응시켜 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 25755
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 25755, 백준 25755번, BOJ 25755, MirrorReflection, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25755번 - 거울반사](https://www.acmicpc.net/problem/25755)

## 설명
N×N 배열을 상하 또는 좌우로 뒤집고, 뒤집힌 숫자를 규칙에 맞게 변환해 출력하는 문제입니다.

<br>

## 접근법
L/R이면 좌우 반전, U/D이면 상하 반전으로 원본 인덱스를 결정합니다.  
가져온 숫자는 1→1, 2↔5, 8→8로 바꾸고 나머지는 `?`로 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static char Conv(int x) {
    if (x == 1) return '1';
    if (x == 2) return '5';
    if (x == 5) return '2';
    if (x == 8) return '8';
    return '?';
  }

  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var w = parts[idx++][0];
    var n = int.Parse(parts[idx++]);

    var a = new int[n, n];
    for (var i = 0; i < n; i++)
      for (var j = 0; j < n; j++)
        a[i, j] = int.Parse(parts[idx++]);

    var sb = new StringBuilder();
    for (var i = 0; i < n; i++) {
      for (var j = 0; j < n; j++) {
        var si = i;
        var sj = j;
        if (w == 'L' || w == 'R') sj = n - 1 - j;
        else si = n - 1 - i;
        if (j > 0) sb.Append(' ');
        sb.Append(Conv(a[si, sj]));
      }
      sb.AppendLine();
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<vi> vvi;

char conv(int x) {
  if (x == 1) return '1';
  if (x == 2) return '5';
  if (x == 5) return '2';
  if (x == 8) return '8';
  return '?';
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  char w; int n;
  cin >> w >> n;
  vvi a(n, vi(n));
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
      cin >> a[i][j];

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      int si = i, sj = j;
      if (w == 'L' || w == 'R') sj = n - 1 - j;
      else si = n - 1 - i;
      if (j > 0) cout << ' ';
      cout << conv(a[si][sj]);
    }
    cout << "\n";
  }

  return 0;
}
```
