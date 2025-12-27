---
layout: single
title: "[백준 3058] 짝수를 찾아라 (C#, C++) - soo:bak"
date: "2025-04-17 00:26:43 +0900"
description: 주어진 7개의 수 중 짝수만 골라 합과 최소값을 구하는 백준 3058번 짝수를 찾아라 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 3058
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 3058, 백준 3058번, BOJ 3058, findEvenSumMin, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3058번 - 짝수를 찾아라](https://www.acmicpc.net/problem/3058)

## 설명
**7개의 자연수 중 짝수만을 골라, 그 합과 최솟값을 출력하는 단순한 필터링 문제**입니다.<br>
<br>

- 각 테스트케이스마다 `7`개의 자연수가 주어집니다.<br>
- 이 중 **짝수인 수들만 골라** 그 **총합과 최솟값**을 출력해야 합니다.<br>

### 접근법
- 7개의 수를 반복하여 입력받으며, 짝수인 경우만 처리합니다.<br>
- 짝수의 경우 누적합에 더하고, 동시에 최솟값 갱신도 함께 수행합니다.<br>
- 테스트케이스마다 결과를 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var nums = Console.ReadLine().Split().Select(int.Parse);
      int sum = 0;
      int min = int.MaxValue;

      foreach (var num in nums) {
        if (num % 2 == 0) {
          sum += num;
          if (num < min) min = num;
        }
      }
      Console.WriteLine($"{sum} {min}");
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int min = 100, sum = 0;
    for (int i = 0; i < 7; i++) {
      int num; cin >> num;
      if (num % 2 == 0) {
        sum += num;
        if (min > num) min = num;
      }
    }
    cout << sum << " " << min << "\n";
  }

  return 0;
}
```
