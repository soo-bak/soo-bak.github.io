---
layout: single
title: "[백준 10973] 이전 순열 (C#, C++) - soo:bak"
date: "2025-05-06 01:54:00 +0900"
description: 사전순으로 바로 앞에 오는 순열을 계산하는 백준 10973번 이전 순열 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10973
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 조합론
keywords: "백준 10973, 백준 10973번, BOJ 10973, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10973번 - 이전 순열](https://www.acmicpc.net/problem/10973)

## 설명
주어진 수열에 대해 **사전순으로 바로 앞에 오는 순열을 찾는 문제**입니다.

<br>
`1`부터 시작하는 연속된 정수들로 이루어진 수열이 주어질 때,

이 수열을 기준으로 사전순으로 더 작은 순열 중에서 **가장 가까운 순열**을 출력합니다.

<br>
만약 현재 수열이 사전순으로 가장 앞서는 순열이라면, 즉, **모든 수가 오름차순 정렬된 상태**라면,

**더 이상 이전 순열이 존재하지 않기 때문에 `-1`을 출력**합니다.

<br>

## 접근법
- 수열의 뒤쪽에서부터 탐색하여, **감소하지 않는 가장 긴 구간**을 찾습니다.<br>
  이는 사전순으로 가장 뒤쪽에 있는 조합에 가까운지를 확인하기 위함입니다.

- 그 감소하지 않는 구간의 **바로 앞에 있는 원소**를 기준으로,<br>
  그 원소보다 **작은 값 중 가장 큰 값**을 뒤쪽에서 찾아 교환합니다.
- 이렇게 하면 현재 수열보다 **사전순으로 가장 가까운 더 작은 순열**을 만들 수 있습니다.

- 두 원소를 교환한 후, 그 뒤쪽 구간을 오름차순으로 정렬하면<br>
  가장 가까운 작은 순열이 완성됩니다.

- 만약 수열 전체가 오름차순이면, 더 이상 이전 순열이 존재하지 않으므로 `-1`을 출력합니다.

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
    var p = Console.ReadLine().Split().Select(int.Parse).ToArray();

    int i = n - 2;
    while (i >= 0 && p[i] <= p[i + 1])
      i--;

    if (i < 0) {
      Console.WriteLine("-1");
      return;
    }

    int j = n - 1;
    while (p[j] >= p[i])
      j--;

    (p[i], p[j]) = (p[j], p[i]);
    Array.Reverse(p, i + 1, n - i - 1);

    Console.WriteLine(string.Join(" ", p));
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

  int n; cin >> n;
  vi p(n);
  for (int i = 0; i < n; i++)
    cin >> p[i];

  int i = n - 2;
  while (i >= 0 && p[i] <= p[i + 1])
    i--;

  if (i < 0) cout << "-1\n";
  else {
    int j = n - 1;
    while (p[j] >= p[i])
      j--;

    swap(p[i], p[j]);

    reverse(p.begin() + i + 1, p.end());

    for (int k = 0; k < n; k++)
      cout << p[k] << (k < n - 1 ? " " : "\n");
  }

  return 0;
}
```
