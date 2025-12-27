---
layout: single
title: "[백준 21180] Reconstruct Sum (C#, C++) - soo:bak"
date: "2025-12-27 10:15:00 +0900"
description: 주어진 수 중 하나가 나머지 모든 수의 합과 같은지 찾아 출력하는 문제
---

## 문제 링크
[21180번 - Reconstruct Sum](https://www.acmicpc.net/problem/21180)

## 설명
주어진 정수들 중 하나가 나머지 모든 수의 합과 같은지 판별하는 문제입니다. 있다면 그 값을, 없으면 BAD를 출력합니다.

<br>

## 접근법
어떤 수가 나머지의 합과 같으려면, 그 수는 전체 합의 절반이어야 합니다.

전체 합이 짝수이고 절반 값이 입력에 존재하면 그 값을 출력하고, 아니면 BAD를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var nums = new List<long>(n);
    long sum = 0;
    var freq = new Dictionary<long, int>();

    for (var i = 0; i < n; i++) {
      var v = long.Parse(Console.ReadLine()!);
      nums.Add(v);
      sum += v;
      if (!freq.ContainsKey(v)) freq[v] = 0;
      freq[v]++;
    }

    if (sum % 2 != 0) {
      Console.WriteLine("BAD");
      return;
    }

    var target = sum / 2;
    if (freq.ContainsKey(target)) Console.WriteLine(target);
    else Console.WriteLine("BAD");
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

  int n; cin >> n;
  unordered_map<ll, int> freq;
  ll sum = 0;
  for (int i = 0; i < n; i++) {
    ll v; cin >> v;
    sum += v;
    freq[v]++;
  }

  if (sum % 2 != 0) {
    cout << "BAD\n";
    return 0;
  }

  ll target = sum / 2;
  if (freq.count(target)) cout << target << "\n";
  else cout << "BAD\n";

  return 0;
}
```
