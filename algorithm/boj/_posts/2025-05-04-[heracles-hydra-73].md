---
layout: single
title: "[백준 10205] 헤라클레스와 히드라 (C#, C++) - soo:bak"
date: "2025-05-04 19:13:00 +0900"
description: 주어진 행동에 따라 히드라의 머리 개수를 증가 또는 감소시키는 시뮬레이션 문제, 백준 10205번 헤라클레스와 히드라 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10205
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 10205, 백준 10205번, BOJ 10205, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10205번 - 헤라클레스와 히드라](https://www.acmicpc.net/problem/10205)

## 설명

히드라의 머리 개수와 히드라에게 수행한 행동들이 주어졌을 때, 최종적으로 남아 있는 머리의 개수를 구하는 시뮬레이션 문제입니다.

각 행동은 다음 두 가지 중 하나입니다:

- **'c'**: 히드라의 머리를 자르기만 한 경우 → 머리 하나를 없애고 두 개가 새로 나와 총 **1개 증가**
- **'b'**: 머리를 자르고 동시에 불로 지진 경우 → 머리 하나만 제거되어 **1개 감소**

히드라의 머리는 1개 이상 남아 있을 때만 살아 있으며, 머리가 모두 제거되면 시뮬레이션이 종료됩니다.

<br>

## 접근법

- 각 테스트마다 히드라의 초기 머리 개수를 입력받은 뒤, 연속된 행동을 나타내는 문자열을 입력받습니다.
- 문자열을 순서대로 확인하면서 다음 기준에 따라 머리 수를 갱신합니다:
  - `'c'`가 등장하면 머리 하나를 자르지만 두 개로 자라나므로 `+1`
  - `'b'`가 등장하면 머리 하나를 자르고 불로 지져 더 이상 자라지 않게 하므로 `-1`
- 각 테스트 결과는 `"Data Set x:"` 형식으로 출력하고, 남은 머리 수를 한 줄에 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    for (int i = 1; i <= t; i++) {
      int h = int.Parse(Console.ReadLine());
      var s = Console.ReadLine();
      foreach (char c in s)
        h += c == 'c' ? 1 : c == 'b' ? -1 : 0;

      Console.WriteLine($"Data Set {i}:");
      Console.WriteLine($"{h}");
      if (i < t) Console.WriteLine();
    }
  }
}
```

<br>

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  for (int i = 1; i <= t; i++) {
    int h; string s; cin >> h >> s;
    for (char c : s)
      h += c == 'c' ? 1 : c == 'b' ? -1 : 0;
    cout << "Data Set " << i << ":\n" << h << "\n";
    if (i < t) cout << "\n";
  }

  return 0;
}
```
