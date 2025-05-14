---
layout: single
title: "[백준 32952] 비트코인 반감기 (C#, C++) - soo:bak"
date: "2025-05-14 23:23:00 +0900"
description: 블록 번호에 따라 반감된 채굴 보상을 계산하는 백준 32952번 비트코인 반감기 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[32952번 - 비트코인 반감기](https://www.acmicpc.net/problem/32952)

## 설명
**특정 블록의 채굴 보상이, 반감 주기와 초기 보상 기준에 따라 얼마나 줄어드는지를 계산**하는 문제입니다.

비트코인 채굴 보상은 다음과 같은 조건을 따라 이루어집니다:

- `R`: 초기 보상 (`0`번 블록부터 적용됨)
- `K`: 반감기 주기 (매 `K`개의 블록마다 보상이 절반으로 감소)
- `M`: 보상을 알고 싶은 블록 번호

매 `K`개의 블록이 지날 때마다 보상은 절반이 되며, 보상이 `1` 미만이 되면 이후 모든 보상은 `0`이 됩니다.

<br>

## 접근법

- 블록 번호 `M`은 몇 번째 반감기에 속하는지를 계산합니다.<br>
  반감 횟수는 다음과 같이 계산됩니다:

  $$
  \text{반감 횟수} = \frac{M}{K}
  $$

- 이후 보상은 반감 횟수만큼 나누어진 값으로 결정되며 다음과 같이 계산됩니다:

  $$
  \text{보상} = \frac{R}{2^\text{반감 횟수}}
  $$

- 이 값이 `0`보다 작아지면 실제 보상은 `0`입니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    long r = long.Parse(input[0]);
    long k = long.Parse(input[1]);
    long m = long.Parse(input[2]);

    long cnt = m / k;
    long reward = r;

    for (long i = 0; i < cnt && reward > 0; i++)
      reward /= 2;

    Console.WriteLine(reward);
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

  ll r, k, m; cin >> r >> k >> m;
  ll cnt = m / k;

  while (cnt-- && r > 0)
    r /= 2;

  cout << r << "\n";

  return 0;
}
```
