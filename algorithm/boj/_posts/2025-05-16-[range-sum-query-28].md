---
layout: single
title: "[백준 11441] 합 구하기 (C#, C++) - soo:bak"
date: "2025-05-16 22:10:00 +0900"
description: 여러 구간의 합을 빠르게 구하기 위해 누적합을 활용하는 백준 11441번 합 구하기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11441
  - C#
  - C++
  - 알고리즘
keywords: "백준 11441, 백준 11441번, BOJ 11441, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11441번 - 합 구하기](https://www.acmicpc.net/problem/11441)

## 설명

**수열에서 여러 구간의 합을 빠르게 구하는 문제입니다.**

총 `N`개의 정수가 주어지고,

그 후 `M`개의 구간 쿼리가 입력됩니다.

<br>
각 쿼리는 구간 `[i, j]`가 주어졌을 때,

해당 구간에 포함된 모든 수의 합을 구해서 출력하는 것이 목표입니다.

<br>
문제에서 주어지는 조건은 다음과 같습니다:

- 수의 개수 `N`은 최대 `100,000`개
- 구간의 개수 `M`도 최대 `100,000`개

따라서 각 쿼리마다 단순 반복문으로 합을 구한다면 전체 시간 초과가 발생하게 됩니다.

<br>

## 접근법

전체 수열에서 여러 구간의 합을 반복해서 구해야 하는 경우,

매번 처음부터 수열 전체를 차례대로 더하는 방식은 너무 느릴 수밖에 없습니다.

<br>
이 때, 수열의 앞부분부터 차곡차곡 누적해서 합을 미리 저장해두면,

어떤 구간이든 두 값을 뺄셈만으로 빠르게 계산할 수 있습니다.

<br>
예를 들어 `3번째`부터 `6번째`까지의 합이 필요할 때,

`1 ~ 6까지의 합`에서 `1 ~ 2까지의 합`을 빼주면 바로 원하는 구간의 합이 나오게 됩니다.

이렇게 미리 누적된 합을 활용해 구간 합을 빠르게 구하는 방식을 누적합(Prefix Sum)이라고 부릅니다.

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
    int n = int.Parse(Console.ReadLine());
    var numbers = Console.ReadLine().Split().Select(int.Parse).ToArray();

    var sum = new int[n + 1];
    for (int i = 1; i <= n; i++)
      sum[i] = sum[i - 1] + numbers[i - 1];

    int m = int.Parse(Console.ReadLine());
    var sb = new StringBuilder();
    for (int i = 0; i < m; i++) {
      var parts = Console.ReadLine().Split().Select(int.Parse).ToArray();
      int s = parts[0], e = parts[1];
      sb.AppendLine((sum[e] - sum[s - 1]).ToString());
    }
    Console.Write(sb.ToString());
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
  vi sum(n + 1);
  for (int i = 1; i <= n; ++i) {
    int x; cin >> x;
    sum[i] = sum[i - 1] + x;
  }

  int m; cin >> m;
  while (m--) {
    int s, e; cin >> s >> e;
    cout << sum[e] - sum[s - 1] << "\n";
  }

  return 0;
}
```
