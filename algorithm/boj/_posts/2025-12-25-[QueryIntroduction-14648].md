---
layout: single
title: "[백준 14648] 쿼리 맛보기 (C#, C++) - soo:bak"
date: "2025-12-25 14:56:00 +0900"
description: "백준 14648번 C#, C++ 풀이 - 구간 합을 계산하고 필요 시 원소를 교환하는 쿼리 처리 문제"
tags:
  - 백준
  - BOJ
  - 14648
  - C#
  - C++
  - 알고리즘
keywords: "백준 14648, 백준 14648번, BOJ 14648, QueryIntroduction, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14648번 - 쿼리 맛보기](https://www.acmicpc.net/problem/14648)

## 설명
길이 n의 수열에서 구간 합을 계산하고, 쿼리 유형에 따라 두 구간의 차를 출력하거나 원소를 교환하는 문제입니다.

<br>

## 접근법
n과 q의 범위가 크지 않으므로 매 쿼리마다 구간 합을 직접 계산해도 충분합니다.

1번 쿼리는 구간 합을 출력한 뒤 해당 위치의 값을 교환하고, 2번 쿼리는 두 구간 합의 차를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static long RangeSum(long[] arr, int l, int r) {
    long sum = 0;
    for (var i = l; i <= r; i++) sum += arr[i];
    return sum;
  }

  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var q = int.Parse(first[1]);

    var nums = Console.ReadLine()!.Split();
    var arr = new long[n];
    for (var i = 0; i < n; i++) arr[i] = long.Parse(nums[i]);

    for (var i = 0; i < q; i++) {
      var parts = Console.ReadLine()!.Split();
      var type = int.Parse(parts[0]);
      if (type == 1) {
        var a = int.Parse(parts[1]) - 1;
        var b = int.Parse(parts[2]) - 1;
        Console.WriteLine(RangeSum(arr, a, b));
        var tmp = arr[a];
        arr[a] = arr[b];
        arr[b] = tmp;
      } else {
        var a = int.Parse(parts[1]) - 1;
        var b = int.Parse(parts[2]) - 1;
        var c = int.Parse(parts[3]) - 1;
        var d = int.Parse(parts[4]) - 1;
        Console.WriteLine(RangeSum(arr, a, b) - RangeSum(arr, c, d));
      }
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<long long> vll;

long long rangeSum(const vll& arr, int l, int r) {
  long long sum = 0;
  for (int i = l; i <= r; i++) sum += arr[i];
  return sum;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, q; cin >> n >> q;
  vll arr(n);
  for (int i = 0; i < n; i++) cin >> arr[i];

  for (int i = 0; i < q; i++) {
    int type; cin >> type;
    if (type == 1) {
      int a, b; cin >> a >> b;
      a--; b--;
      cout << rangeSum(arr, a, b) << "\n";
      swap(arr[a], arr[b]);
    } else {
      int a, b, c, d; cin >> a >> b >> c >> d;
      a--; b--; c--; d--;
      cout << rangeSum(arr, a, b) - rangeSum(arr, c, d) << "\n";
    }
  }

  return 0;
}
```
