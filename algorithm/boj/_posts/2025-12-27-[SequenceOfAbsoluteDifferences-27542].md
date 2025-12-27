---
layout: single
title: "[백준 27542] 絶対階差数列 (Sequence of Absolute Differences) (C#, C++) - soo:bak"
date: "2025-12-27 10:55:00 +0900"
description: "백준 27542번 C#, C++ 풀이 - 인접한 값의 절대차로 수열을 줄여나가 마지막에 남는 값을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 27542
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 27542, 백준 27542번, BOJ 27542, SequenceOfAbsoluteDifferences, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[27542번 - 絶対階差数列 (Sequence of Absolute Differences)](https://www.acmicpc.net/problem/27542)

## 설명
수열이 주어질 때, 인접한 두 원소의 절대차로 새로운 수열을 만드는 작업을 반복합니다. 마지막에 남는 값을 구하는 문제입니다.

<br>

## 접근법
현재 수열에서 인접한 원소 쌍의 절대차를 계산해 새 수열을 만듭니다.

길이가 1이 될 때까지 반복하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var arr = Console.ReadLine()!.Split().Select(long.Parse).ToArray();

    for (var len = n; len > 1; len--) {
      var next = new long[len - 1];
      for (var i = 0; i < len - 1; i++)
        next[i] = Math.Abs(arr[i + 1] - arr[i]);
      arr = next;
    }

    Console.WriteLine(arr[0]);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef vector<ll> vll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vll a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  for (int len = n; len > 1; len--) {
    vll nxt(len - 1);
    for (int i = 0; i < len - 1; i++)
      nxt[i] = llabs(a[i + 1] - a[i]);
    a.swap(nxt);
  }

  cout << a[0] << "\n";

  return 0;
}
```
