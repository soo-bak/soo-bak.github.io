---
layout: single
title: "[백준 11759] Bottled-Up Feelings (C#, C++) - soo:bak"
date: "2025-12-06 20:55:00 +0900"
description: 두 용기 부피를 사용해 전체 용량을 정확히 채우되 병 개수를 최소화하는 백준 11759번 Bottled-Up Feelings 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[11759번 - Bottled-Up Feelings](https://www.acmicpc.net/problem/11759)

## 설명
총 유량을 큰 병과 작은 병 두 종류에 정확히 담습니다. 모든 병은 꽉 채워야 하고, 사용한 병의 총 개수가 최소가 되어야 합니다.

가능한 조합을 찾아 큰 병 개수와 작은 병 개수를 출력하고, 불가능하면 Impossible을 출력하는 문제입니다.

<br>

## 접근법
먼저, 병 개수를 최소화하려면 큰 병을 최대한 많이 쓰는 것이 유리합니다.

다음으로, 큰 병 개수를 최대값부터 0까지 감소시키며 남은 용량이 작은 병으로 나누어떨어지는지 확인합니다.

이후, 처음으로 나누어떨어지는 시점이 곧 병 개수가 최소인 해입니다. 끝까지 찾지 못하면 Impossible을 출력합니다.

<br>

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var parts = Console.ReadLine()!.Split();
      var s = int.Parse(parts[0]);
      var v1 = int.Parse(parts[1]);
      var v2 = int.Parse(parts[2]);

      var big = s / v1;
      while (big >= 0 && (s - big * v1) % v2 != 0)
        big--;

      if (big >= 0) {
        var small = (s - big * v1) / v2;
        Console.WriteLine($"{big} {small}");
      } else Console.WriteLine("Impossible");
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

  int s, v1, v2; cin >> s >> v1 >> v2;

  int big = s / v1;
  while (big >= 0 && (s - big * v1) % v2 != 0)
    big--;

  if (big >= 0) {
    int small = (s - big * v1) / v2;
    cout << big << " " << small << "\n";
  } else cout << "Impossible\n";

  return 0;
}
```
