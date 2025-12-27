---
layout: single
title: "[백준 2712] 미국 스타일 (C#, C++) - soo:bak"
date: "2025-05-02 05:03:00 +0900"
description: 질량과 부피 단위를 서로 변환하는 미국 스타일 단위 변환 문제인 백준 2712번의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2712
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 2712, 백준 2712번, BOJ 2712, unitconvert, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2712번 - 미국 스타일](https://www.acmicpc.net/problem/2712)

## 설명
질량(kg ↔ lb)과 부피(l ↔ g)에 대한 단위가 서로 다른 경우,<br>
각 값에 대해 지정된 단위 변환 비율에 따라 변환값을 출력하는 문제입니다.

- 단위는 총 `4`가지: `kg`, `lb`, `l`, `g`
- 변환은 아래 비율을 따릅니다:

| 종류 | 미터법 → 미국 단위계 | 미국 단위계 → 미터법 |
|------|-----------------------|------------------------|
| 무게 | 1 kg = 2.2046 lb      | 1 lb = 0.4536 kg       |
| 부피 | 1 l  = 0.2642 g       | 1 g  = 3.7854 l        |

각 테스트 케이스마다 주어진 값을 변환하여 **소수점 넷째 자리까지 반올림**해 출력해야 합니다.

<br>

## 접근법

- 입력으로 주어진 값과 단위를 각각 읽습니다.
- 단위에 따라 변환 공식을 선택하여 변환값을 계산합니다.
- 단위를 함께 출력 형식에 포함하여 정답을 주어진 형식에 맞게 출력합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    for (int i = 0; i < t; i++) {
      var parts = Console.ReadLine().Split();
      double v = double.Parse(parts[0]);
      string u = parts[1];

      if (u == "kg") Console.WriteLine($"{(v * 2.2046):F4} lb");
      else if (u == "lb") Console.WriteLine($"{(v * 0.4536):F4} kg");
      else if (u == "l") Console.WriteLine($"{(v * 0.2642):F4} g");
      else if (u == "g") Console.WriteLine($"{(v * 3.7854):F4} l");
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

  cout << fixed << setprecision(4);
  int t; cin >> t;
  while (t--) {
    double v; string u; cin >> v >> u;

    if (u == "kg") cout << v * 2.2046 << " lb\n";
    else if (u == "lb") cout << v * 0.4536 << " kg\n";
    else if (u == "l") cout << v * 0.2642 << " g\n";
    else if (u == "g") cout << v * 3.7854 << " l\n";
  }

  return 0;
}
```
