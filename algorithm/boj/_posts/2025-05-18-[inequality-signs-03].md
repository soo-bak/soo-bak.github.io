---
layout: single
title: "[백준 2529] 부등호 (C#, C++) - soo:bak"
date: "2025-05-18 03:00:00 +0900"
description: 주어진 부등호 조건을 만족하는 모든 숫자 조합 중 최댓값과 최솟값을 구하는 백준 2529번 부등호 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2529
  - C#
  - C++
  - 알고리즘
  - 브루트포스
  - 백트래킹
keywords: "백준 2529, 백준 2529번, BOJ 2529, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2529번 - 부등호](https://www.acmicpc.net/problem/2529)

## 설명

**주어진 부등호 순서를 만족하면서 0부터 9까지의 숫자 중 서로 다른 숫자를 사용하여 만들 수 있는 최댓값과 최솟값을 구하는 문제입니다.**

<br>
입력으로 `k`개의 부등호가 주어지며, 숫자는 총 `k + 1`개 사용됩니다.

모든 숫자는 **한 자리 수이며, 중복 없이 선택**되어야 합니다.

<br>
예를 들어 부등호가 `< >`인 경우, 숫자 `0 2 1`을 배치하면 `0 < 2 > 1`이 되어 조건을 만족합니다.

이때 가능한 모든 경우 중 최댓값과 최솟값을 찾아야 합니다.

<br>

## 접근법

백트래킹 방식을 통해 가능한 모든 숫자 조합을 시도하면서, 부등호 조건을 만족하는지를 확인합니다.

각 단계에서 다음 숫자를 선택할 때는 다음을 고려합니다:

- 아직 사용하지 않은 숫자 중에서 하나를 선택합니다.
- 현재 선택한 숫자와 이전에 선택한 숫자 사이의 부등호 조건이 맞는지 확인합니다.
- 조건을 만족할 경우 다음 자릿수로 재귀적 탐색을 진행합니다.
- 조건을 만족하지 않으면 해당 선택은 무시합니다.

<br>
모든 경우의 수를 다 확인한 뒤, 정답 목록을 사전순으로 정렬하면

가장 앞에 있는 경우가 최솟값, 가장 뒤에 있는 경우가 최댓값이 됩니다.

<br>

> 참고 : [백트래킹(Backtracking)의 개념과 구조적 사고 - soo:bak](https://soo-bak.github.io/algorithm/theory/backTracking/)

> 참고 : [조합(Combination)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/combination/)

<br>

---

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static int k;
  static char[] signs = new char[10];
  static bool[] used = new bool[10];
  static string s = "";
  static List<string> results = new List<string>();

  static void Solve(int idx) {
    if (idx == k + 1) {
      results.Add(s);
      return;
    }

    for (char c = '0'; c <= '9'; ++c) {
      int digit = c - '0';
      if (used[digit]) continue;
      if (idx > 0) {
        char last = s[s.Length - 1];
        if ((signs[idx - 1] == '<' && last >= c) ||
            (signs[idx - 1] == '>' && last <= c)) continue;
      }

      used[digit] = true;
      s += c;
      Solve(idx + 1);
      s = s.Substring(0, s.Length - 1);
      used[digit] = false;
    }
  }

  static void Main() {
    k = int.Parse(Console.ReadLine());
    var input = Console.ReadLine()?.Split();
    for (int i = 0; i < k; i++)
      signs[i] = input[i][0];
    Solve(0);
    results.Sort();
    Console.WriteLine(results[results.Count - 1]);
    Console.WriteLine(results[0]);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<string> vs;

int k;
char signs[10];
bool used[10];
string s;
vs ans;

void solve(int idx) {
  if (idx == k + 1) {
    ans.push_back(s);
    return;
  }

  for (char c = '0'; c <= '9'; ++c) {
    if (used[c - '0']) continue;
    if (idx && ((signs[idx - 1] == '>' && s.back() < c) ||
                (signs[idx - 1] == '<' && s.back() > c))) continue;

    used[c - '0'] = true;
    s += c;

    solve(idx + 1);

    s.pop_back();
    used[c - '0'] = false;
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> k;
  for (int i = 0; i < k; ++i)
    cin >> signs[i];

  solve(0);

  cout << ans.back() << "\n" << ans.front() << "\n";

  return 0;
}
```
