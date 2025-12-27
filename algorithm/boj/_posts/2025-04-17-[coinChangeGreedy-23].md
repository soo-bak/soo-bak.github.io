---
layout: single
title: "[백준 11047] 동전 0 (C#, C++) - soo:bak"
date: "2025-04-17 00:29:43 +0900"
description: 주어진 동전 종류로 목표 금액을 만들기 위해 필요한 최소 개수를 구하는 그리디 알고리즘 기반의 백준 11047번 동전 0 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11047
  - C#
  - C++
  - 알고리즘
  - 그리디
keywords: "백준 11047, 백준 11047번, BOJ 11047, coinChangeGreedy, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11047번 - 동전 0](https://www.acmicpc.net/problem/11047)

## 설명
**주어진 동전 종류를 이용하여 특정 금액을 만들기 위해 필요한 최소 동전 개수를 구하는 문제**입니다.<br>
<br>
탐욕법(그리디 알고리듬)을 활용하여 풀이할 수 있는 전형적인 문제입니다. <br>
<br>

- 동전의 가치는 오름차순으로 주어지며, 모든 동전은 무한히 사용 가능하다고 가정합니다.<br>
- 목표 금액을 만들기 위해 가장 적은 수의 동전을 사용하는 것이 목적입니다.<br>
- 각 동전은 이전 동전으로 나누어 떨어지지 않을 수도 있으므로, **그리디 알고리듬으로 역순 탐색**을 통해 해결합니다.<br>

### 접근법
- 동전의 종류를 내림차순으로 정렬하여 큰 동전부터 최대한 많이 사용하도록 합니다.<br>
- 현재 금액이 해당 동전으로 나누어 떨어지면 몫만큼 카운트하고, 나머지 금액으로 갱신합니다.<br>
- 반복하며 금액이 `0`이 될 때까지 진행합니다.<br>

<br>
> 참고 : [그리디 알고리듬(Greedy Algorithm, 탐욕법)의 원리와 적용 - soo:bak](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)

<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split().Select(int.Parse).ToArray();
    int count = input[0];
    int target = input[1];

    var coins = new int[count];
    for (int i = 0; i < count; i++)
      coins[i] = int.Parse(Console.ReadLine());

    int result = 0;
    for (int i = count - 1; i >= 0; i--) {
      result += target / coins[i];
      target %= coins[i];
      if (target == 0) break;
    }

    Console.WriteLine(result);
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, tSum; cin >> n >> tSum;
  vi coins(n);
  for (int i = n - 1; i >= 0; i--)
    cin >> coins[i];

  int cnt = 0;
  for (int i = 0; i < n; i++) {
    cnt += tSum / coins[i];
    tSum %= coins[i];
    if (tSum == 0) break;
  }
  cout << cnt << "\n";

  return 0;
}
```
