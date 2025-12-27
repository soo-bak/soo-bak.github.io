---
layout: single
title: "[백준 2997] 네 번째 수 (C#, C++) - soo:bak"
date: "2025-05-05 03:14:00 +0900"
description: 등차수열의 성질을 활용하여 누락된 하나의 수를 찾는 백준 2997번 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2997
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 2997, 백준 2997번, BOJ 2997, fourthnumber, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2997 - 네 번째 수](https://www.acmicpc.net/problem/2997)

## 설명

등차수열을 이루는 정수 `4개` 중 `1개`가 누락된 상태에서,

**나머지 `3개`의 수가 주어졌을 때 빠진 `1개`의 수를 찾아내는 문제**입니다.

<br>
주어진 수는 정렬되지 않은 상태일 수 있지만, 문제에서 주어진 조건에 따라 **항상 등차수열을 구성할 수** 있습니다.

<br>

## 접근법

- 우선, 주어진 세 수를 `오름차순`으로 정렬합니다.
- 정렬된 세 수를 기준으로, 앞과 뒤의 차이를 각각 계산합니다:
  - `앞쪽 차이` = `두 번째 수` − `첫 번째 수`
  - `뒤쪽 차이` = `세 번째 수` − `두 번째 수`
- 세 수 사이의 차이가 동일한 경우 등차수열의 **마지막 수가 누락된 것**입니다.
- 만약 두 차이가 다른 경우:
  - 뒤쪽 차이가 작다면 가운데 수가 누락된 경우입니다.
    따라서, **첫 번째 수에 뒤쪽 차이를 공차로 더한 값**이 정답입니다.
  - 반대로 앞쪽 차이가 작다면 마지막 수가 빠진 경우입니다.
    따라서, **두 번째 수에 앞쪽 차이를 공차로 더한 값**이 정답입니다.
- 문제 조건상 정답은 반드시 존재하며, 복수의 정답이 가능할 경우 어느 하나를 출력해도 정답으로 처리됩니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split().Select(int.Parse).ToArray();
    Array.Sort(input);

    var d1 = input[1] - input[0];
    var d2 = input[2] - input[1];

    if (d1 == d2) Console.WriteLine(input[2] + d1);
    else if (2 * d2 == d1) Console.WriteLine(input[0] + d2);
    else Console.WriteLine(input[1] + d1);
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

  int a[3];
  cin >> a[0] >> a[1] >> a[2];

  sort(a, a + 3);

  int d1 = a[1] - a[0], d2 = a[2] - a[1];

  if (d1 == d2) cout << a[2] + d1;
  else if (2 * d2 == d1) cout << a[0] + d2;
  else cout << a[1] + d1;

  cout << "\n";

  return 0;
}
```
