---
layout: single
title: "[백준 13627] Dangerous Dive (C#, C++) - soo:bak"
date: "2025-05-17 20:06:56 +0900"
description: 전체 인원 중 복귀하지 않은 번호를 오름차순으로 구하는 백준 13627번 Dangerous Dive 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 13627
  - C#
  - C++
  - 알고리즘
keywords: "백준 13627, 백준 13627번, BOJ 13627, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[13627번 - Dangerous Dive](https://www.acmicpc.net/problem/13627)

## 설명

**전체 인원 수 `N`과 복귀한 인원 수 `R`이 주어졌을 때, 복귀하지 않은 인원의 번호를 구하는 문제입니다.**

- 번호는 `1`부터 `N`까지 연속적으로 부여되어 있으며,
- 복귀한 인원의 번호만 입력으로 주어집니다.
- 복귀하지 않은 인원의 번호를 오름차순으로 출력해야 하며,
- 모든 인원이 복귀했다면 `*`을 출력합니다.

<br>

## 접근법

전체 인원 수는 `1`부터 `N`까지 순서대로 번호가 매겨져 있고,

그 중 복귀한 번호들이 일부 입력으로 주어집니다.

<br>
우선, 복귀 여부를 빠르게 확인할 수 있도록 전체 번호 범위를 대상으로 기록을 만들어 둡니다.

이후 복귀한 사람들의 번호를 하나씩 확인하면서 그 번호에 해당하는 위치를 표시해두고,

`1`부터 `N`까지의 번호를 순차적으로 확인하며, 복귀하지 않은 번호만 선택하여 출력하면 됩니다.

<br>

모든 사람이 복귀했다면 별도의 출력 없이 `*`만 출력해야 하므로,

처음에 주어진 전체 인원 수와 복귀 인원 수가 같은지를 먼저 확인해야 함에 주의합니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine().Split();
    int n = int.Parse(first[0]);
    int r = int.Parse(first[1]);

    var returned = new bool[n + 1];
    var second = Console.ReadLine().Split();
    foreach (var s in second)
      returned[int.Parse(s)] = true;

    if (n == r) {
      Console.WriteLine("*");
      return;
    }

    for (int i = 1; i <= n; i++) {
      if (!returned[i])
        Console.Write($"{i} ");
    }
    Console.WriteLine();
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

  int n, r; cin >> n >> r;
  bool arr[10001] = {};
  for (int i = 0; i < r; ++i) {
    int x; cin >> x;
    arr[x] = true;
  }

  if (n == r) {
    cout << "*\n";
    return 0;
  }

  for (int i = 1; i <= n; ++i) {
    if (!arr[i]) cout << i << " ";
  }

  cout << "\n";
  return 0;
}
```
