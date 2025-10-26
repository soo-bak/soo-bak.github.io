---
layout: single
title: "[백준 2851] 슈퍼 마리오 (C#, C++) - soo:bak"
date: "2025-05-18 02:37:00 +0900"
description: 버섯 점수의 누적합을 계산하여 100에 가장 가까운 값을 선택하는 백준 2851번 슈퍼 마리오 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크

[2851번 - 슈퍼 마리오](https://www.acmicpc.net/problem/2851)

## 설명

**버섯을 순서대로 먹으면서 점수를 누적할 때, 총합이 100에 가장 가깝도록 멈추는 시점을 결정하는 문제입니다.**

총 `10개`의 버섯이 주어지고, 각 버섯에는 `100 이하의 점수`가 부여되어 있습니다.

버섯은 반드시 첫 번째부터 차례대로 먹어야 하며,

도중에 멈추면 그 이후의 버섯은 더 이상 먹을 수 없습니다.

<br>
목표는 누적 점수가 `100`에 최대한 가까워지도록 하되,

가까운 수가 둘일 경우 더 큰 점수를 선택해야 합니다.

<br>

## 접근법

입력으로 주어진 `10개`의 점수를 앞에서부터 하나씩 더해가며 누적합을 계산합니다.

* 누적합이 `100` 이상이 되는 순간 반복을 종료합니다.
* 단, 마지막에 더한 값이 오히려 `100`을 넘겨버린 경우를 고려해야 합니다.
  * 이때 이전 누적합과 비교하여 더 가까운 쪽을 선택합니다.
  * 두 값이 같은 거리만큼 떨어져 있다면, **더 큰 값을 선택**하는 조건에 따라 지금까지의 누적합을 유지합니다.

<br>
> 참고 : [누적합(Prefix Sum)의 원리와 구간 합 계산 - soo:bak](https://soo-bak.github.io/algorithm/theory/prefix-sum/)

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int[] mush = new int[10];
    for (int i = 0; i < 10; i++)
      mush[i] = int.Parse(Console.ReadLine());

    int sum = 0;
    for (int i = 0; i < 10; i++) {
      sum += mush[i];
      if (sum >= 100) {
        if (sum - 100 > 100 - (sum - mush[i]))
          sum -= mush[i];
        break;
      }
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

  vi mush(10);
  for (int& x : mush)
    cin >> x;

  int sum = 0;
  for (int i = 0; i < 10; ++i) {
    sum += mush[i];
    if (sum >= 100) {
      if (sum - 100 > 100 - (sum - mush[i])) sum -= mush[i];
      break;
    }
  }

  cout << sum << "\n";

  return 0;
}
```
