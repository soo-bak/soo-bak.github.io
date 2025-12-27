---
layout: single
title: "[백준 32279] 수열의 비밀 (Easy) (C#, C++) - soo:bak"
date: "2025-12-27 16:05:00 +0900"
description: "백준 32279번 C#, C++ 풀이 - 점화식에 따라 수열을 생성하고 합을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 32279
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 32279, 백준 32279번, BOJ 32279, SecretOfSequence, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32279번 - 수열의 비밀 (Easy)](https://www.acmicpc.net/problem/32279)

## 설명
주어진 점화식에 따라 수열을 생성하고, 첫째 항부터 n번째 항까지의 합을 구하는 문제입니다.

점화식은 인덱스가 짝수일 때와 홀수일 때 다르게 적용됩니다.

<br>

## 접근법
2부터 n까지 순회하며 각 인덱스에 맞는 점화식을 적용합니다.

짝수 인덱스면 p * a[i/2] + q, 홀수 인덱스면 r * a[i/2] + s로 계산하고, 모든 항의 합을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var pqrs = Console.ReadLine()!.Split();
    var p = int.Parse(pqrs[0]);
    var q = int.Parse(pqrs[1]);
    var r = int.Parse(pqrs[2]);
    var s = int.Parse(pqrs[3]);
    var a1 = int.Parse(Console.ReadLine()!);

    var v = new int[n + 1];
    v[1] = a1;
    var sum = v[1];

    for (var i = 2; i <= n; i++) {
      v[i] = (i % 2 == 0 ? p * v[i / 2] + q : r * v[i / 2] + s);
      sum += v[i];
    }

    Console.WriteLine(sum);
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

  int n, p, q, r, s; cin >> n >> p >> q >> r >> s;
  vi v(n + 1);
  cin >> v[1];

  int sum = v[1];
  for (int i = 2; i <= n; i++) {
    v[i] = (i % 2 == 0 ? p * v[i / 2] + q : r * v[i / 2] + s);
    sum += v[i];
  }

  cout << sum << "\n";

  return 0;
}
```

