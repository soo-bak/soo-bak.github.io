---
layout: single
title: "[백준 9349] Fegla and the Bed Bugs (C#, C++) - soo:bak"
date: "2025-12-27 11:15:00 +0900"
description: N칸에 K마리 벌레를 놓을 때 인접 벌레 사이 최소 빈칸을 최대로 하는 값 계산
---

## 문제 링크
[9349번 - Fegla and the Bed Bugs](https://www.acmicpc.net/problem/9349)

## 설명
일직선 칸에 벌레를 배치할 때, 인접한 벌레 사이의 빈칸 수 중 최솟값을 최대화하는 문제입니다.

<br>

## 접근법
벌레가 차지하는 칸을 제외한 빈칸을 인접 구간에 균등하게 나눕니다.

전체 빈칸 수를 구간 수로 나눈 몫이 답입니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    while (t-- > 0) {
      var parts = Console.ReadLine()!.Split();
      var n = int.Parse(parts[0]);
      var k = int.Parse(parts[1]);
      var ans = (n - k) / (k - 1);
      Console.WriteLine(ans);
    }
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

  int t; cin >> t;
  while (t--) {
    int n, k; cin >> n >> k;
    int ans = (n - k) / (k - 1);
    cout << ans << "\n";
  }

  return 0;
}
```
