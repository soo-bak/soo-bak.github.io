---
layout: single
title: "[백준 9461] 파도반 수열 (C#, C++) - soo:bak"
date: "2025-11-17 23:04:00 +0900"
description: 점화식 P(n)=P(n-1)+P(n-5)를 이용해 1≤n≤100 구간을 빠르게 계산하는 백준 9461번 파도반 수열 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 9461
  - C#
  - C++
  - 알고리즘
keywords: "백준 9461, 백준 9461번, BOJ 9461, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9461번 - 파도반 수열](https://www.acmicpc.net/problem/9461)

## 설명

파도반 수열은 정삼각형들을 나선 모양으로 채워나갈 때 각 삼각형의 변의 길이로 정의되는 수열입니다.<br>

수열의 초기값은 `P(1) = P(2) = P(3) = 1`, `P(4) = P(5) = 2`이며, `P(n) = P(n-1) + P(n-5)`의 점화식을 따릅니다.

예를 들어 `P(6) = P(5) + P(1) = 2 + 1 = 3`, `P(7) = P(6) + P(2) = 3 + 1 = 4`입니다.<br>

여러 개의 테스트 케이스가 주어지며, 각 케이스마다 `N (1 ≤ N ≤ 100)`이 주어질 때 `P(N)`을 출력해야 합니다.<br>

`N`이 `100`까지 커질 수 있으므로 `P(N)`의 값도 매우 커집니다.<br>

<br>

## 접근법

동적 프로그래밍을 사용하여 해결합니다.

파도반 수열은 나선형으로 삼각형을 배치할 때 `n`번째 삼각형의 변의 길이가 `n-1`번째와 `n-5`번째 삼각형의 변의 길이의 합이 되는 규칙을 따릅니다.

이를 식으로 나타내면 `P(n) = P(n-1) + P(n-5)`입니다.

<br>
기저 값은 `P(1) = P(2) = P(3) = 1`, `P(4) = P(5) = 2`로 설정합니다.

이후 `P(6)`부터는 점화식을 적용합니다.

예를 들어 `P(6) = P(5) + P(1) = 2 + 1 = 3`, `P(7) = P(6) + P(2) = 3 + 1 = 4`입니다.

<br>
`P(1)`부터 `P(100)`까지 미리 계산해 두면 각 테스트 케이스마다 O(1) 시간에 답할 수 있습니다.

`P(100)`은 `12,000,000,000`을 넘으므로 `long` 타입을 사용합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var padovan = new long[101];
      padovan[1] = padovan[2] = padovan[3] = 1;
      padovan[4] = padovan[5] = 2;
      for (var i = 6; i <= 100; i++)
        padovan[i] = padovan[i - 1] + padovan[i - 5];

      var t = int.Parse(Console.ReadLine()!);
      var answers = new long[t];
      for (var i = 0; i < t; i++) {
        var n = int.Parse(Console.ReadLine()!);
        answers[i] = padovan[n];
      }

      Console.WriteLine(string.Join("\n", answers));
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<long long> vll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vll padovan(101, 0);
  padovan[1] = padovan[2] = padovan[3] = 1;
  padovan[4] = padovan[5] = 2;
  for (int i = 6; i <= 100; ++i)
    padovan[i] = padovan[i - 1] + padovan[i - 5];

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    cout << padovan[n] << "\n";
  }

  return 0;
}
```

