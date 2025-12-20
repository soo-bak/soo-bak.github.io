---
layout: single
title: "[백준 21280] Confused Lecturer (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: 직전 주 일정만 믿고 출석하는 교수의 빈 강의실/결강 횟수를 합산하는 문제
---

## 문제 링크
[21280번 - Confused Lecturer](https://www.acmicpc.net/problem/21280)

## 설명
첫 주를 제외하면 교수는 항상 직전 주와 동일한 강의 수만 있다고 생각합니다. 각 주의 실제 강의 수가 주어질 때, 빈 강의실에서 강의한 횟수와 결강한 횟수를 합산해 출력하는 문제입니다.

<br>

## 접근법
교수는 항상 직전 주의 강의 수만큼 강의가 있다고 생각합니다. 실제 강의 수가 더 적으면 그 차이만큼 빈 강의실에서 강의하게 되고, 실제 강의 수가 더 많으면 그 차이만큼 결강하게 됩니다.

각 주마다 직전 주와 현재 주의 강의 수를 비교하여 차이를 누적하면 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var vals = new List<int>();
    while (vals.Count < n) {
      var line = Console.ReadLine();
      if (string.IsNullOrWhiteSpace(line)) continue;
      vals.AddRange(line.Split().Select(int.Parse));
    }

    var empty = 0;
    var missed = 0;
    for (var i = 1; i < n; i++) {
      var prev = vals[i - 1];
      var cur = vals[i];
      if (prev > cur) empty += prev - cur;
      else if (cur > prev) missed += cur - prev;
    }

    Console.WriteLine($"{empty} {missed}");
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
  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  int empty = 0, missed = 0;
  for (int i = 1; i < n; i++) {
    int prev = a[i - 1], cur = a[i];
    if (prev > cur) empty += prev - cur;
    else if (cur > prev) missed += cur - prev;
  }

  cout << empty << " " << missed << "\n";

  return 0;
}
```
