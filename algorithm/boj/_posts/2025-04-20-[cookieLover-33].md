---
layout: single
title: "[백준 11134] 쿠키애호가 (C#, C++) - soo:bak"
date: "2025-04-20 04:29:00 +0900"
description: 하루에 먹을 수 있는 쿠키 수에 따라 며칠 동안 나누어 먹어야 하는지를 계산하는 백준 11134번 쿠키애호가 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[11134번 - 쿠키애호가](https://www.acmicpc.net/problem/11134)

## 설명
**쿠키의 총 개수와 하루에 먹을 수 있는 개수가 주어졌을 때, 모든 쿠키를 먹는 데 필요한 최소 일수를 구하는 문제입니다.**
<br>

- 각 테스트케이스마다 다음 두 개의 정수가 주어집니다:
  - 쿠키의 총 개수
  - 하루에 먹을 수 있는 쿠키 개수
- 하루에 먹을 수 있는 수만큼 매일 먹을 수 있으며,<br>
  만약, 먹을 수 있는 수 미만의 쿠키가 남아있다면 전부 먹습니다.
- 모든 쿠키를 먹을 때까지 며칠이 걸리는지를 계산합니다.


## 접근법

- 테스트케이스 수를 입력받습니다.
- 각 테스트케이스마다 **쿠키의 전체 개수**와 **하루에 먹을 수 있는 양**을 입력받습니다.
- 모든 쿠키를 먹기 위해 필요한 최소 일수는 다음과 같이 계산됩니다:
  - 하루에 `k`개씩 먹을 수 있을 때, 매일 최대치로 먹는다고 가정해도 `총 개수 ÷ k`일이 걸립니다.
  - 그런데 딱 나누어떨어지지 않는 경우에는, **쿠키가 일부 남아 있는 상태로 하루가 더 필요합니다.**
- 예를 들어, `10`개의 쿠키를 하루에 `3`개씩 먹으면 `3일 동안 9개`만 먹게 되며, `1`개가 남기 때문에 `4일`이 필요합니다.
- 전체 쿠키를 하루에 먹을 수 있는 양으로 나눈 값에 대해,<br>
  남는 쿠키가 있을 경우 하루가 더 필요하므로 최소 일수는 이 값을 올림한 결과로 계산해야 합니다.

- 실수형 계산을 사용하지 않고도, 다음과 같은 수식을 통해 정수 연산으로 올림 연산을 간단히 처리할 수 있습니다 :

  $$
  \left\lfloor \frac{\text{총 쿠키 수} + (\text{하루 섭취량} - 1)}{\text{하루 섭취량}} \right\rfloor
  $$

  분자에 하루 섭취량에서 1을 뺀 값을 더함으로써, 나눗셈 결과가 정수로 나누어떨어지지 않을 경우에도 올림 처리가 이루어지게 됩니다.

- 모든 테스트는 `O(1)` 연산으로 처리되며, 테스트케이스 수만큼 반복되므로 전체 시간 복잡도는 `O(n)`입니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int testCount = int.Parse(Console.ReadLine());
    while (testCount-- > 0) {
      var parts = Console.ReadLine().Split();
      int total = int.Parse(parts[0]);
      int perDay = int.Parse(parts[1]);

      Console.WriteLine((total + (perDay - 1)) / perDay);
    }
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

  int t; cin >> t;
  while (t--) {
    int day, cookie; cin >> day >> cookie;
    cout << (day + (cookie - 1)) / cookie << "\n";
  }

  return 0;
}
```
