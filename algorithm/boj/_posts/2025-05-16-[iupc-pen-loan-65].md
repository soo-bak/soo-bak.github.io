---
layout: single
title: "[백준 12788] 제 2회 IUPC는 잘 개최될 수 있을까? (C#, C++) - soo:bak"
date: "2025-05-16 22:00:00 +0900"
description: 펜이 필요한 팀 참가자 수를 고려해 최소한의 회원에게 펜을 빌리는 백준 12788번 IUPC 개최 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 12788
  - C#
  - C++
  - 알고리즘
keywords: "백준 12788, 백준 12788번, BOJ 12788, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12788번 - 제 2회 IUPC는 잘 개최될 수 있을까?](https://www.acmicpc.net/problem/12788)

## 설명

**여러 명의 팀 참가자에게 펜을 나누기 위해, 최소한의 사람에게 펜을 빌리는 문제입니다.**

각 회원은 서로 다른 수의 펜을 가지고 있으며,

경시대회에 참가하는 팀원 전체에게 펜을 나눠줘야 합니다.

- 팀 수 `m`와 팀당 인원 수 `k`가 주어졌을 때,<br>
  필요한 펜의 총 수는 `m × k`입니다.
- 펜을 빌릴 회원의 수를 최소로 하되, 펜이 부족하면 `"STRESS"`를 출력합니다.

<br>

## 접근법

펜의 수가 많은 회원부터 차례대로 펜을 빌리는 방식으로 문제를 해결할 수 있습니다.

1. 먼저 회원들이 가진 펜의 수를 내림차순으로 정렬합니다.
2. 가장 많은 사람부터 펜을 빌려가며, 누적한 펜의 수가 `m × k` 이상이 되는 시점을 찾습니다.
3. 이때까지 동원된 회원 수가 정답이 됩니다.
4. 만약 펜을 모두 빌려도 부족하다면 `"STRESS"`를 출력합니다.

<br>
이 문제는 **그리디 알고리듬**으로 해결할 수 있으며, 핵심은 "적은 인원에게서 최대한 많이 빌리는 전략"입니다.

<br>

> 참고 : [그리디 알고리듬(Greedy Algorithm, 탐욕법)의 원리와 적용 - soo:bak](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)

<br>

---

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var tokens = Console.ReadLine().Split();
    int t = int.Parse(tokens[0]), m = int.Parse(tokens[1]);

    int totalNeed = t * m;
    var pens = Console.ReadLine().Split().Select(int.Parse)
      .OrderByDescending(x => x).ToArray();

    int sum = 0, count = 0;
    foreach (var x in pens) {
      sum += x;
      count++;
      if (sum >= totalNeed) {
        Console.WriteLine(count);
        return;
      }
    }

    Console.WriteLine("STRESS");
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

  int n, t, m; cin >> n >> t >> m;

  vi cases(n);
  for (int& x : cases)
    cin >> x;

  sort(cases.rbegin(), cases.rend());

  int sum = 0, count = 0;
  for (int x : cases) {
    sum += x;
    ++count;
    if (sum >= t * m) {
      cout << count << "\n";
      return 0;
    }
  }

  cout << "STRESS\n";

  return 0;
}
```
