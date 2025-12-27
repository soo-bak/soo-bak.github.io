---
layout: single
title: "[백준 33572] 자세히 보아야 예쁘다 (C#, C++) - soo:bak"
date: "2025-05-15 00:02:00 +0900"
description: 친구별 제한 시간을 넘기지 않도록 M시간을 배정할 수 있는지를 판단하는 백준 33572번 자세히 보아야 예쁘다 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 33572
  - C#
  - C++
  - 알고리즘
keywords: "백준 33572, 백준 33572번, BOJ 33572, lookclosely, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[33572번 - 자세히 보아야 예쁘다](https://www.acmicpc.net/problem/33572)

## 설명
`N` **명의 친구와 함께 총** `M`**시간을 보내야 할 때, 주어진 조건에 따라 시간을 배분할 수 있는지 판단**하는 문제입니다.

각 친구는 최대 `A_i`시간까지만 함께할 수 있습니다.

재원이는 항상 누군가와 함께 있어야 하며, 매 시간마다 친구를 바꿔볼 수 있지만, 한 친구와 너무 오래 있으면 퇴학당합니다.

<br>

## 접근법

모든 친구와 최소 `1시간`씩은 함께해야 하므로, **최소한 필요한 총 시간은 `N`시간**입니다.

<br>
그 이후에는 각 친구가 정해준 시간 `A_i`보다 `1시간`씩 덜 쓰도록 분배할 수 있으므로,

**전체 시간의 최대 허용치는** 다음과 같습니다:

$$
	\text{총 허용 시간} = \sum A_i - N
$$

<br>
여기서 `M`이 이 총 허용 시간을 넘는다면,

**어느 친구와는 `A_i` 이상을 함께할 수밖에 없게 되므로 퇴학당합니다.**

<br>
> 참고 : [비둘기집 원리(Pigeonhole Principle)의 직관과 알고리듬 문제에서의 활용 - soo:bak](https://soo-bak.github.io/algorithm/theory/pigeonhole-principle)

<br>
반대로 $$M \leq \sum A_i - N$$이면,

친구별 제한 시간을 넘지 않고 모든 시간 배정이 가능합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var tokens = Console.ReadLine().Split().Select(long.Parse).ToArray();
    long n = tokens[0], m = tokens[1];

    var a = Console.ReadLine().Split().Select(long.Parse).ToArray();
    long sum = a.Sum();

    Console.WriteLine(sum - n < m ? "OUT" : "DIMI");
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

  ll n, m; cin >> n >> m;

  ll sum = 0;
  for (ll i = 0; i < n; i++) {
    ll a; cin >> a;
    sum += a;
  }

  cout << (sum - n < m ? "OUT" : "DIMI") << "\n";

  return 0;
}
```
