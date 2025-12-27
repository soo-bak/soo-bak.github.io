---
layout: single
title: "[백준 9507] Generations of Tribbles (C#, C++) - soo:bak"
date: "2025-04-29 05:22:00 +0900"
description: 기존 피보나치 수열을 확장하여 앞선 네 항의 합을 이용하는 변형 수열을 계산하는 백준 9507번 Generations of Tribbles 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9507
  - C#
  - C++
  - 알고리즘
  - 다이나믹 프로그래밍
keywords: "백준 9507, 백준 9507번, BOJ 9507, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9507번 - Generations of Tribbles](https://www.acmicpc.net/problem/9507)

## 설명
`0`번째 항부터 `67`번째 항까지 정의된 수열에서, 주어진 항의 값을 구하는 문제입니다.

문제에서 정의된 수열은 기존의 피보나치 수열과 비슷하지만, 규칙이 조금 다르게 정의되어 있습니다:

- `n = 0` 또는 `n = 1`일 때는 `1`
- `n = 2`일 때는 `2`
- `n = 3`일 때는 `4`
- `n ≥ 4`일 때는 바로 앞의 네 항을 모두 더해 값을 계산합니다.

<br>
점화식은 다음과 같습니다:

$$
f(n) = f(n-1) + f(n-2) + f(n-3) + f(n-4)
$$


즉, 기존 피보나치 수열이 이전 두 항의 합으로 구성되는 것과 비교 했을 때,

이전 네 개의 항을 이용해 다음 항을 만드는 **피보나치 수열의 확장 형태** 입니다.

<br>
목표는 입력으로 주어지는 값 `n`에 대해, 이 수열의 `n`번째 항을 계산하여 출력하는 것입니다.

<br>

## 접근법

먼저, 수열의 초깃값인 `0`, `1`, `2`, `3`번째 항을 배열에 저장합니다.

그 이후부터는, 각 항을 앞선 네 항의 합으로 계산하여 배열을 채워나갑니다.

<br>
이렇게 미리 `0`부터 `67`까지의 초깃값을 모두 구해두면,

테스트케이스마다 입력된 `n`에 대해 중복 계산 없이 바로 값을 찾아 출력할 수 있습니다.

<br>
초기 계산은 $$O(N)$$, 각 테스트케이스는 $$O(1)$$ 의 시간 복잡도를 가집니다.



## Code

### C#

```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    long[] fibo = new long[68];
    fibo[0] = fibo[1] = 1;
    fibo[2] = 2;
    fibo[3] = 4;
    for (int i = 4; i < 68; i++)
      fibo[i] = fibo[i - 1] + fibo[i - 2] + fibo[i - 3] + fibo[i - 4];

    int t = int.Parse(Console.ReadLine());
    StringBuilder sb = new();
    while (t-- > 0)
      sb.AppendLine(fibo[int.Parse(Console.ReadLine())].ToString());

    Console.Write(sb.ToString());
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll fibo[68] = {1, 1, 2, 4, };
  for (int i = 4; i < 68; i++)
    fibo[i] = fibo[i - 1] + fibo[i - 2] + fibo[i - 3] + fibo[i - 4];

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    cout << fibo[n] << "\n";
  }

  return 0;
}
```
