---
layout: single
title: "[백준 32369] 양파 실험 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: 매일 성장과 역할 교대 규칙을 시뮬레이션하는 문제
---

## 문제 링크
[32369번 - 양파 실험](https://www.acmicpc.net/problem/32369)

## 설명
칭찬/비난 양파의 길이를 매일 갱신하며 N일 후의 길이를 출력하는 문제입니다.

<br>

## 접근법
두 양파의 길이를 유지하며 매일 각각의 성장량만큼 증가시킵니다.

이후 비난 양파가 더 길면 역할을 교대하고, 같으면 비난 양파를 1만큼 줄이는 규칙을 N일 동안 시뮬레이션합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var n = int.Parse(parts[0]);
    var a = int.Parse(parts[1]);
    var b = int.Parse(parts[2]);

    var good = 1;
    var bad = 1;
    for (var i = 0; i < n; i++) {
      good += a;
      bad += b;

      if (bad > good) {
        var temp = good;
        good = bad;
        bad = temp;
      } else if (bad == good) bad--;
    }

    Console.WriteLine($"{good} {bad}");
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

  int n, a, b; cin >> n >> a >> b;
  int good = 1, bad = 1;

  for (int i = 0; i < n; i++) {
    good += a;
    bad += b;

    if (bad > good) {
      int temp = good;
      good = bad;
      bad = temp;
    } else if (bad == good) bad--;
  }

  cout << good << " " << bad << "\n";

  return 0;
}
```
