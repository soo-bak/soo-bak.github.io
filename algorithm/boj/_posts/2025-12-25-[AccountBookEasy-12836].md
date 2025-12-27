---
layout: single
title: "[백준 12836] 가계부 (Easy) (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 누적합을 이용하여 수입/지출 추가와 구간 합을 처리하는 백준 12836번 가계부 (Easy) 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 12836
  - C#
  - C++
  - 알고리즘
keywords: "백준 12836, 백준 12836번, BOJ 12836, AccountBookEasy, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12836번 - 가계부 (Easy)](https://www.acmicpc.net/problem/12836)

## 설명
생후 p일에 수입/지출을 추가하고, p일부터 q일까지의 변화 합을 구하는 문제입니다.

<br>

## 접근법
먼저, 각 일자별 수입/지출을 저장할 배열과 누적합 배열을 준비합니다.

다음으로, 쿼리 1이 들어오면 해당 일자에 금액을 더하고, 쿼리 2가 들어오면 누적합 배열을 이용해 구간 합을 계산합니다.

이후, 매 쿼리마다 누적합 배열을 갱신하여 최신 상태를 유지합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);
    var q = int.Parse(parts[idx++]);
    var money = new long[n + 1];
    var sum = new long[n + 1];

    var sb = new StringBuilder();
    for (var i = 0; i < q; i++) {
      var query = int.Parse(parts[idx++]);
      var p = int.Parse(parts[idx++]);
      var x = long.Parse(parts[idx++]);

      if (query == 1) money[p] += x;
      else {
        var r = (int)x;
        sb.AppendLine((sum[r] - sum[p - 1]).ToString());
      }

      for (var j = 1; j <= n; j++)
        sum[j] = sum[j - 1] + money[j];
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
typedef vector<ll> vll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, q; cin >> n >> q;
  vll money(n + 1, 0);
  vll sum(n + 1, 0);

  while (q--) {
    int query, p; ll x; cin >> query >> p >> x;

    if (query == 1) money[p] += x;
    else {
      int r = x;
      cout << sum[r] - sum[p - 1] << "\n";
    }

    for (int i = 1; i <= n; i++)
      sum[i] = sum[i - 1] + money[i];
  }

  return 0;
}
```
