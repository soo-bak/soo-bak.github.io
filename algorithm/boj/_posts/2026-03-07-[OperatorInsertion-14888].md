---
layout: single
title: "[백준 14888] 연산자 끼워넣기 (C#, C++) - soo:bak"
date: "2026-03-07 19:06:00 +0900"
description: "백준 14888번 C#, C++ 풀이 - 주어진 연산자 개수로 만들 수 있는 식의 최댓값과 최솟값을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 14888
  - C#
  - C++
  - 알고리즘
  - 브루트포스
  - 백트래킹
keywords: "백준 14888, 백준 14888번, BOJ 14888, 연산자 끼워넣기, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14888번 - 연산자 끼워넣기](https://www.acmicpc.net/problem/14888)

## 설명
수열의 순서를 유지한 채 주어진 개수만큼의 연산자를 사이사이에 넣어 식을 만들 때, 앞에서부터 계산한 결과의 최댓값과 최솟값을 구하는 문제입니다.

<br>

## 접근법
연산자 개수가 정해져 있으므로, 현재 위치에서 사용할 수 있는 연산자를 하나씩 선택하며 모든 경우를 탐색하면 됩니다. 각 단계에서는 지금까지 계산한 값과 다음 수를 현재 연산자로 계산해 다음 단계로 넘깁니다.

끝까지 연산자를 모두 사용했다면 그 결과로 최댓값과 최솟값을 갱신합니다. 수의 개수가 최대 11개라 가능한 경우의 수를 완전탐색해도 충분합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static int n;
  static int[] nums = Array.Empty<int>();
  static int[] ops = Array.Empty<int>();
  static int maxValue = int.MinValue;
  static int minValue = int.MaxValue;

  static void Dfs(int idx, int value) {
    if (idx == n) {
      if (value > maxValue) maxValue = value;
      if (value < minValue) minValue = value;
      return;
    }

    for (int i = 0; i < 4; i++) {
      if (ops[i] == 0)
        continue;

      ops[i]--;
      int next = value;
      if (i == 0) next += nums[idx];
      else if (i == 1) next -= nums[idx];
      else if (i == 2) next *= nums[idx];
      else next /= nums[idx];

      Dfs(idx + 1, next);
      ops[i]++;
    }
  }

  static void Main() {
    n = int.Parse(Console.ReadLine()!);
    nums = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    ops = Console.ReadLine()!.Split().Select(int.Parse).ToArray();

    Dfs(1, nums[0]);

    Console.WriteLine(maxValue);
    Console.WriteLine(minValue);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> nums, ops;
int max_value = INT_MIN;
int min_value = INT_MAX;

void dfs(int idx, int value) {
  if (idx == n) {
    max_value = max(max_value, value);
    min_value = min(min_value, value);
    return;
  }

  for (int i = 0; i < 4; i++) {
    if (ops[i] == 0)
      continue;

    ops[i]--;
    int next = value;
    if (i == 0) next += nums[idx];
    else if (i == 1) next -= nums[idx];
    else if (i == 2) next *= nums[idx];
    else next /= nums[idx];

    dfs(idx + 1, next);
    ops[i]++;
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> n;
  nums.resize(n);
  ops.resize(4);

  for (int i = 0; i < n; i++)
    cin >> nums[i];
  for (int i = 0; i < 4; i++)
    cin >> ops[i];

  dfs(1, nums[0]);

  cout << max_value << "\n";
  cout << min_value << "\n";

  return 0;
}
```
