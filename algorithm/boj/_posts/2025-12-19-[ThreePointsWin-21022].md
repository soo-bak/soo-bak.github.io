---
layout: single
title: "[백준 21022] Three Points for a Win (C#, C++) - soo:bak"
date: "2025-12-19 22:47:00 +0900"
description: 경기 결과 a[i], b[i]를 비교해 승리 3점, 무승부 1점, 패배 0점을 합산하는 단순 구현 문제
tags:
  - 백준
  - BOJ
  - 21022
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 21022, 백준 21022번, BOJ 21022, ThreePointsWin, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[21022번 - Three Points for a Win](https://www.acmicpc.net/problem/21022)

## 설명
n경기의 우리 팀 점수와 상대 팀 점수가 주어질 때, 총 승점을 구하는 문제입니다.

승리하면 3점, 무승부면 1점, 패배하면 0점입니다.

<br>

## 접근법
각 경기에서 우리 팀 점수가 더 크면 3점, 같으면 1점을 더합니다.

모든 경기의 승점을 합산하여 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var a = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
    var b = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);

    var pts = 0;
    for (var i = 0; i < n; i++) {
      if (a[i] > b[i]) pts += 3;
      else if (a[i] == b[i]) pts += 1;
    }

    Console.WriteLine(pts);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vi a(n), b(n);
  for (int i = 0; i < n; i++) cin >> a[i];
  for (int i = 0; i < n; i++) cin >> b[i];

  int pts = 0;
  for (int i = 0; i < n; i++) {
    if (a[i] > b[i]) pts += 3;
    else if (a[i] == b[i]) pts += 1;
  }

  cout << pts << "\n";

  return 0;
}
```
