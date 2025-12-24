---
layout: single
title: "[백준 32604] Jumbled Scoreboards (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: 두 팀 점수가 시간에 따라 감소하지 않는지 확인하는 문제
---

## 문제 링크
[32604번 - Jumbled Scoreboards](https://www.acmicpc.net/problem/32604)

## 설명
사진에 나온 점수들이 시간 순서인지 확인하는 문제입니다.

<br>

## 접근법
점수는 시간이 지나면서 감소하지 않습니다.

이전 점수와 비교해 두 팀 중 하나라도 감소하면 no, 끝까지 감소가 없으면 yes를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var first = Console.ReadLine()!.Split();
    var prevA = int.Parse(first[0]);
    var prevB = int.Parse(first[1]);

    for (var i = 1; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var a = int.Parse(parts[0]);
      var b = int.Parse(parts[1]);
      if (a < prevA || b < prevB) {
        Console.WriteLine("no");
        return;
      }
      prevA = a;
      prevB = b;
    }

    Console.WriteLine("yes");
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

  int n; cin >> n;
  int prevA, prevB; cin >> prevA >> prevB;
  for (int i = 1; i < n; i++) {
    int a, b; cin >> a >> b;
    if (a < prevA || b < prevB) {
      cout << "no\n";
      return 0;
    }
    prevA = a;
    prevB = b;
  }

  cout << "yes\n";

  return 0;
}
```
