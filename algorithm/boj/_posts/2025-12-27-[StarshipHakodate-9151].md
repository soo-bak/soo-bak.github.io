---
layout: single
title: "[백준 9151] Starship Hakodate-maru (C#, C++) - soo:bak"
date: "2025-12-27 03:45:00 +0900"
description: "백준 9151번 C#, C++ 풀이 - 주어진 값 이하에서 큐브 수와 사면체 수의 합으로 만들 수 있는 최댓값을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 9151
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
  - arithmetic
keywords: "백준 9151, 백준 9151번, BOJ 9151, StarshipHakodate, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9151번 - Starship Hakodate-maru](https://www.acmicpc.net/problem/9151)

## 설명
0 이상의 세제곱수(큐브 수)와 사면체수의 합으로 만들 수 있는 값 중, 주어진 값 이하에서 가장 큰 값을 구하는 문제입니다. 입력은 여러 줄이며 0이 나오면 종료합니다.

<br>

## 접근법
세제곱수와 사면체수를 각각 계산하는 함수를 만들어 둡니다. 이중 루프로 두 값의 합이 입력값 이하인 모든 경우를 탐색하며 최댓값을 갱신합니다.

세제곱수가 입력값을 넘으면 바깥 루프를, 합이 입력값을 넘으면 안쪽 루프를 종료합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static int Cubic(int x) => x * x * x;
  static int Tetra(int x) => x * (x + 1) * (x + 2) / 6;

  static void Main() {
    var parts = Console.In.ReadToEnd().Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
    var sb = new StringBuilder();

    foreach (var p in parts) {
      var n = int.Parse(p);
      if (n == 0) break;

      var ans = 0;
      for (var i = 0; Cubic(i) <= n; i++)
        for (var j = 0; Cubic(i) + Tetra(j) <= n; j++)
          ans = Math.Max(ans, Cubic(i) + Tetra(j));
      sb.AppendLine(ans.ToString());
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int cubic(int x) { return x * x * x; }
int tetra(int x) { return x * (x + 1) * (x + 2) / 6; }

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  while (true) {
    int n; cin >> n;
    if (!n) break;

    int ans = 0;
    for (int i = 0; cubic(i) <= n; i++)
      for (int j = 0; cubic(i) + tetra(j) <= n; j++)
        ans = max(ans, cubic(i) + tetra(j));
    cout << ans << "\n";
  }

  return 0;
}
```
