---
layout: single
title: "[백준 10599] 페르시아의 왕들 (C#, C++) - soo:bak"
date: "2025-05-02 06:06:00 +0900"
description: 출생과 사망 시기의 추정 범위를 바탕으로 최소 나이와 최대 나이를 계산하는 백준 10599번 페르시아의 왕들 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[10599번 - 페르시아의 왕들](https://www.acmicpc.net/problem/10599)

## 설명
한 인물의 생몰 연도 추정 범위가 주어졌을 때, **그가 살았을 수 있는 최소 나이와 최대 나이**를 계산하는 문제입니다.

<br>
입력은 네 개의 정수로 주어집니다:

- `[a, b]`: 출생일 추정 범위
- `[c, d]`: 사망일 추정 범위

출생일은 `a`~`b`, 사망일은 `c`~`d`라고 했을 때<br>
- **최소 나이**: `c - b`
- **최대 나이**: `d - a`

연도는 BC 포함 범위이기 때문에 음수도 들어올 수 있음에 주의합니다.

<br>

## 접근법

- 각 줄마다 `4개`의 정수를 입력받습니다.
- 입력이 `0 0 0 0`이면 종료합니다.
- 각 줄마다 최소 나이와 최대 나이를 계산하여 출력합니다.

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    while (true) {
      var line = Console.ReadLine().Split();
      int a = int.Parse(line[0]);
      int b = int.Parse(line[1]);
      int c = int.Parse(line[2]);
      int d = int.Parse(line[3]);

      if (a == 0 && b == 0 && c == 0 && d == 0) break;

      int minAge = c - b;
      int maxAge = d - a;
      Console.WriteLine($"{minAge} {maxAge}");
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

  while (true) {
    int sB, eB, sD, eD; cin >> sB >> eB >> sD >> eD;
    if (!sB && !eB && !sD && !eD) break;
    cout << sD - eB << " " << eD - sB << "\n";
  }

  return 0;
}
```
