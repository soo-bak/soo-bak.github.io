---
layout: single
title: "[백준 30596] Axis-Aligned Area (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: 네 막대를 축에 평행하게 놓아 만들 수 있는 최대 직사각형 넓이를 구하는 문제
---

## 문제 링크
[30596번 - Axis-Aligned Area](https://www.acmicpc.net/problem/30596)

## 설명
네 개의 막대를 축에 평행하게 놓아 만들 수 있는 최대 직사각형 넓이를 구하는 문제입니다.

두 개는 가로, 두 개는 세로로 배치하며, 각 변의 길이는 같은 방향에 놓인 두 막대 중 짧은 길이가 됩니다.

<br>

## 접근법
막대가 오름차순으로 정렬되어 주어지므로, 가장 긴 두 막대를 한 방향으로, 짧은 두 막대를 다른 방향으로 배치하는 것이 최적입니다. 한 변은 첫 번째와 두 번째 중 짧은 값, 다른 한 변은 세 번째와 네 번째 중 짧은 값이 되어, 첫 번째와 세 번째 막대의 곱이 최대 넓이가 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var a1 = int.Parse(Console.ReadLine()!);
    _ = Console.ReadLine();
    var a3 = int.Parse(Console.ReadLine()!);
    _ = Console.ReadLine();

    Console.WriteLine(a1 * a3);
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

  int a1, a2, a3, a4; cin >> a1 >> a2 >> a3 >> a4;

  cout << a1 * a3 << "\n";

  return 0;
}
```
