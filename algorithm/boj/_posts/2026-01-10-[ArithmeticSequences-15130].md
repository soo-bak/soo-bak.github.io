---
layout: single
title: "[백준 15130] Arithmetic Sequences (C#, C++) - soo:bak"
date: "2026-01-10 21:50:00 +0900"
description: "백준 15130번 C#, C++ 풀이 - 10개 항 중 두 항만 주어진 등차수열을 복원하거나 불가능 시 -1을 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 15130
  - C#
  - C++
  - 알고리즘
  - 구현
  - 수학
keywords: "백준 15130, 백준 15130번, BOJ 15130, Arithmetic Sequences, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15130번 - Arithmetic Sequences](https://www.acmicpc.net/problem/15130)

## 설명
길이 10의 등차수열에서 8개는 0으로 표시되고 2개는 양의 정수가 주어집니다. 등차수열을 정수로 완성할 수 있으면 전체 10항을, 불가능하면 -1을 출력하는 문제입니다.

<br>

## 접근법
먼저 주어진 두 위치와 값을 찾은 후, 두 값의 차이가 두 위치의 차이로 나누어떨어지는지 확인해 공차를 구합니다.

만약, 나누어떨어지지 않으면 불가능하므로 -1을 출력합니다.

나누어떨어진다면 첫 항을 계산하고 이를 이용해 모든 항을 생성합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var arr = Array.ConvertAll(parts, int.Parse);

    var idx1 = -1;
    var idx2 = -1;
    long val1 = 0, val2 = 0;
    for (var i = 0; i < 10; i++) {
      if (arr[i] != 0) {
        if (idx1 == -1) {
          idx1 = i;
          val1 = arr[i];
        }
        else {
          idx2 = i;
          val2 = arr[i];
        }
      }
    }

    var diffNum = val2 - val1;
    var diffDen = idx2 - idx1;
    if (diffNum % diffDen != 0) {
      Console.WriteLine(-1);
      return;
    }
    var d = diffNum / diffDen;
    var a0 = val1 - d * idx1;

    var res = new long[10];
    for (var i = 0; i < 10; i++)
      res[i] = a0 + d * i;

    if (res[idx1] != val1 || res[idx2] != val2) {
      Console.WriteLine(-1);
      return;
    }

    var sb = new StringBuilder();
    for (var i = 0; i < 10; i++) {
      if (i > 0)
        sb.Append(' ');
      sb.Append(res[i]);
    }
    Console.WriteLine(sb.ToString());
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll arr[10];
  for (int i = 0; i < 10; i++)
    cin >> arr[i];

  int idx1 = -1, idx2 = -1;
  ll v1 = 0, v2 = 0;
  for (int i = 0; i < 10; i++) {
    if (arr[i] != 0) {
      if (idx1 == -1) {
        idx1 = i;
        v1 = arr[i];
      }
      else {
        idx2 = i;
        v2 = arr[i];
      }
    }
  }

  ll num = v2 - v1;
  int den = idx2 - idx1;
  if (num % den != 0) {
    cout << -1 << "\n";
    return 0;
  }
  ll d = num / den;
  ll a0 = v1 - d * idx1;

  ll res[10];
  for (int i = 0; i < 10; i++)
    res[i] = a0 + d * i;

  if (res[idx1] != v1 || res[idx2] != v2) {
    cout << -1 << "\n";
    return 0;
  }

  for (int i = 0; i < 10; i++) {
    if (i)
      cout << ' ';
    cout << res[i];
  }
  cout << "\n";

  return 0;
}
```
