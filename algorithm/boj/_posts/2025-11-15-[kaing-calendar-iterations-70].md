---
layout: single
title: "[백준 6064] 카잉 달력 (C#, C++) - soo:bak"
date: "2025-11-15 01:15:00 +0900"
description: 카잉 달력 표현 <x:y>가 몇 번째 해인지 M,N의 LCM까지 반복하며 찾는 백준 6064번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[6064번 - 카잉 달력](https://www.acmicpc.net/problem/6064)

## 설명

카잉 달력은 두 개의 숫자 `M`과 `N`을 기반으로 각 해를 `<x:y>` 형태로 표현하는 달력 체계입니다.<br>

해마다 `x`는 `1`부터 `M`까지, `y`는 `1`부터 `N`까지 순환하며 증가합니다. 예를 들어 `M = 10`, `N = 12`일 때, 1년은 `<1:1>`, 2년은 `<2:2>`, ... 10년은 `<10:10>`, 11년은 `<1:11>`, 12년은 `<2:12>`, 13년은 `<3:1>`이 됩니다.<br>

이 달력은 `M`과 `N`의 최소공배수(LCM) 번째 해가 되면 다시 `<1:1>`로 돌아옵니다. 즉, 마지막 해는 `<M:N>`입니다.<br>

이 상황에서 `M`, `N`, `x`, `y`가 주어질 때, `<x:y>`가 몇 번째 해인지 구하는 문제입니다.

해당하는 해가 존재하지 않으면 `-1`을 출력합니다.<br>

<br>

## 접근법

반복문을 사용하여 조건을 만족하는 해를 찾습니다.

먼저 `M`과 `N`의 최소공배수(LCM)를 계산합니다. 카잉 달력의 마지막 해는 `LCM(M, N)`이므로 이 값을 넘어가면 해가 존재하지 않습니다.

<br>
연도는 `x`부터 시작하여 `M`씩 증가시키며 탐색합니다. `k = x, x + M, x + 2M, ...` 형태로 반복하면 `k`를 `M`으로 나눈 나머지가 항상 `x`가 됩니다.

<br>
각 `k`에 대해 `k`를 `N`으로 나눈 나머지를 계산하여 `y`와 일치하는지 확인합니다. 카잉 달력은 `1`부터 시작하므로 나머지가 `0`이면 `N`으로 취급합니다.

<br>
조건을 만족하는 `k`를 찾으면 해당 값을 출력하고, LCM을 넘어도 찾지 못하면 `-1`을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static int Gcd(int a, int b) => b == 0 ? a : Gcd(b, a % b);

    static void Main(string[] args) {
      var t = int.Parse(Console.ReadLine()!);
      var outputs = new int[t];

      for (var i = 0; i < t; i++) {
        var tokens = Console.ReadLine()!.Split();
        var m = int.Parse(tokens[0]);
        var n = int.Parse(tokens[1]);
        var x = int.Parse(tokens[2]);
        var y = int.Parse(tokens[3]);

        var lcm = m / Gcd(m, n) * n;
        var year = x;

        while (year <= lcm) {
          var cy = year % n == 0 ? n : year % n;
          if (cy == y) break;
          year += m;
        }

        outputs[i] = year > lcm ? -1 : year;
      }

      Console.WriteLine(string.Join("\n", outputs));
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int gcd(int a, int b) {
  while (b) {
    int t = a % b;
    a = b;
    b = t;
  }
  return a;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int m, n, x, y; cin >> m >> n >> x >> y;
    int lcm = m / gcd(m, n) * n;
    int year = x, answer = -1;

    while (year <= lcm) {
      int cy = year % n;
      if (cy == 0) cy = n;
      if (cy == y) {
        answer = year;
        break;
      }
      year += m;
    }

    cout << answer << "\n";
  }

  return 0;
}
```

