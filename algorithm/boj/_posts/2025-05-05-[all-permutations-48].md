---
layout: single
title: "[백준 10974] 모든 순열 (C#, C++) - soo:bak"
date: "2025-05-05 18:30:00 +0900"
description: 1부터 N까지의 수를 사전순으로 나열한 모든 순열을 출력하는 백준 10974번 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10974 - 모든 순열](https://www.acmicpc.net/problem/10974)

## 설명

`1`부터 `N`까지의 수로 만들 수 있는 **모든 순열을 사전순으로 출력하는 문제**입니다.

순열이란 `N`개의 원소를 서로 다른 순서로 나열한 경우의 집합이며,

이 문제에서는 가능한 모든 순열을 **작은 수부터 시작하여 사전순으로 정렬된 형태로 출력**해야 합니다.

<br>

## 접근법

- `1`부터 `N`까지의 수 중 아직 사용하지 않은 수를 하나씩 선택하며, <br>
  **현재까지 선택된 순열 뒤에 이어붙이는 방식으로 탐색**을 진행합니다.
- 선택된 수는 **중복되지 않도록 방문 여부를 확인**하며 선택하고, <br>
  모든 선택이 완료되어 수열의 길이가 `N`이 되면 **해당 순열을 출력**합니다.
- 이러한 방식은 전형적인 **백트래킹(재귀)** 구조로 구현할 수 있으며, <br>
  사전순 출력을 위해 항상 **작은 수부터 탐색**합니다.

<br>
> 참고 : [백트래킹(Backtracking)의 개념과 구조적 사고 - soo:bak](https://soo-bak.github.io/algorithm/theory/backTracking/)

<br>

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

class Program {
  static int n;
  static List<int> perm = new List<int>();
  static bool[] used;

  static void BackTrack() {
    if (perm.Count == n) {
      Console.WriteLine(string.Join(" ", perm));
      return;
    }

    for (int i = 1; i <= n; i++) {
      if (!used[i]) {
        used[i] = true;
        perm.Add(i);
        BackTrack();
        perm.RemoveAt(perm.Count - 1);
        used[i] = false;
      }
    }
  }

  static void Main() {
    n = int.Parse(Console.ReadLine());
    used = new bool[n + 1];
    BackTrack();
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;

int n;
vi p;
vector<bool> used;

void backTrack() {
  if (p.size() == (size_t)n) {
    for (int i = 0; i < n; i++)
      cout << p[i] << (i < n - 1 ? " " : "\n");
  } else {
    for (int i = 1; i <= n; i++) {
      if (!used[i]) {
        used[i] = true;
        p.push_back(i);
        backTrack();
        used[i] = false;
        p.pop_back();
      }
    }
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> n;
  used.resize(n + 1);

  backTrack();

  return 0;
}
```
