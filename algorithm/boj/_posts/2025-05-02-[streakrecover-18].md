---
layout: single
title: "[백준 30395] 내 스트릭을 돌려내! (C#, C++) - soo:bak"
date: "2025-05-02 04:14:00 +0900"
description: 문제 풀이 여부와 프리즈 재장착 조건에 따라 스트릭을 유지하며, 최장 스트릭 길이를 계산하는 백준 30395번 내 스트릭을 돌려내! 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[30395번 - 내 스트릭을 돌려내!](https://www.acmicpc.net/problem/30395)

## 설명
**문제를 매일 최소 1개 이상 해결한 연속일 수**, 즉 스트릭의 최장 길이를 계산하는 문제입니다.<br>

스트릭은 연속적으로 문제를 푼 날짜가 이어져야 유지되지만, `스트릭 프리즈` 아이템을 사용하면 하루 문제를 풀지 않아도 스트릭이 끊기지 않습니다.

이 아이템은 사용된 이후 최소 `2일`이 지나야 다시 장착할 수 있으며, 하루에 한 번만 사용할 수 있습니다.

처음 시작할 때는 `스트릭 프리즈`가 장착되어 있으며, 문제를 푼 날은 스트릭을 계속 이어갈 수 있습니다.

하루라도 문제를 풀지 않았고 `스트릭 프리즈`를 사용할 수 없는 상황이라면 스트릭이 끊기게 됩니다.<br>

<br>

## 접근법

- 입력으로 주어진 `N`일 동안의 문제 해결 기록을 순회합니다.
- 현재 날짜의 풀이 수가 `1` 이상이라면 스트릭을 그대로 이어갑니다.
- 풀이 수가 `0`이라면 두 가지 경우로 나뉩니다:
  - 최근 `스트릭 프리즈`를 사용한 날로부터 **2일 이상** 지났다면 다시 장착하여 스트릭을 유지할 수 있습니다.
  - 그렇지 않다면 현재 스트릭은 끊기고 길이를 초기화합니다.
- 매일 현재 스트릭의 길이를 갱신하며, 전체 중 가장 길었던 스트릭을 최종 출력합니다.

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var p = Console.ReadLine().Split().Select(int.Parse).ToArray();

    int max = 0, cur = 0, f = -2;
    for (int i = 0; i < n; i++) {
      if (p[i] > 0) cur++;
      else if (i - f >= 2) f = i;
      else cur = 0;

      max = Math.Max(max, cur);
    }

    Console.WriteLine(max);
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

  int n; cin >> n;

  int ans = 0, cur = 0, f = -2;
  for (int i = 0; i < n; i++) {
    int p; cin >> p;
    if (p) cur++;
    else if (i - f >= 2) f = i;
    else cur = 0;

    ans = max(ans, cur);
  }

  cout << ans << "\n";

  return 0;
}
```
