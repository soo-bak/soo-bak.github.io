---
layout: single
title: "[백준 2979] 트럭 주차 (C++, C#) - soo:bak"
date: "2025-05-02 19:51:00 +0900"
description: 시간대별 트럭 수를 기준으로 주차 요금을 계산하는 시뮬레이션 문제 백준 2979번 트럭 주차의 C++ 및 C# 풀이와 해설
---

## 문제 링크
[2979번 - 트럭 주차](https://www.acmicpc.net/problem/2979)

## 설명
세 대의 트럭이 특정 시간 구간에 따라 주차장을 사용하며,

**동시에 주차된 트럭 수에 따라 단가가 다르게 적용되는 상황**을 시뮬레이션하여 **총 주차 요금**을 계산하는 문제입니다.

<br>

- 요금은 다음과 같이 주어집니다:
  - 한 대만 있을 때는 분당 `A`원
  - 두 대가 동시에 있을 경우, 한 대당 분당 `B`원 (총 `2 * B`)
  - 세 대가 동시에 있을 경우, 한 대당 분당 `C`원 (총 `3 * C`)

- 각 트럭의 도착 시각과 떠나는 시각이 주어졌을 때, **1분 단위로 총 주차 요금을 계산**해야 합니다.

<br>

## 접근법

- 각 트럭의 주차 시간 구간을 순회하면서, 해당 구간에 트럭이 있었던 시각마다 값을 하나씩 증가시켜 기록합니다.
- 이후, 전체 시각을 순회하며 각 시각에 주차된 트럭 수에 따라 요금을 계산해 누적합니다.
- 이렇게 계산한 요금을 모두 더하여, 최종적으로 지불해야 할 주차 요금을 계산한 후 출력합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    int a = int.Parse(input[0]);
    int b = int.Parse(input[1]);
    int c = int.Parse(input[2]);

    var cnt = new int[101];

    for (int i = 0; i < 3; i++) {
      var range = Console.ReadLine().Split();
      int start = int.Parse(range[0]);
      int end = int.Parse(range[1]);

      for (int t = start; t < end; t++)
        cnt[t]++;
    }

    int sum = 0;
    for (int t = 1; t <= 100; t++) {
      if (cnt[t] == 1) sum += a;
      else if (cnt[t] == 2) sum += 2 * b;
      else if (cnt[t] == 3) sum += 3 * c;
    }

    Console.WriteLine(sum);
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

  int cnt[100] = {0, };

  int a, b, c; cin >> a >> b >> c;

  int minStart = 100, maxEnd = 0;
  for (int i = 0; i < 3; i++) {
    int start, end; cin >> start >> end;
    minStart = min(minStart, start);
    maxEnd = max(maxEnd, end);
    for (int t = start; t < end; t++)
      cnt[t - 1]++;
  }

  int sum = 0;
  for (int t = minStart; t < maxEnd; t++) {
    if (cnt[t - 1] == 1) sum += a;
    else if (cnt[t - 1] == 2) sum += 2 * b;
    else if (cnt[t - 1] == 3) sum += 3 * c;
  }

  cout << sum << "\n";

  return 0;
}
```
