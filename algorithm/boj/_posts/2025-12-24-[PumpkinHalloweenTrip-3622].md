---
layout: single
title: "[백준 3622] 어떤 호박의 할로윈 여행 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 3622번 C#, C++ 풀이 - 두 고리의 외반지름과 판의 반지름으로 제작 가능 여부를 판단하는 문제"
tags:
  - 백준
  - BOJ
  - 3622
  - C#
  - C++
  - 알고리즘
  - 기하학
  - 케이스분류
keywords: "백준 3622, 백준 3622번, BOJ 3622, PumpkinHalloweenTrip, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3622번 - 어떤 호박의 할로윈 여행](https://www.acmicpc.net/problem/3622)

## 설명
두 개의 고리를 하나의 원판에서 잘라낼 수 있는지 판단하는 문제입니다.

<br>

## 접근법
각 고리의 외반지름이 원판 반지름을 넘으면 불가능합니다.

이후 두 고리를 나란히 배치할 수 있으면 가능하므로 두 외반지름의 합이 원판 반지름 이하인지 확인합니다.

그렇지 않다면 한 고리를 다른 고리의 구멍에 넣을 수 있는지 확인합니다. 한 고리의 외반지름이 다른 고리의 내반지름 이하이면 가능합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var A = int.Parse(parts[0]);
    var a = int.Parse(parts[1]);
    var B = int.Parse(parts[2]);
    var b = int.Parse(parts[3]);
    var P = int.Parse(parts[4]);

    if (A > P || B > P) {
      Console.WriteLine("No");
      return;
    }

    if (A + B <= P || A <= b || B <= a) Console.WriteLine("Yes");
    else Console.WriteLine("No");
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

  int A, a, B, b, P; cin >> A >> a >> B >> b >> P;

  if (A > P || B > P) {
    cout << "No\n";
    return 0;
  }

  if (A + B <= P || A <= b || B <= a) cout << "Yes\n";
  else cout << "No\n";

  return 0;
}
```
