---
layout: single
title: "[백준 6810] ISBN (C#, C++) - soo:bak"
date: "2025-11-23 03:15:00 +0900"
description: 앞의 10자리가 고정된 ISBN에서 1-3-sum 규칙을 활용해 상수 91에 마지막 세 자리의 가중치를 더해 결과를 구하는 백준 6810번 ISBN 문제의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 6810
  - C#
  - C++
  - 알고리즘
keywords: "백준 6810, 백준 6810번, BOJ 6810, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6810번 - ISBN](https://www.acmicpc.net/problem/6810)

## 설명

ISBN-13의 `1-3-sum`은 13자리 각각에 1과 3을 번갈아가며 곱한 후 모두 더한 값입니다.

첫 번째 자리는 1을 곱하고, 두 번째는 3을 곱하는 식으로 반복합니다.

앞 10자리가 `9780921418`로 고정된 상황에서 마지막 3자리가 주어질 때, 전체 13자리의 `1-3-sum`을 구하는 문제입니다.

<br>

## 접근법

고정된 앞 10자리 `9780921418`의 `1-3-sum`을 미리 계산하면 91입니다.

<br>
입력으로 주어지는 11, 12, 13번째 자리에는 각각 1, 3, 1을 곱합니다.

이 세 값을 합한 후 91을 더하면 전체 13자리의 `1-3-sum`이 됩니다.

<br>
출력 형식은 `The 1-3-sum is X` 형태로 지정되어 있으므로 문자열을 맞춰 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      const int baseSum = 91;

      var d11 = int.Parse(Console.ReadLine()!);
      var d12 = int.Parse(Console.ReadLine()!);
      var d13 = int.Parse(Console.ReadLine()!);

      var total = baseSum + d11 * 1 + d12 * 3 + d13 * 1;

      Console.WriteLine($"The 1-3-sum is {total}");
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

  const int baseSum = 91;
  int d11, d12, d13;
  cin >> d11 >> d12 >> d13;

  int total = baseSum + d11 * 1 + d12 * 3 + d13 * 1;

  cout << "The 1-3-sum is " << total << "\n";

  return 0;
}
```

