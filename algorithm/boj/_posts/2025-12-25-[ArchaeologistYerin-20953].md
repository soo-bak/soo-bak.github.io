---
layout: single
title: "[백준 20953] 고고학자 예린 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 삼중 반복문의 반복 횟수를 수식으로 계산하는 백준 20953번 고고학자 예린 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[20953번 - 고고학자 예린](https://www.acmicpc.net/problem/20953)

## 설명
주어진 함수 dolmen(a, b)가 반환하는 값을 계산하는 문제입니다.

<br>

## 접근법
먼저, 가장 안쪽 루프는 0부터 j - 1까지 반복하므로 횟수는 j입니다.

다음으로, 바깥 두 루프는 각각 0부터 a + b - 1까지 반복하므로, 전체 합은 (a + b) × (0 + 1 + ... + (a + b - 1))입니다.

이를 정리하면 (a + b - 1) × (a + b) × (a + b) / 2가 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var t = long.Parse(parts[idx++]);

    var sb = new StringBuilder();
    for (var i = 0L; i < t; i++) {
      var a = long.Parse(parts[idx++]);
      var b = long.Parse(parts[idx++]);
      sb.AppendLine(((a + b - 1) * (a + b) * (a + b) / 2).ToString());
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll t; cin >> t;
  while (t--) {
    ll a, b; cin >> a >> b;
    cout << (a + b - 1) * (a + b) * (a + b) / 2 << "\n";
  }

  return 0;
}
```
