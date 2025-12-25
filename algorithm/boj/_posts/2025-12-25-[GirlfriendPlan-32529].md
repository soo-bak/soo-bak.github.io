---
layout: single
title: "[백준 32529] 래환이의 여자친구 사귀기 대작전 (C#, C++) - soo:bak"
date: "2025-12-25 21:03:00 +0900"
description: 뒤에서부터 누적 합으로 시작 날을 찾는 문제
---

## 문제 링크
[32529번 - 래환이의 여자친구 사귀기 대작전](https://www.acmicpc.net/problem/32529)

## 설명
다이어트를 늦게 시작하면서도 목표 감량을 채울 수 있는 시작 날짜를 구하는 문제입니다.

<br>

## 접근법
마지막 날부터 거꾸로 합을 쌓아가면, 처음으로 목표를 넘기는 순간이 가장 늦게 시작할 수 있는 날입니다.  
끝까지 합이 목표에 도달하지 못하면 시작해도 성공할 수 없으므로 -1을 출력합니다.

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
    var m = int.Parse(parts[idx++]);

    var a = new int[n];
    for (var i = 0; i < n; i++)
      a[i] = int.Parse(parts[idx++]);

    var sum = 0;
    var ans = -1;
    for (var i = n - 1; i >= 0; i--) {
      sum += a[i];
      if (sum >= m) { ans = i + 1; break; }
    }

    Console.WriteLine(ans);
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

  int n, m; cin >> n >> m;
  vector<int> a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  int sum = 0;
  int ans = -1;
  for (int i = n - 1; i >= 0; i--) {
    sum += a[i];
    if (sum >= m) { ans = i + 1; break; }
  }

  cout << ans << "\n";

  return 0;
}
```
