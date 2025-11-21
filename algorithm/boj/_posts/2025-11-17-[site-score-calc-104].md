---
layout: single
title: "[백준 20254] Site Score (C#, C++) - soo:bak"
date: "2025-11-17 23:03:00 +0900"
description: 사이트 점수 공식 56UR + 24TR + 14UO + 6TO를 그대로 적용하는 백준 20254번 Site Score 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[20254번 - Site Score](https://www.acmicpc.net/problem/20254)

## 설명

사이트의 점수를 계산하는 문제입니다.<br>

네 가지 지표 `UR`, `TR`, `UO`, `TO`가 주어지며, 각각에 정해진 가중치를 곱하여 합산합니다.<br>

사이트 점수는 `56 × UR + 24 × TR + 14 × UO + 6 × TO`로 계산됩니다.<br>

<br>

## 접근법

네 개의 값을 입력받아 주어진 공식에 대입하여 계산한 결과를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var ur = int.Parse(tokens[0]);
      var tr = int.Parse(tokens[1]);
      var uo = int.Parse(tokens[2]);
      var to = int.Parse(tokens[3]);

      Console.WriteLine(56 * ur + 24 * tr + 14 * uo + 6 * to);
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

  int ur, tr, uo, to; cin >> ur >> tr >> uo >> to;
  cout << 56 * ur + 24 * tr + 14 * uo + 6 * to << "\n";

  return 0;
}
```

