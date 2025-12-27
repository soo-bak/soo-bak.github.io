---
layout: single
title: "[백준 4890] Tiles of Tetris, NOT! (C#, C++) - soo:bak"
date: "2025-12-26 00:31:33 +0900"
description: "백준 4890번 C#, C++ 풀이 - 직사각형 타일로 가장 작은 정사각형을 만들 때 필요한 개수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 4890
  - C#
  - C++
  - 알고리즘
keywords: "백준 4890, 백준 4890번, BOJ 4890, TilesOfTetrisNot, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4890번 - Tiles of Tetris, NOT!](https://www.acmicpc.net/problem/4890)

## 설명
같은 방향으로 놓는 직사각형 타일만으로 가장 작은 정사각형을 만들 때 필요한 타일 개수를 구하는 문제입니다.

<br>

## 접근법
먼저 정사각형의 한 변은 타일의 가로와 세로 길이 모두의 배수여야 합니다.

다음으로 가능한 한 변 중 가장 작은 값은 두 길이의 최소 공배수입니다.

이후 가로와 세로에 들어가는 타일 수를 곱하면 필요한 타일 개수가 됩니다.

마지막으로 0 0이 나올 때까지 각 입력을 처리해 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static long Gcd(long a, long b) {
    while (b != 0) {
      var t = a % b;
      a = b;
      b = t;
    }
    return a;
  }

  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var sb = new StringBuilder();

    while (idx + 1 < parts.Length) {
      var w = long.Parse(parts[idx++]);
      var h = long.Parse(parts[idx++]);
      if (w == 0 && h == 0) break;

      var g = Gcd(w, h);
      var ans = (w / g) * (h / g);
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
typedef long long ll;

ll gcd(ll a, ll b) {
  while (b != 0) {
    ll t = a % b;
    a = b;
    b = t;
  }
  return a;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll w, h;
  while (cin >> w >> h) {
    if (w == 0 && h == 0) break;
    ll g = gcd(w, h);
    ll ans = (w / g) * (h / g);
    cout << ans << "\n";
  }

  return 0;
}
```
