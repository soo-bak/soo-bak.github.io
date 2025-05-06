---
layout: single
title: "[백준 10972] 다음 순열 (C#, C++) - soo:bak"
date: "2025-05-06 01:40:00 +0900"
description: 사전순으로 다음에 오는 순열을 계산하는 백준 10972번 다음 순열 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10972번 - 다음 순열](https://www.acmicpc.net/problem/10972)

## 설명
주어진 수열에 대해 **사전순으로 다음에 오는 순열을 찾는 문제**입니다.

<br>
`1`부터 시작하는 연속된 정수들로 이루어진 수열이 주어질 때,

이 수열을 기준으로 사전순으로 더 큰 순열 중에서 **가장 가까운 순열**을 출력합니다.

<br>
만약 현재 수열이 사전순으로 가장 마지막 순열이라면, 즉, **모든 수가 내림차순 정렬된 상태**라면,

**더 이상 다음 순열이 존재하지 않기 때문에** `-1`**을 출력**합니다.

<br>

## 접근법
- 먼저 수열의 뒤쪽에서부터 탐색하여, **증가하지 않는 가장 긴 구간**을 찾습니다.<br>
  이는 현재 수열이 정렬된 마지막 상태에 가까운지를 확인하기 위함입니다.  <br>
  → 해당 구간은 **다음 순열을 만들기 위해 정렬해야 하는 구간**입니다.<br>

- 그 증가하지 않는 구간의 **바로 앞에 있는 원소**를 기준으로,<br>
  그 원소보다 **큰 수 중 가장 오른쪽에 있는 수**를 찾습니다.  <br>
  → 이렇게 선택하는 이유는, 사전순으로 가장 근접한 다음 순열을 만들기 위해서입니다.

- 두 원소를 교환한 후, 그 뒤쪽 구간을 오름차순으로 정렬하면<br>
  사전순으로 바로 다음에 오는 순열이 완성됩니다.
- 만약 증가하지 않는 구간이 수열 전체라면, 이미 마지막 순열이므로 `-1`을 출력합니다.

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

    int k = -1;
    for (int i = n - 2; i >= 0; i--) {
      if (p[i] < p[i + 1]) {
        k = i;
        break;
      }
    }

    if (k == -1) {
      Console.WriteLine("-1");
      return;
    }

    int l = n - 1;
    while (p[l] <= p[k])
      l--;

    (p[k], p[l]) = (p[l], p[k]);
    Array.Reverse(p, k + 1, n - k - 1);

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

  int k = -1;
  for (int i = n - 2; i >= 0; i--) {
    if (p[i] < p[i + 1]) {
      k = i;
      break;
    }
  }

  if (k == -1) cout << "-1\n";
  else {
    int l = n - 1;
    while (p[l] <= p[k])
      l--;

    swap(p[k], p[l]);

    reverse(p.begin() + k + 1, p.end());

    for (int i = 0; i < n; i++)
      cout << p[i] << (i < n - 1 ? " " : "\n");
  }

  return 0;
}
```
