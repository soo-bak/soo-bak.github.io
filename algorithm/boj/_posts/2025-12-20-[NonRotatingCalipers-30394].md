---
layout: single
title: "[백준 30394] 회전하지 않는 캘리퍼스 (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 30394번 C#, C++ 풀이 - 자를 세워 놓고 점 집합의 최소/최대 x좌표 차이를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 30394
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 30394, 백준 30394번, BOJ 30394, NonRotatingCalipers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30394번 - 회전하지 않는 캘리퍼스](https://www.acmicpc.net/problem/30394)

## 설명
y축에 평행하게 세운 캘리퍼스로 점 집합을 측정할 때, 날이 처음 닿는 거리를 구하는 문제입니다. 캘리퍼스가 y축 방향으로 서 있으므로 측정되는 것은 y좌표의 범위입니다.

<br>

## 접근법
캘리퍼스가 y축에 평행하게 고정되어 있으므로 측정되는 거리는 y좌표의 범위입니다. 모든 점의 y좌표를 저장한 뒤 정렬하면 최솟값과 최댓값을 쉽게 얻을 수 있습니다.

정렬된 배열의 마지막 원소에서 첫 원소를 빼면 답입니다.

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var yCoords = new int[n];

    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      yCoords[i] = int.Parse(parts[1]);
    }

    Array.Sort(yCoords);

    Console.WriteLine(yCoords[n - 1] - yCoords[0]);
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

  vi yCoords(n);
  for (int i = 0; i < n; i++) {
    int x, y; cin >> x >> y;
    yCoords[i] = y;
  }

  sort(yCoords.begin(), yCoords.end());

  cout << yCoords.back() - yCoords.front() << "\n";

  return 0;
}
```
