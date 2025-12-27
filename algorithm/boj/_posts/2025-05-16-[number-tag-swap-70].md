---
layout: single
title: "[백준 11949] 번호표 교환 (C#, C++) - soo:bak"
date: "2025-05-16 22:03:00 +0900"
description: 각 단계마다 카드값에 따라 학생들의 번호표를 조건에 맞게 교환하는 시뮬레이션 문제 백준 11949번 번호표 교환의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11949
  - C#
  - C++
  - 알고리즘
  - 구현
  - 시뮬레이션
keywords: "백준 11949, 백준 11949번, BOJ 11949, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11949번 - 번호표 교환](https://www.acmicpc.net/problem/11949)

## 설명

**학생들이 한 줄로 서 있는 상태에서, 주어진 규칙에 따라 번호표를 교환해 나가는 시뮬레이션 문제입니다.**

모든 학생들은 번호표를 들고 한 줄로 서 있으며, 이 번호표에는 각각 다른 수가 적혀 있습니다.

게임이 시작되면 선생님은 `1번부터 M번까지`의 카드를 차례대로 사용합니다.

각 카드가 사용될 때마다, 카드에 적힌 숫자를 기준으로 인접한 학생 두 명이 자신들의 번호를 비교하고,

조건에 맞으면 서로 교환합니다.

<br>
비교는 단순한 크기 비교가 아니라, **각자의 번호를 현재 카드 번호로 나눈 나머지 값**을 기준으로 진행됩니다.

<br>
즉, 한 카드가 사용될 때 줄 전체를 한 번 훑으며,

왼쪽부터 오른쪽으로 학생들의 번호가 조건에 따라 교환되는 과정을 반복하게 됩니다.

<br>

## 접근법

이 문제는 전체적으로 `M번의 시뮬레이션`으로 구성됩니다.

각 카드 번호 `k`에 대해, 줄의 왼쪽부터 오른쪽까지 학생들을 순서대로 확인하면서

두 학생의 번호를 각각 `k`로 나눈 나머지를 비교합니다.

이 때, 왼쪽 학생의 나머지가 오른쪽 학생의 나머지보다 크면, 두 번호표를 즉시 교환합니다.

이 과정을 `k = 1`부터 `k = M`까지 반복한 뒤,

마지막에 남은 번호표 상태를 그대로 출력하면 됩니다.

<br>

---

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var tokens = Console.ReadLine().Split().Select(int.Parse).ToArray();
    int n = tokens[0], c = tokens[1];

    var students = new int[n];
    for (int i = 0; i < n; i++)
      students[i] = int.Parse(Console.ReadLine());

    for (int k = 1; k <= c; k++) {
      for (int i = 0; i < n - 1; i++) {
        if (students[i] % k > students[i + 1] % k)
          (students[i], students[i + 1]) = (students[i + 1], students[i]);
      }
    }

    foreach (var x in students)
      Console.WriteLine(x);
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

  int n, c; cin >> n >> c;

  vi students(n);
  for (int& x : students)
    cin >> x;

  for (int k = 1; k <= c; ++k) {
    for (int i = 0; i < n - 1; ++i) {
      if (students[i] % k > students[i + 1] % k)
        swap(students[i], students[i + 1]);
    }
  }

  for (int x : students)
    cout << x << "\n";

  return 0;
}
```
