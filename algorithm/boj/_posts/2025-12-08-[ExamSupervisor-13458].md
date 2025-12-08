---
layout: single
title: "[백준 13458] 시험 감독 (C#, C++) - soo:bak"
date: "2025-12-08 03:25:00 +0900"
description: 각 시험장마다 총감독 1명과 부감독 여러 명을 배치할 때 필요한 감독관 최소 수를 구하는 백준 13458번 시험 감독 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[13458번 - 시험 감독](https://www.acmicpc.net/problem/13458)

## 설명
각 시험장에 총감독 1명을 반드시 배치하고, 남은 응시자를 부감독이 감시할 때 필요한 감독관의 최소 인원을 구하는 문제입니다.

<br>

## 접근법
각 시험장을 순서대로 처리합니다. 먼저 총감독 1명을 배치하고, 총감독이 감시할 수 있는 인원만큼 뺍니다. 남은 응시자가 있으면 부감독을 추가로 배치합니다. 부감독 한 명이 감시할 수 있는 인원으로 나눈 뒤 올림하면 필요한 부감독 수가 됩니다.

시험장 수가 최대 백만 개이고 응시자도 많을 수 있으므로 답을 64비트 정수로 누적해야 합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var parts = Console.ReadLine()!.Split();
    var a = new int[n];
    for (var i = 0; i < n; i++) a[i] = int.Parse(parts[i]);
    var bc = Console.ReadLine()!.Split();
    var b = int.Parse(bc[0]);
    var c = int.Parse(bc[1]);

    var ans = 0L;
    foreach (var x0 in a) {
      var x = x0 - b;
      ans++;
      if (x > 0) ans += (x + c - 1) / c;
    }
    Console.WriteLine(ans);
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
  for (int i = 0; i < n; i++) cin >> a[i];
  int b, c; cin >> b >> c;

  ll ans = 0;
  for (int x : a) {
    x -= b;
    ans++;
    if (x > 0) ans += (x + c - 1) / c;
  }
  cout << ans << "\n";

  return 0;
}
```
