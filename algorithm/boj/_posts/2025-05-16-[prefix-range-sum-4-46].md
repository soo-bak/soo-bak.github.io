---
layout: single
title: "[백준 11659] 구간 합 구하기 4 (C#, C++) - soo:bak"
date: "2025-05-16 22:14:00 +0900"
description: 수열에서 여러 구간의 합을 빠르게 구하기 위해 누적합을 활용하는 백준 11659번 구간 합 구하기 4 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11659
  - C#
  - C++
  - 알고리즘
keywords: "백준 11659, 백준 11659번, BOJ 11659, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11659번 - 구간 합 구하기 4](https://www.acmicpc.net/problem/11659)

## 설명

**주어진 수열에서 여러 구간의 합을 반복적으로 구해야 하는 문제입니다.**

총 `N`개의 수와 `M`개의 구간 쿼리가 주어졌을 때,

각 구간에 해당하는 수의 합을 빠르게 출력하는 것이 목표입니다.

문제의 조건상 `N`, `M` 모두 최대 `100,000`으로 매우 크기 때문에,

매 쿼리마다 단순히 반복문으로 합을 구하면 시간 초과가 발생하게 됩니다.

<br>

## 접근법

이 문제는 구간 합을 빠르게 계산하기 위한 **누적합(Prefix Sum)** 기법을 적용하면 효율적으로 해결할 수 있습니다.

<br>
수열의 앞에서부터 순서대로 누적해서 더해나간 값을 배열에 저장해 두면,

어떤 구간 `[i, j]`에 대해 다음처럼 한 번의 뺄셈으로 바로 합을 구할 수 있습니다.

예를 들어,
- `1`부터 `j`번째까지의 합: `sum[j]`
- `1`부터 `(i - 1)`번째까지의 합: `sum[i - 1]`

이 두 값을 빼면 `i부터 j까지의 구간 합`이 남습니다.

<br>
즉, 구간 `[i, j]`의 합은
$$
\text{sum}[j] - \text{sum}[i - 1]
$$

와 같이 계산할 수 있습니다.

<br>

> 참고 : [누적합(Prefix Sum)의 원리와 구간 합 계산 - soo:bak](https://soo-bak.github.io/algorithm/theory/prefix-sum/)

<br>

---

## Code

### C#
```csharp
using System;
using System.Linq;
using System.Text;

class Program {
  static void Main() {
    var nm = Console.ReadLine().Split().Select(int.Parse).ToArray();
    int n = nm[0], m = nm[1];

    var nums = Console.ReadLine().Split().Select(int.Parse).ToArray();
    var sum = new int[n + 1];
    for (int i = 1; i <= n; i++)
      sum[i] = sum[i - 1] + nums[i - 1];

    var sb = new StringBuilder();
    for (int i = 0; i < m; i++) {
      var range = Console.ReadLine().Split().Select(int.Parse).ToArray();
      int s = range[0], e = range[1];
      sb.AppendLine((sum[e] - sum[s - 1]).ToString());
    }

    Console.WriteLine(sb.ToString());
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

  int n, m; cin >> n >> m;

  vi sum(n + 1);
  for (int i = 1; i <= n; ++i) {
    int x; cin >> x;
    sum[i] = sum[i - 1] + x;
  }

  while (m--) {
    int s, e; cin >> s >> e;
    cout << sum[e] - sum[s - 1] << "\n";
  }

  return 0;
}
```
