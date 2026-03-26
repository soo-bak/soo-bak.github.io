---
layout: single
title: "[백준 15155] Analysis of Advanced Analytics (C#, C++) - soo:bak"
date: "2026-03-28 06:11:00 +0900"
description: "백준 15155번 C#, C++ 풀이 - 현재 공책에 들어가면 쓰고 아니면 새 공책으로 넘어가는 시뮬레이션 문제"
tags:
  - 백준
  - BOJ
  - 15155
  - C#
  - C++
  - 알고리즘
  - 구현
  - 시뮬레이션
keywords: "백준 15155, 백준 15155번, BOJ 15155, Analysis of Advanced Analytics, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15155번 - Analysis of Advanced Analytics](https://www.acmicpc.net/problem/15155)

## 설명
하루마다 필요한 필기 분량이 주어질 때, 현재 공책에 다 들어가면 계속 쓰고 들어가지 않으면 새 공책으로 넘어가는 방식으로 필요한 공책 수를 구하는 문제입니다.

<br>

## 접근법
현재 공책에 몇 쪽을 사용했는지만 관리하면 충분합니다.

각 날짜의 필기 분량을 순서대로 보면서, 현재 공책에 더 쓸 수 있으면 그대로 더합니다. 반대로 현재 공책에 다 들어가지 않으면 공책 수를 하나 늘리고, 새 공책에 그날 분량부터 다시 기록합니다.

이 과정을 모든 날짜에 대해 반복하면 필요한 공책 수를 구할 수 있습니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int[] first = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    int n = first[0];
    int k = first[1];
    int[] pages = Console.ReadLine()!.Split().Select(int.Parse).ToArray();

    int notebooks = 1;
    int used = 0;

    for (int i = 0; i < n; i++) {
      if (used + pages[i] <= k) {
        used += pages[i];
      } else {
        notebooks++;
        used = pages[i];
      }
    }

    Console.WriteLine(notebooks);
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

  int n, k;
  cin >> n >> k;

  int notebooks = 1;
  int used = 0;

  for (int i = 0; i < n; i++) {
    int pages;
    cin >> pages;

    if (used + pages <= k) {
      used += pages;
    } else {
      notebooks++;
      used = pages;
    }
  }

  cout << notebooks << "\n";

  return 0;
}
```
