---
layout: single
title: "[백준 2028] 자기복제수 (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: 제곱수의 끝자리가 원래 수와 같은지 확인하는 문제
---

## 문제 링크
[2028번 - 자기복제수](https://www.acmicpc.net/problem/2028)

## 설명
자연수 N의 제곱이 N으로 끝나는지 확인해 YES/NO를 출력하는 문제입니다.

<br>

## 접근법
제곱수를 계산한 뒤, 원래 수의 자릿수에 해당하는 10의 거듭제곱으로 나머지를 구합니다.

이후 나머지가 원래 수와 같으면 YES, 아니면 NO를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < t; i++) {
      var n = int.Parse(Console.ReadLine()!);
      var sq = n * n;
      var mod = 1;
      var tmp = n;
      while (tmp > 0) {
        mod *= 10;
        tmp /= 10;
      }
      Console.WriteLine(sq % mod == n ? "YES" : "NO");
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
    int n; cin >> n;
    int sq = n * n;
    int mod = 1;
    int tmp = n;
    while (tmp > 0) {
      mod *= 10;
      tmp /= 10;
    }
    cout << (sq % mod == n ? "YES" : "NO") << "\n";
  }

  return 0;
}
```
