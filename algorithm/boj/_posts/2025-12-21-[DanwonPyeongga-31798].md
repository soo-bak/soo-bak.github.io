---
layout: single
title: "[백준 31798] 단원평가 (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: a+b=c^2 관계에서 하나의 빈칸을 채워 양의 정수를 구하는 문제
---

## 문제 링크
[31798번 - 단원평가](https://www.acmicpc.net/problem/31798)

## 설명
a + b = c² 관계에서 하나의 빈칸을 채워 양의 정수를 구하는 문제입니다.

<br>

## 접근법
세 수 중 하나가 0으로 주어지고 나머지는 양수입니다. c가 0이면 a와 b의 합에 제곱근을 취하고, a나 b가 0이면 c의 제곱에서 다른 값을 빼면 됩니다. 항상 정수 해가 존재하므로 계산 결과를 그대로 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = int.Parse(parts[0]);
    var b = int.Parse(parts[1]);
    var c = int.Parse(parts[2]);

    var ans = 0;
    if (c == 0) ans = (int)Math.Sqrt(a + b);
    else if (a == 0) ans = c * c - b;
    else ans = c * c - a;

    Console.WriteLine(ans);
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

  int a, b, c; cin >> a >> b >> c;

  int ans = 0;
  if (c == 0) ans = (int)sqrt(a + b);
  else if (a == 0) ans = c * c - b;
  else ans = c * c - a;

  cout << ans << "\n";

  return 0;
}
```
