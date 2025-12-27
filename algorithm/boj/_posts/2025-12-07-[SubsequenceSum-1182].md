---
layout: single
title: "[백준 1182] 부분수열의 합 (C#, C++) - soo:bak"
date: "2025-12-07 01:55:00 +0900"
description: N개의 정수에서 공집합이 아닌 부분수열 중 합이 S가 되는 경우의 수를 구하는 백준 1182번 부분수열의 합 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1182
  - C#
  - C++
  - 알고리즘
  - 브루트포스
  - 백트래킹
keywords: "백준 1182, 백준 1182번, BOJ 1182, SubsequenceSum, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1182번 - 부분수열의 합](https://www.acmicpc.net/problem/1182)

## 설명
N개의 정수가 주어질 때, 공집합이 아닌 부분수열 중 합이 S가 되는 경우의 수를 구하는 문제입니다.

<br>

## 접근법
DFS로 각 원소에 대해 포함할지 말지를 결정합니다. 현재 인덱스와 현재까지의 합을 인자로 넘기면서, 해당 원소를 포함하지 않고 다음으로 넘어가는 경우와 포함하고 합에 더한 뒤 다음으로 넘어가는 경우 두 갈래로 재귀 호출합니다.

인덱스가 N에 도달하면 모든 원소에 대한 선택이 끝난 것입니다. 이때 현재 합이 S와 같으면 경우의 수를 하나 증가시킵니다.

탐색이 모두 끝난 뒤, S가 0인 경우에는 공집합도 합이 0이므로 경우의 수에서 하나를 빼줍니다.

<br>

- - -

## Code

### C#

```csharp
using System;

class Program {
  static int n, target;
  static int[] arr = Array.Empty<int>();
  static int cnt = 0;

  static void Dfs(int idx, int sum) {
    if (idx == n) {
      if (sum == target) cnt++;
      return;
    }
    Dfs(idx + 1, sum);
    Dfs(idx + 1, sum + arr[idx]);
  }

  static void Main() {
    var first = Console.ReadLine()!.Split();
    n = int.Parse(first[0]);
    target = int.Parse(first[1]);
    var nums = Console.ReadLine()!.Split();
    arr = new int[n];
    for (var i = 0; i < n; i++) arr[i] = int.Parse(nums[i]);

    Dfs(0, 0);
    if (target == 0) cnt--;

    Console.WriteLine(cnt);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, target;
int arr[21];
int cnt = 0;

void dfs(int idx, int sum) {
  if (idx == n) {
    if (sum == target) cnt++;
    return;
  }
  dfs(idx + 1, sum);
  dfs(idx + 1, sum + arr[idx]);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> n >> target;
  for (int i = 0; i < n; i++) cin >> arr[i];

  dfs(0, 0);
  if (target == 0) cnt--;

  cout << cnt << "\n";

  return 0;
}
```
