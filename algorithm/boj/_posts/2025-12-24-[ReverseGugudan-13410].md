---
layout: single
title: "[백준 13410] 거꾸로 구구단 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: 구구단 결과를 뒤집어 최댓값을 구하는 문제
---

## 문제 링크
[13410번 - 거꾸로 구구단](https://www.acmicpc.net/problem/13410)

## 설명
N단의 1~K항 결과를 뒤집어 그중 최댓값을 구하는 문제입니다.

<br>

## 접근법
각 항의 곱을 문자열로 뒤집어 정수로 변환합니다.

모든 항 중 최댓값을 갱신해 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var n = int.Parse(parts[0]);
    var k = int.Parse(parts[1]);

    var best = 0;
    for (var i = 1; i <= k; i++) {
      var v = (n * i).ToString().ToCharArray();
      Array.Reverse(v);
      var val = int.Parse(new string(v));
      if (val > best) best = val;
    }

    Console.WriteLine(best);
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

  int n, k; cin >> n >> k;
  int best = 0;

  for (int i = 1; i <= k; i++) {
    int v = n * i;
    string s = to_string(v);
    reverse(s.begin(), s.end());
    int val = stoi(s);
    if (val > best) best = val;
  }

  cout << best << "\n";

  return 0;
}
```
