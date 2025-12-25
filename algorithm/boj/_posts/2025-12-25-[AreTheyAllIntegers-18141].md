---
layout: single
title: "[백준 18141] Are They All Integers? (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 모든 서로 다른 i, j, k에 대해 (A[i]-A[j])가 A[k]로 나눠지는지 판단하는 문제
---

## 문제 링크
[18141번 - Are They All Integers?](https://www.acmicpc.net/problem/18141)

## 설명
서로 다른 i, j, k에 대해 (A[i]−A[j]) / A[k]가 항상 정수인지 판별하는 문제입니다.

<br>

## 접근법
조건은 모든 세 원소 조합에 대해 나머지가 0인지 확인하면 됩니다.  
n이 50이므로 O(n^3)로 충분합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);
    var a = new int[n];
    for (var i = 0; i < n; i++)
      a[i] = int.Parse(parts[idx++]);

    for (var i = 0; i < n; i++) {
      for (var j = 0; j < n; j++) {
        if (i == j) continue;
        for (var k = 0; k < n; k++) {
          if (k == i || k == j) continue;
          if ((a[i] - a[j]) % a[k] != 0) {
            Console.WriteLine("no");
            return;
          }
        }
      }
    }

    Console.WriteLine("yes");
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

  int n; cin >> n;
  vector<int> a(n);
  for (int i = 0; i < n; i++) cin >> a[i];

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      if (i == j) continue;
      for (int k = 0; k < n; k++) {
        if (k == i || k == j) continue;
        if ((a[i] - a[j]) % a[k] != 0) {
          cout << "no\n";
          return 0;
        }
      }
    }
  }

  cout << "yes\n";

  return 0;
}
```
