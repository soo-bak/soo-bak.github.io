---
layout: single
title: "[백준 11170] 0의 개수 (C#, C++) - soo:bak"
date: "2025-04-14 02:36:00 +0900"
description: 정수 구간 내 등장하는 0의 총 개수를 세는 백준 11170번 0의 개수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11170
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 브루트포스
keywords: "백준 11170, 백준 11170번, BOJ 11170, countZeroDigits, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11170번 - 0의 개수](https://www.acmicpc.net/problem/11170)

## 설명
정수 구간 `[N, M]` 사이의 모든 수들에 대해서, 각 숫자들에 등장하는 `0`의 총 갯수를 구하는 문제입니다.

---

## 접근법
- 0부터 `1,000,000`까지의 모든 수에 대해 **'0'이 몇 번 나오는지를 사전 계산**합니다.
- 각 테스트 케이스마다 구간 `[N, M]`을 순회하며 미리 계산한 개수를 누적합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int[] cntZero = new int[1_000_001];
      for (int i = 0; i < cntZero.Length; i++) {
        var str = i.ToString();
        foreach (var c in str)
          if (c == '0') cntZero[i]++;
      }

      int t = int.Parse(Console.ReadLine()!);
      while (t-- > 0) {
        var parts = Console.ReadLine()!.Split();
        int s = int.Parse(parts[0]), e = int.Parse(parts[1]);
        int sum = 0;
        for (int i = s; i <= e; i++) sum += cntZero[i];
        Console.WriteLine(sum);
      }
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>
#define MAX 1'000'001

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntZero[MAX];
  for (int i = 0; i < MAX; i++) {
    string str = to_string(i);
    int cnt = 0;
    for (size_t j = 0; j < str.size(); j++)
      if (str[j] == '0') cnt++;

    cntZero[i] = cnt;
  }

  int t; cin >> t;
  while (t--) {
    int s, e; cin >> s >> e;
    int sum = 0;
    for (int i = s; i <= e; i++)
      sum += cntZero[i];

    cout << sum << "\n";
  }

  return 0;
}
```
