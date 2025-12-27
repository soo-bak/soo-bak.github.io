---
layout: single
title: "[백준 24803] Provinces and Gold (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 24803번 C#, C++ 풀이 - 보유한 동전 가치로 구매 가능한 최고의 승점 카드와 보물 카드를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 24803
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
  - 케이스분류
keywords: "백준 24803, 백준 24803번, BOJ 24803, ProvincesAndGold, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24803번 - Provinces and Gold](https://www.acmicpc.net/problem/24803)

## 설명
손에 든 Gold, Silver, Copper의 구매력으로 살 수 있는 최고 승점 카드와 최고 보물 카드를 출력하는 문제입니다.

<br>

## 접근법
총 구매력을 계산할 때 Gold는 3, Silver는 2, Copper는 1로 계산합니다. 구매력에 따라 살 수 있는 최고 승점 카드와 최고 보물 카드를 결정합니다.

승점 카드를 살 수 있으면 두 카드를 함께 출력하고, 아니면 보물 카드만 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var g = int.Parse(parts[0]);
    var s = int.Parse(parts[1]);
    var c = int.Parse(parts[2]);

    var power = g * 3 + s * 2 + c;

    var victory = "";
    if (power >= 8) victory = "Province";
    else if (power >= 5) victory = "Duchy";
    else if (power >= 2) victory = "Estate";

    var treasure = "";
    if (power >= 6) treasure = "Gold";
    else if (power >= 3) treasure = "Silver";
    else treasure = "Copper";

    if (victory != "") Console.WriteLine($"{victory} or {treasure}");
    else Console.WriteLine(treasure);
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

  int g, s, c; cin >> g >> s >> c;
  int power = g * 3 + s * 2 + c;

  string victory;
  if (power >= 8) victory = "Province";
  else if (power >= 5) victory = "Duchy";
  else if (power >= 2) victory = "Estate";

  string treasure;
  if (power >= 6) treasure = "Gold";
  else if (power >= 3) treasure = "Silver";
  else treasure = "Copper";

  if (!victory.empty()) cout << victory << " or " << treasure << "\n";
  else cout << treasure << "\n";

  return 0;
}
```
