---
layout: single
title: "[백준 2526] 싸이클 (C++, C#) - soo:bak"
date: "2025-05-17 07:51:16 +0900"
description: 주어진 연산을 반복했을 때 순환이 시작되는 부분의 길이를 구하는 백준 2526번 싸이클 문제의 C++ 및 C# 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2526
  - C#
  - C++
  - 알고리즘
keywords: "백준 2526, 백준 2526번, BOJ 2526, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2526번 - 싸이클](https://www.acmicpc.net/problem/2526)

## 설명

**정해진 연산을 반복했을 때, 반복 구간에 포함되는 서로 다른 수의 개수를 구하는 문제입니다.**

처음에는 어떤 자연수 `N`이 주어지고, 이후의 수열은 다음과 같이 생성됩니다:

- 현재 값에 `N`을 곱한 뒤, `P`로 나눈 나머지를 다음 수로 사용

이 과정을 반복하면 결국 **어떤 시점부터는 수열이 순환하게 됩니다.**

문제는 이 **순환 구간에 포함된 서로 다른 수의 개수**를 구하는 것입니다.

<br>

## 접근법

이 문제는 특정 연산을 반복할 때 발생하는 수열에서, 순환 구간에 포함된 서로 다른 수의 개수를 구하는 문제입니다.

<br>
수열은 아래 규칙으로 생성됩니다:
- 시작은 `N`으로 고정됩니다.
- 이후에는 이전 값에 `N`을 곱하고, 그 결과를 `P`로 나눈 나머지를 다음 값으로 사용합니다.

이렇게 생성되는 수열은 유한한 수의 상태만 가질 수 있기 때문에,

언젠가는 이전에 등장한 수가 다시 등장하게 되어 순환이 시작됩니다.

<br>
순환 구간의 서로 다른 수의 개수를 구하기 위해서는 다음과 같은 방식으로 처리합니다:
- 각 수가 처음 등장한 위치를 기록해둡니다.
- 이미 등장했던 수가 다시 나타나면, 그 수가 처음 등장했던 이후부터 지금까지 생성된 수들 중 반복되는 부분입니다.
- 이때 등장 위치 정보를 바탕으로, 반복되는 구간에 어떤 값들이 등장했는지를 탐색하여 중복 없이 집합 형태로 기록합니다.

집합에 포함된 값들의 개수가 곧 정답이 됩니다.

<br>

> 참고 : [순열 반복 구조(Permutation Cycle)의 개념과 알고리듬적 활용 - soo:bak](https://soo-bak.github.io/algorithm/theory/middle-square-algorithm/)

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var tokens = Console.ReadLine().Split();
    int n = int.Parse(tokens[0]);
    int p = int.Parse(tokens[1]);

    var seen = new int[1001];
    int val = n, order = 0;
    while (seen[val] == 0) {
      seen[val] = ++order;
      val = val * n % p;
    }

    Console.WriteLine(order - seen[val] + 1);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, p; cin >> n >> p;
  vi seen(1001);
  int val = n, order = 0;
  while (!seen[val]) {
    seen[val] = ++order;
    val = val * n % p;
  }
  cout << order - seen[val] + 1 << "\n";
  return 0;
}
```
