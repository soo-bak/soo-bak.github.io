---
layout: single
title: "[백준 13136] Do Not Touch Anything (C#, C++) - soo:bak"
date: "2025-12-13 05:01:00 +0900"
description: R×C 좌석을 N×N 감시 범위의 CCTV로 덮을 때 필요한 최소 대수를 올림 나눗셈으로 구하는 백준 13136번 Do Not Touch Anything 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[13136번 - Do Not Touch Anything](https://www.acmicpc.net/problem/13136)

## 설명
R행 C열의 좌석을 N×N 영역을 감시하는 CCTV로 모두 커버할 때 필요한 최소 CCTV 개수를 구하는 문제입니다.

<br>

## 접근법
행 방향으로 필요한 CCTV 수는 R을 N으로 나눈 값을 올림한 것입니다.

열 방향도 마찬가지로 C를 N으로 나눈 값을 올림합니다.

두 값을 곱하면 전체 CCTV 수가 됩니다.

올림 나눗셈은 (x + n - 1) / n으로 계산합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Console.ReadLine()!.Split();
    var r = long.Parse(line[0]);
    var c = long.Parse(line[1]);
    var n = long.Parse(line[2]);

    long rows = (r + n - 1) / n;
    long cols = (c + n - 1) / n;
    Console.WriteLine(rows * cols);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll r, c, n; cin >> r >> c >> n;
  ll rows = (r + n - 1) / n;
  ll cols = (c + n - 1) / n;
  cout << rows * cols << "\n";

  return 0;
}
```
