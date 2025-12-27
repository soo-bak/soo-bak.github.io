---
layout: single
title: "[백준 17173] 배수들의 합 (C#, C++) - soo:bak"
date: "2025-12-09 12:10:00 +0900"
description: 주어진 K들의 배수 중 1..N 범위에 속하는 수를 합산하는 백준 17173번 배수들의 합 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17173
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 브루트포스
keywords: "백준 17173, 백준 17173번, BOJ 17173, SumOfMultiples, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17173번 - 배수들의 합](https://www.acmicpc.net/problem/17173)

## 설명
1 이상 N 이하의 수 중에서 주어진 M개 수 Ki 중 하나라도 배수인 수를 모두 더하는 문제입니다. 동일한 수는 한 번만 더해야 합니다.

<br>

## 접근법
N이 1000 이하이므로 단순한 완전탐색으로 충분합니다. 1부터 N까지 순회하며 각 수가 주어진 수 중 하나로 나누어떨어지는지 확인합니다. 나누어떨어지면 합에 더하고 바로 다음 수로 넘어가서 중복으로 더하는 것을 방지합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line1 = Console.ReadLine()!.Split();
    var n = int.Parse(line1[0]);
    var m = int.Parse(line1[1]);
    var k = new int[m];
    var line2 = Console.ReadLine()!.Split();
    for (var i = 0; i < m; i++)
      k[i] = int.Parse(line2[i]);

    var sum = 0;
    for (var x = 1; x <= n; x++) {
      for (var i = 0; i < m; i++) {
        if (x % k[i] == 0) { sum += x; break; }
      }
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

  int n, m; cin >> n >> m;
  vi k(m);
  for (int i = 0; i < m; i++)
    cin >> k[i];

  int sum = 0;
  for (int x = 1; x <= n; x++) {
    for (int i = 0; i < m; i++) {
      if (x % k[i] == 0) { sum += x; break; }
    }
  }

  cout << sum << "\n";

  return 0;
}
```
