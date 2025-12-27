---
layout: single
title: "[백준 2960] 에라토스테네스의 체 (C#, C++) - soo:bak"
date: "2025-04-14 04:35:43 +0900"
description: 소수를 체로 거르는 과정에서 K번째로 지워지는 수를 추적하는 백준 2960번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2960
  - C#
  - C++
  - 알고리즘
keywords: "백준 2960, 백준 2960번, BOJ 2960, eratosthenesKill, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2960번 - 에라토스테네스의 체](https://www.acmicpc.net/problem/2960)

## 설명
이 문제는 소수를 찾기 위해 사용하는 **에라토스테네스의 체 알고리듬**을 구현하면서,  <br>
그 과정에서 **K번째로 지워지는 수**를 구하는 시뮬레이션 문제입니다.

---

## 접근법
- `2`부터 `N`까지 순서대로 지워나가며, **소수가 아닌 수들을 지울 때마다 카운트**를 올립니다.
- 각 수 `i`가 아직 지워지지 않았고, `i`의 배수들을 순서대로 지울 때 `K`번째가 되면 해당 값을 출력합니다.
- 에라토스테네스의 체는 일반적으로 **소수를 남기는 과정**이지만, 이 문제에서는 **지우는 순서**를 추적해야 합니다.

<br>

> 참고 : [에라토스테네스의 체 (Sieve of Eratosthenes) - soo:bak](https://soo-bak.github.io/algorithm/theory/SieveOfEratosthenes/)

<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var input = Console.ReadLine()!.Split();
      int n = int.Parse(input[0]);
      int k = int.Parse(input[1]);

      var sieve = new bool[n + 1];
      int cnt = 0;

      for (int i = 2; i <= n; i++) {
        for (int j = i; j <= n; j += i) {
          if (!sieve[j]) {
            sieve[j] = true;
            cnt++;
            if (cnt == k) {
              Console.WriteLine(j);
              return;
            }
          }
        }
      }
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

  int n, k; cin >> n >> k;
  int* sieve = new int[n + 1];
  fill_n(sieve, n, 0);

  int cnt = 0;
  for (int i = 2; i <= n; i++) {
    for (int j = 2; j <= n; j++) {
      if (!sieve[j] && j % i == 0) {
        sieve[j] = 1;
        cnt++;
        if (cnt == k) cout << j << "\n";
      }
    }
  }

  return 0;
}
```
