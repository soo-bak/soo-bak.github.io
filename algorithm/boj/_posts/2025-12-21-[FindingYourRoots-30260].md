---
layout: single
title: "[백준 30260] Finding Your Roots (C#, C++) - soo:bak"
date: "2025-12-21 09:00:00 +0900"
description: 단방향 부모 관계에서 한 개체의 조상 깊이를 따라가 세는 문제
---

## 문제 링크
[30260번 - Finding Your Roots](https://www.acmicpc.net/problem/30260)

## 설명
한 개체에서 시작해 부모를 따라 올라가며 알 수 있는 조상의 수를 구하는 문제입니다.

<br>

## 접근법
각 개체의 부모 정보가 주어지고, 부모가 0이면 더 이상 알 수 없다는 의미입니다. 관심 대상에서 시작해 부모를 따라가며 개수를 셉니다. 자기 자신도 포함하므로 시작점부터 카운트를 증가시키고, 부모가 0이 될 때까지 반복합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var k = int.Parse(Console.ReadLine()!);

    for (var tc = 1; tc <= k; tc++) {
      var first = Console.ReadLine()!.Split();
      var l = int.Parse(first[0]);
      var n = int.Parse(first[1]);
      var p = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var parent = new int[n + 1];
      for (var i = 1; i <= n; i++)
        parent[i] = p[i - 1];

      var cur = l;
      var cnt = 0;
      while (cur != 0) {
        cnt++;
        cur = parent[cur];
      }

      Console.WriteLine($"Data Set {tc}:");
      Console.WriteLine(cnt);
      Console.WriteLine();
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

  int k; cin >> k;

  for (int tc = 1; tc <= k; tc++) {
    int l, n; cin >> l >> n;
    vi parent(n + 1);
    for (int i = 1; i <= n; i++)
      cin >> parent[i];

    int cur = l, cnt = 0;
    while (cur != 0) {
      cnt++;
      cur = parent[cur];
    }

    cout << "Data Set " << tc << ":\n" << cnt << "\n\n";
  }

  return 0;
}
```
