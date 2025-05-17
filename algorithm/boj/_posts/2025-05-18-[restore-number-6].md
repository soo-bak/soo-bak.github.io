---
layout: single
title: "[백준 2312] 수 복원하기 (C#, C++) - soo:bak"
date: "2025-05-18 01:05:53 +0900"
description: 정수를 소인수분해하여 인수와 지수를 오름차순으로 출력하는 백준 2312번 수 복원하기 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[2312번 - 수 복원하기](https://www.acmicpc.net/problem/2312)

## 설명

**주어진 정수를 소인수분해하여, 각 인수와 해당 인수의 지수를 출력하는 문제입니다.**

- 입력으로 양의 정수 `N`이 주어집니다.
- 이를 소수의 곱으로 표현하고,
- 각 소인수와 그 인수가 곱해진 횟수를 출력합니다.

출력은 소인수 오름차순 순서로 구성되어야 하며,

동일한 인수는 한 번만 출력되어야 합니다.

<br>

## 접근법

소인수분해를 위해 먼저 일정 범위까지의 **소수를 에라토스테네스의 체**로 미리 구해둡니다.

이후 각 테스트케이스마다 입력된 수를 작은 소수부터 나누어가며,

해당 수가 몇 번씩 나누어지는지를 세어 소인수와 함께 출력합니다.

<br>
과정은 다음과 같습니다:

- 먼저 `1`부터 `100,000`까지의 소수를 미리 구해둡니다.
- 각 수 `n`에 대해 다음을 반복합니다:
  - 만약 `n`이 소수라면 `n 1`을 바로 출력합니다.
  - 그렇지 않다면, 작은 소수부터 차례대로 나누어가며:
    - 나눌 수 있을 때마다 횟수를 누적하고
    - 그 횟수를 함께 출력합니다.
- 모든 소수에 대해 나누기를 마치면 소인수분해가 완료됩니다.

<br>

> 참고 : [에라토스테네스의 체 (Sieve of Eratosthenes) - soo:bak](https://soo-bak.github.io/algorithm/theory/SieveOfEratosthenes/)

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    const int MAX = 100000;
    var isNotPrime = new bool[MAX + 1];
    isNotPrime[0] = isNotPrime[1] = true;

    for (int i = 2; i * i <= MAX; i++) {
      if (!isNotPrime[i]) {
        for (int j = i * i; j <= MAX; j += i)
          isNotPrime[j] = true;
      }
    }

    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      int n = int.Parse(Console.ReadLine());

      if (!isNotPrime[n]) {
        Console.WriteLine($"{n} 1");
        continue;
      }

      for (int i = 2; i <= n; i++) {
        if (!isNotPrime[i] && n % i == 0) {
          int count = 0;
          while (n % i == 0) {
            n /= i;
            count++;
          }
          Console.WriteLine($"{i} {count}");
        }
      }
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
#define MAX 100000
using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  bool sieve[MAX + 1] = {true, true};
  for (int i = 2; i * i <= MAX; ++i) {
    if (!sieve[i]) {
      for (int j = i * i; j <= MAX; j += i)
        sieve[j] = true;
    }
  }

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    if (!sieve[n]) {
      cout << n << " " << 1 << "\n";
      continue;
    }
    for (int i = 2; i <= n; ++i) {
      if (!sieve[i] && n % i == 0) {
        int cnt = 0;
        while (n % i == 0) {
          n /= i;
          ++cnt;
        }
        cout << i << " " << cnt << "\n";
      }
    }
  }

  return 0;
}
```
