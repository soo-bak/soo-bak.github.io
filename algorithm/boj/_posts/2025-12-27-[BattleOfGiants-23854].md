---
layout: single
title: "[백준 23854] The Battle of Giants (C#, C++) - soo:bak"
date: "2025-12-27 03:55:00 +0900"
description: 최종 점수 a:b를 만들 수 있는 최소 경기 수와 승/무/패 개수를 구하는 문제
---

## 문제 링크
[23854번 - The Battle of Giants](https://www.acmicpc.net/problem/23854)

## 설명
승리 3점, 무승부 1점, 패배 0점일 때 최종 점수 a:b가 가능하면 최소 경기 수로 승/무/패 개수를 구하고, 불가능하면 -1을 출력하는 문제입니다.

<br>

## 접근법
승리는 3점, 무승부는 1점, 패배는 0점입니다. 두 점수를 3으로 나눈 나머지가 다르면 만들 수 없으므로 -1을 출력합니다.

나머지가 같다면 무승부 횟수는 나머지와 같고, 승리 횟수는 a를 3으로 나눈 몫, 패배 횟수는 b를 3으로 나눈 몫이 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var a = int.Parse(Console.ReadLine()!);
    var b = int.Parse(Console.ReadLine()!);

    if (a % 3 != b % 3)
      Console.WriteLine("-1");
    else
      Console.WriteLine($"{a / 3} {a % 3} {b / 3}");
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

  int a, b; cin >> a >> b;

  if (a % 3 != b % 3)
    cout << -1 << "\n";
  else
    cout << a / 3 << " " << a % 3 << " " << b / 3 << "\n";

  return 0;
}
```
