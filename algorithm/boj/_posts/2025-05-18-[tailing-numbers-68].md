---
layout: single
title: "[백준 1598] 꼬리를 무는 숫자 나열 (C#, C++) - soo:bak"
date: "2025-05-18 20:48:00 +0900"
description: 4열로 구성된 수직 배열에서 두 수 간의 직각거리를 계산하는 백준 1598번 꼬리를 무는 숫자 나열 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1598
  - C#
  - C++
  - 알고리즘
keywords: "백준 1598, 백준 1598번, BOJ 1598, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1598번 - 꼬리를 무는 숫자 나열](https://www.acmicpc.net/problem/1598)

## 설명

숫자들을 위에서 아래로 `4열`에 나누어 나열한 뒤,

그 배열 내에서 두 수의 위치를 기준으로 **직각거리**를 계산하는 문제입니다.

<br>
숫자는 `4열` 구조로 `세로 방향`으로 차례로 배치됩니다.

예를 들어 다음과 같습니다:

```
1  5  9  13 ...
2  6 10  14 ...
3  7 11  15 ...
4  8 12  16 ...
```

<br>

## 접근법

먼저 입력으로 주어진 두 자연수 각각의 좌표를 계산합니다.

<br>
숫자판은 `4열 구조`이므로,
- `(값 - 1) / 4`를 통해 세로 방향(행)
- `(값 - 1) % 4`를 통해 가로 방향(열)을 구할 수 있습니다.

<br>
그 후 두 좌표의 행 차이와 열 차이를 각각 구해 더하면 직각거리(맨해튼 거리)가 됩니다:

- 세로 거리 = $$\lvert r_2 - r_1\rvert$$
- 가로 거리 = $$\lvert c_2 - c_1\rvert$$
- 직각 거리 = $$\lvert r_2 - r_1\rvert + \lvert c_2 - c_1\rvert$$

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var tokens = Console.ReadLine().Split();
    int n1 = int.Parse(tokens[0]);
    int n2 = int.Parse(tokens[1]);

    int r1 = (n1 - 1) / 4, c1 = (n1 - 1) % 4;
    int r2 = (n2 - 1) / 4, c2 = (n2 - 1) % 4;

    int distance = Math.Abs(r2 - r1) + Math.Abs(c2 - c1);
    Console.WriteLine(distance);
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

  int n1, n2; cin >> n1 >> n2;
  int r1 = (n1 - 1) / 4, c1 = (n1 - 1) % 4;
  int r2 = (n2 - 1) / 4, c2 = (n2 - 1) % 4;
  cout << abs(r2 - r1) + abs(c2 - c1) << "\n";

  return 0;
}
```
