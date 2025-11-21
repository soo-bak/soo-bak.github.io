---
layout: single
title: "[백준 17256] 달달함이 넘쳐흘러 (C#, C++) - soo:bak"
date: "2025-11-22 03:04:00 +0900"
description: 케이크 수 연산 a 🍰 b = (a.z + b.x, a.y × b.y, a.x + b.z)를 역으로 풀어 b를 구하는 백준 17256번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[17256번 - 달달함이 넘쳐흘러](https://www.acmicpc.net/problem/17256)

## 설명

케이크 수는 세 개의 정수 `(x, y, z)`로 구성됩니다.

두 케이크 수 `a`와 `b`에 대한 연산 `🍰`는 `a 🍰 b = (a.z + b.x, a.y × b.y, a.x + b.z)`로 정의됩니다.

케이크 수 `a`와 `c`가 주어질 때, `a 🍰 b = c`를 만족하는 케이크 수 `b`를 구해야 합니다.

<br>

## 접근법

`a 🍰 b = c`의 정의에 따라 각 좌표별로 방정식을 세우면 `c.x = a.z + b.x`, `c.y = a.y × b.y`, `c.z = a.x + b.z`입니다.

이를 `b`에 대해 정리하면 `b.x = c.x - a.z`, `b.y = c.y / a.y`, `b.z = c.z - a.x`가 됩니다.

문제 조건상 항상 나누어떨어지므로, 이 식을 그대로 계산하여 출력하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    struct Cake { public int x, y, z; }

    static void Main(string[] args) {
      var aTokens = Console.ReadLine()!.Split();
      var cTokens = Console.ReadLine()!.Split();

      var a = new Cake {
        x = int.Parse(aTokens[0]),
        y = int.Parse(aTokens[1]),
        z = int.Parse(aTokens[2])
      };
      var c = new Cake {
        x = int.Parse(cTokens[0]),
        y = int.Parse(cTokens[1]),
        z = int.Parse(cTokens[2])
      };

      var bx = c.x - a.z;
      var by = c.y / a.y;
      var bz = c.z - a.x;

      Console.WriteLine($"{bx} {by} {bz}");
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Cake { int x, y, z; };

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  Cake a, c;
  cin >> a.x >> a.y >> a.z;
  cin >> c.x >> c.y >> c.z;

  int bx = c.x - a.z;
  int by = c.y / a.y;
  int bz = c.z - a.x;

  cout << bx << " " << by << " " << bz << "\n";

  return 0;
}
```

