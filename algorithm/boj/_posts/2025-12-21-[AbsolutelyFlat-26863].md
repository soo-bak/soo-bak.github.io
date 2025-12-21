---
layout: single
title: "[백준 26863] Absolutely Flat (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 한 다리에 패드를 붙이거나 붙이지 않아 네 다리 길이를 같게 만들 수 있는지 판별하는 문제
---

## 문제 링크
[26863번 - Absolutely Flat](https://www.acmicpc.net/problem/26863)

## 설명
네 다리 길이와 패드 길이가 주어질 때, 패드를 한 다리에 붙이거나 붙이지 않아 네 다리 길이를 같게 만들 수 있는지 확인하는 문제입니다.

<br>

## 접근법
먼저 패드를 붙이지 않았을 때 네 다리 길이가 모두 같은지 확인합니다.

이후 각 다리에 패드를 붙이는 경우를 한 번씩 시도해 모든 길이가 같아지는지 확인합니다. 하나라도 성립하면 1, 아니면 0을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var a = new int[4];
    for (var i = 0; i < 4; i++)
      a[i] = int.Parse(Console.ReadLine()!);
    var b = int.Parse(Console.ReadLine()!);

    bool Flat(int[] v) {
      return v[0] == v[1] && v[1] == v[2] && v[2] == v[3];
    }

    if (Flat(a)) {
      Console.WriteLine(1);
      return;
    }

    for (var i = 0; i < 4; i++) {
      a[i] += b;
      if (Flat(a)) {
        Console.WriteLine(1);
        return;
      }
      a[i] -= b;
    }

    Console.WriteLine(0);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

bool flat(const int a[4]) {
  return a[0] == a[1] && a[1] == a[2] && a[2] == a[3];
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int a[4];
  for (int i = 0; i < 4; i++)
    cin >> a[i];
  int b; cin >> b;

  if (flat(a)) {
    cout << 1 << "\n";
    return 0;
  }

  for (int i = 0; i < 4; i++) {
    a[i] += b;
    if (flat(a)) {
      cout << 1 << "\n";
      return 0;
    }
    a[i] -= b;
  }

  cout << 0 << "\n";

  return 0;
}
```
