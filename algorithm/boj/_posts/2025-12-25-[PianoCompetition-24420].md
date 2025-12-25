---
layout: single
title: "[백준 24420] ピアノコンクール (Piano Competition) (C#, C++) - soo:bak"
date: "2025-12-25 23:49:24 +0900"
description: 최고점과 최저점을 제외한 나머지 점수 합을 구하는 문제
---

## 문제 링크
[24420번 - ピアノコンクール (Piano Competition)](https://www.acmicpc.net/problem/24420)

## 설명
심사 점수들이 주어질 때 최고점과 최저점을 제외한 나머지 점수의 합을 구하는 문제입니다.

<br>

## 접근법
먼저 모든 점수를 합산하면서 최댓값과 최솟값을 함께 구합니다.

다음으로 전체 합에서 최댓값과 최솟값을 뺍니다.

마지막으로 결과를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var parts = Console.ReadLine()!.Split();

    var sum = 0;
    var mx = int.MinValue;
    var mn = int.MaxValue;

    for (var i = 0; i < n; i++) {
      var v = int.Parse(parts[i]);
      sum += v;
      if (v > mx) mx = v;
      if (v < mn) mn = v;
    }

    Console.WriteLine(sum - mx - mn);
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

  int n;
  if (!(cin >> n)) return 0;

  int sum = 0;
  int mx = -1;
  int mn = 101;
  for (int i = 0; i < n; i++) {
    int v; cin >> v;
    sum += v;
    if (v > mx) mx = v;
    if (v < mn) mn = v;
  }

  cout << sum - mx - mn << "\n";
  return 0;
}
```
