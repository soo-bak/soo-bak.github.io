---
layout: single
title: "[백준 21312] 홀짝 칵테일 (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 세 수 중 홀수를 우선 곱하고, 없으면 전부 곱하는 방식으로 가장 맛있는 칵테일 맛을 구하는 백준 21312번 홀짝 칵테일 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[21312번 - 홀짝 칵테일](https://www.acmicpc.net/problem/21312)

## 설명
세 음료 번호 중 선택하여 가장 맛있는 칵테일을 만드는 문제입니다.

<br>

## 접근법
문제의 규칙에 따르면 홀수 결과는 값에 관계없이 짝수 결과보다 항상 맛있습니다.

홀수가 하나라도 있으면 모든 홀수를 곱한 값이 최적입니다.

홀수가 없으면 세 수를 모두 곱한 값이 최대가 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
    var prodOdd = 1; var cntOdd = 0;
    foreach (var x in line) {
      if (x % 2 != 0) {
        cntOdd++;
        prodOdd *= x;
      }
    }
    var ans = (cntOdd > 0) ? prodOdd : line[0] * line[1] * line[2];
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

  int a, b, c;
  if (!(cin >> a >> b >> c)) return 0;
  int prodOdd = 1, cntOdd = 0;
  int arr[3] = {a, b, c};
  for (int x : arr) {
    if (x % 2) {
      cntOdd++;
      prodOdd *= x;
    }
  }
  int ans = (cntOdd > 0) ? prodOdd : a * b * c;
  cout << ans << "\n";

  return 0;
}
```
