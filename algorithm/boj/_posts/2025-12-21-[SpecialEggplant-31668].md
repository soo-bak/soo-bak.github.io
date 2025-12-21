---
layout: single
title: "[백준 31668] 특별한 가지 (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 파묻튀밥 총량을 구해 같은 줄 수만큼 K그램 가지를 준비하는 최소 필요량을 계산하는 문제
---

## 문제 링크
[31668번 - 특별한 가지](https://www.acmicpc.net/problem/31668)

## 설명
파묻튀밥 한 줄에 들어가는 파묻튀 양과 총 사용량, 가지로 대체할 때 한 줄당 필요한 가지 양이 주어질 때, 전체 가지 필요량을 구하는 문제입니다.

<br>

## 접근법
제작한 파묻튀밥 줄 수는 총 사용량을 한 줄당 양으로 나눈 값입니다. 각 줄에 필요한 가지 양을 곱하면 총 필요한 가지를 구할 수 있습니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var m = int.Parse(Console.ReadLine()!);
    var k = int.Parse(Console.ReadLine()!);

    var rolls = m / n;
    Console.WriteLine(rolls * k);
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

  int n, m, k; cin >> n >> m >> k;

  int rolls = m / n;
  cout << rolls * k << "\n";

  return 0;
}
```
