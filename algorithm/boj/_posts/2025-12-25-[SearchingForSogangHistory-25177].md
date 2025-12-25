---
layout: single
title: "[백준 25177] 서강의 역사를 찾아서 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 한 장소를 예전 시설로 바꿀 때 점수 증가량의 최댓값을 구하는 문제
---

## 문제 링크
[25177번 - 서강의 역사를 찾아서](https://www.acmicpc.net/problem/25177)

## 설명
현재 점수와 신입생 시절 점수가 주어질 때, 최대 한 장소를 예전 시설로 바꿔 얻는 점수 증가량의 최댓값을 구하는 문제입니다.

<br>

## 접근법
각 장소 i의 증가량은 `b_i - a_i`이며, 범위를 벗어나면 해당 값은 0으로 취급합니다.  
모든 장소에 대해 증가량의 최댓값과 0을 비교해 출력합니다.

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

    var b = new int[m];
    for (var i = 0; i < m; i++)
      b[i] = int.Parse(parts[idx++]);

    var max = 0;
    var len = n > m ? n : m;
    for (var i = 0; i < len; i++) {
      var cur = i < n ? a[i] : 0;
      var old = i < m ? b[i] : 0;
      var diff = old - cur;
      if (diff > max) max = diff;
    }

    Console.WriteLine(max);
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
  vector<int> a(n), b(m);
  for (int i = 0; i < n; i++) cin >> a[i];
  for (int i = 0; i < m; i++) cin >> b[i];

  int mx = 0;
  int len = max(n, m);
  for (int i = 0; i < len; i++) {
    int cur = i < n ? a[i] : 0;
    int old = i < m ? b[i] : 0;
    int diff = old - cur;
    if (diff > mx) mx = diff;
  }

  cout << mx << "\n";

  return 0;
}
```
