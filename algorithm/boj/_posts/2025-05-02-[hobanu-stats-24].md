---
layout: single
title: "[백준 30468] 호반우가 학교에 지각한 이유 1 (C#, C++) - soo:bak"
date: "2025-05-02 04:20:00 +0900"
description: 네 개의 능력치 합을 바탕으로 평균을 목표 수치 이상으로 맞추기 위해 필요한 최소 증가량을 구하는 백준 30468번 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 30468
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 30468, 백준 30468번, BOJ 30468, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30468번 - 호반우가 학교에 지각한 이유 1](https://www.acmicpc.net/problem/30468)

## 설명
네 개의 능력치(힘, 민첩, 지능, 운)가 주어졌을 때,

이들의 평균이 목표 수치 이상이 되도록 능력치를 증가시켜야 합니다.

능력치를 `1` 올릴 때마다 축복을 `1회` 사용하는 것으로 간주하며,

**평균이 목표치에 도달할 때까지 필요한 최소 축복 횟수**를 구하는 문제입니다.

<br>

## 접근법

- 네 개의 능력치를 입력받은 뒤, 이들의 합을 구합니다.
- 현재 평균이 목표 이상인지 확인합니다.
- 목표에 미치지 못하는 경우, 능력치를 하나씩 증가시켜 전체 합을 늘려갑니다.
- 평균이 기준을 넘는 순간 반복을 멈추고, 그동안 능력치를 몇 번 올렸는지 계산해 출력합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var tokens = Console.ReadLine().Split();
      int total = 0;
      for (int i = 0; i < 4; i++)
        total += int.Parse(tokens[i]);

      int n = int.Parse(tokens[4]);

      int avg = total / 4;
      int blessings = 0;
      while (avg < n) {
        total++;
        avg = total / 4;
        blessings++;
      }

      Console.WriteLine(blessings);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int str, dex, wis, luk, n;
  cin >> str >> dex >> wis >> luk >> n;

  int total = str + dex + wis + luk;
  int avg = total / 4;

  int blessings = 0;
  while (avg < n) {
    total++;
    avg = total / 4;
    blessings++;
  }

  cout << blessings << "\n";

  return 0;
}
```
