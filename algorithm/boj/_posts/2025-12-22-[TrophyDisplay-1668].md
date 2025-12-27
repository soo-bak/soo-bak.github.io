---
layout: single
title: "[백준 1668] 트로피 진열 (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: "백준 1668번 C#, C++ 풀이 - 왼쪽과 오른쪽에서 보이는 트로피 개수를 각각 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 1668
  - C#
  - C++
  - 알고리즘
keywords: "백준 1668, 백준 1668번, BOJ 1668, TrophyDisplay, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1668번 - 트로피 진열](https://www.acmicpc.net/problem/1668)

## 설명
트로피 높이가 주어질 때 왼쪽과 오른쪽에서 보이는 개수를 계산하는 문제입니다.

<br>

## 접근법
왼쪽에서 보이는 개수는 왼쪽부터 순회하며 현재까지의 최대 높이를 갱신하고, 갱신될 때마다 개수를 증가시킵니다.

오른쪽에서 보이는 개수도 오른쪽부터 같은 방식으로 셉니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var h = new int[n];
    for (var i = 0; i < n; i++)
      h[i] = int.Parse(Console.ReadLine()!);

    var left = 0;
    var maxL = 0;
    for (var i = 0; i < n; i++) {
      if (h[i] > maxL) {
        maxL = h[i];
        left++;
      }
    }

    var right = 0;
    var maxR = 0;
    for (var i = n - 1; i >= 0; i--) {
      if (h[i] > maxR) {
        maxR = h[i];
        right++;
      }
    }

    Console.WriteLine(left);
    Console.WriteLine(right);
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

  int n; cin >> n;
  vi h(n);
  for (int i = 0; i < n; i++)
    cin >> h[i];

  int left = 0, maxL = 0;
  for (int i = 0; i < n; i++) {
    if (h[i] > maxL) {
      maxL = h[i];
      left++;
    }
  }

  int right = 0, maxR = 0;
  for (int i = n - 1; i >= 0; i--) {
    if (h[i] > maxR) {
      maxR = h[i];
      right++;
    }
  }

  cout << left << "\n";
  cout << right << "\n";

  return 0;
}
```
