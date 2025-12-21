---
layout: single
title: "[백준 13456] Richard Hamming (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: 두 벡터의 해밍 거리를 여러 테스트케이스에 대해 계산하는 문제
---

## 문제 링크
[13456번 - Richard Hamming](https://www.acmicpc.net/problem/13456)

## 설명
두 벡터 사이의 해밍 거리를 구하는 문제입니다.

<br>

## 접근법
해밍 거리는 두 벡터에서 같은 위치에 있는 원소가 서로 다른 개수를 의미합니다. 두 벡터의 각 위치를 순회하면서 원소가 다르면 카운트를 증가시킵니다. 모든 위치를 확인한 뒤 카운트된 값이 해밍 거리가 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var tc = 0; tc < t; tc++) {
      var n = int.Parse(Console.ReadLine()!);
      var v = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      var u = Console.ReadLine()!.Split().Select(int.Parse).ToArray();

      var dist = 0;
      for (var i = 0; i < n; i++) {
        if (v[i] != u[i]) dist++;
      }

      Console.WriteLine(dist);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    vi v(n), u(n);
    for (int i = 0; i < n; i++)
      cin >> v[i];
    for (int i = 0; i < n; i++)
      cin >> u[i];

    int dist = 0;
    for (int i = 0; i < n; i++) {
      if (v[i] != u[i]) dist++;
    }

    cout << dist << "\n";
  }

  return 0;
}
```
