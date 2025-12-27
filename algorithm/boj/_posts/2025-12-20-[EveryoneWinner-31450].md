---
layout: single
title: "[백준 31450] Everyone is a winner (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 31450번 C#, C++ 풀이 - 메달 수를 아이들 수로 정확히 나눌 수 있는지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 31450
  - C#
  - C++
  - 알고리즘
keywords: "백준 31450, 백준 31450번, BOJ 31450, EveryoneWinner, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31450번 - Everyone is a winner](https://www.acmicpc.net/problem/31450)

## 설명
메달을 아이들에게 똑같이 나눠줄 수 있는지 판별하는 문제입니다.

<br>

## 접근법
메달 수를 아이 수로 나눈 나머지가 0이면 균등하게 분배할 수 있고, 그렇지 않으면 불가능합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var m = int.Parse(parts[0]);
    var k = int.Parse(parts[1]);

    Console.WriteLine(m % k == 0 ? "Yes" : "No");
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

  int m, k; cin >> m >> k;

  cout << ((m % k == 0) ? "Yes" : "No") << "\n";

  return 0;
}
```
