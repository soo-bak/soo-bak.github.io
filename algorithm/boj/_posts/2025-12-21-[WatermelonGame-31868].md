---
layout: single
title: "[백준 31868] 수박 게임 (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 체리 K개로 만들 수 있는 수박 개수를 2^(N-1)로 나누어 구하는 문제
---

## 문제 링크
[31868번 - 수박 게임](https://www.acmicpc.net/problem/31868)

## 설명
체리 K개에서 시작해 한 단계씩 두 개를 합쳐 N단계 수박을 만들 때, 만들 수 있는 수박의 최대 개수를 구하는 문제입니다.

<br>

## 접근법
수박 1개를 만들려면 단계마다 2배씩 필요하므로, 체리가 2의 거듭제곱 개만큼 필요합니다.

주어진 체리 개수를 필요한 체리 개수로 나누면 만들 수 있는 수박의 최대 개수를 구할 수 있습니다.

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

    var need = 1 << (n - 1);
    Console.WriteLine(k / need);
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
  int need = 1 << (n - 1);
  cout << k / need << "\n";

  return 0;
}
```
