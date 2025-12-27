---
layout: single
title: "[백준 3554] Enigmatic Device (C#, C++) - soo:bak"
date: "2025-12-27 14:01:00 +0900"
description: "백준 3554번 C#, C++ 풀이 - 구간 제곱 연산과 구간 합 쿼리를 처리하는 시뮬레이션 문제"
tags:
  - 백준
  - BOJ
  - 3554
  - C#
  - C++
  - 알고리즘
keywords: "백준 3554, 백준 3554번, BOJ 3554, EnigmaticDevice, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3554번 - Enigmatic Device](https://www.acmicpc.net/problem/3554)

## 설명
수열에 대해 두 가지 연산을 수행하는 문제입니다.

첫 번째 연산은 주어진 구간의 각 원소를 제곱하고 2010으로 나눈 나머지로 갱신하는 것이고, 두 번째 연산은 주어진 구간의 합을 출력하는 것입니다.

<br>

## 접근법
수열의 길이 n과 초기 수열을 입력받은 후, 각 연산의 종류에 따라 처리합니다.

연산 종류가 1이면 구간 내 모든 원소에 대해 제곱 후 2010으로 나눈 나머지를 저장합니다. 연산 종류가 2이면 구간 내 모든 원소의 합을 계산하여 출력합니다.

<br>

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);

    var a = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);

    var m = int.Parse(Console.ReadLine()!);

    var sb = new StringBuilder();
    for (var i = 0; i < m; i++) {
      var query = Console.ReadLine()!.Split();
      var kind = int.Parse(query[0]);
      var l = int.Parse(query[1]) - 1;
      var r = int.Parse(query[2]) - 1;

      if (kind == 1) {
        for (var j = l; j <= r; j++)
          a[j] = (a[j] * a[j]) % 2010;
      } else {
        var sum = 0L;
        for (var j = l; j <= r; j++)
          sum += a[j];
        sb.AppendLine(sum.ToString());
      }
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  int m; cin >> m;

  for (int i = 0; i < m; i++) {
    int kind, l, r;
    cin >> kind >> l >> r;
    l--; r--;

    if (kind == 1) {
      for (int j = l; j <= r; j++)
        a[j] = (a[j] * a[j]) % 2010;
    } else {
      ll sum = 0;
      for (int j = l; j <= r; j++)
        sum += a[j];
      cout << sum << "\n";
    }
  }

  return 0;
}
```

