---
layout: single
title: "[백준 2863] 이게 분수? (C#, C++) - soo:bak"
date: "2025-05-18 02:03:24 +0900"
description: 2x2 표의 회전 상태 중 가장 큰 분수 값을 만드는 회전 횟수를 구하는 백준 2863번 이게 분수? 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2863
  - C#
  - C++
  - 알고리즘
keywords: "백준 2863, 백준 2863번, BOJ 2863, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2863번 - 이게 분수?](https://www.acmicpc.net/problem/2863)

## 설명

`2 x 2` **형태의 수들을 이용해 정의된 분수 값을 회전하며 비교하여, 가장 큰 값을 만드는 회전 횟수를 찾는 문제입니다.**

표의 구성은 다음과 같습니다:

```
A B
C D
```

<br>
이 때, 표의 값은 $$\frac{A}{C} + \frac{B}{D}$$로 정의됩니다.

이 표를 **90도씩 시계 방향으로 회전**할 수 있으며,

총 `0`, `1`, `2`, `3`번 회전한 상태 중 **가장 큰 값을 만드는 회전 횟수**를 구해야 합니다.

<br>

## 접근법

- 표의 상태는 `90도`씩 총 `4번` 회전 가능한 구조이므로, `4번` 반복하며 모든 경우를 확인합니다.
- 각 회전마다 다음의 값을 계산합니다:
  $$
  \frac{왼쪽 위}{왼쪽 아래} + \frac{오른쪽 위}{오른쪽 아래}
  $$
- 이때, 실제 값이 가장 큰 회전 상태를 기억해두고 그 회전 횟수를 정답으로 출력합니다.
- 회전은 좌표를 시계 방향으로 바꾸는 방식으로 처리합니다:
  - 즉, `a b` → `c a` → `d c` → `b d` 순으로 회전합니다.

입력 수의 범위가 작기 때문에, 단순한 완전탐색 방식으로 충분히 처리할 수 있습니다.

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var input1 = Console.ReadLine().Split();
    var input2 = Console.ReadLine().Split();

    double[,] grid = new double[2, 2];
    grid[0, 0] = double.Parse(input1[0]);
    grid[0, 1] = double.Parse(input1[1]);
    grid[1, 0] = double.Parse(input2[0]);
    grid[1, 1] = double.Parse(input2[1]);

    double maxVal = -1;
    int answer = 0;

    for (int i = 0; i < 4; i++) {
      double val = grid[0, 0] / grid[1, 0] + grid[0, 1] / grid[1, 1];
      if (val > maxVal) {
        maxVal = val;
        answer = i;
      }

      double temp = grid[0, 0];
      grid[0, 0] = grid[1, 0];
      grid[1, 0] = grid[1, 1];
      grid[1, 1] = grid[0, 1];
      grid[0, 1] = temp;
    }

    Console.WriteLine(answer);
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

  double arr[2][2];
  for (int i = 0; i < 2; ++i) {
    for (int j = 0; j < 2; ++j)
      cin >> arr[i][j];
  }

  double maxV = -1, val;
  int ans = 0;
  for (int i = 0; i < 4; ++i) {
    val = arr[0][0] / arr[1][0] + arr[0][1] / arr[1][1];
    if (val > maxV) {
      maxV = val;
      ans = i;
    }

    double temp = arr[0][0];
    arr[0][0] = arr[1][0];
    arr[1][0] = arr[1][1];
    arr[1][1] = arr[0][1];
    arr[0][1] = temp;
  }

  cout << ans << "\n";

  return 0;
}
```
