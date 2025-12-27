---
layout: single
title: "[백준 6778] Which Alien? (C#, C++) - soo:bak"
date: "2025-11-21 23:47:00 +0900"
description: 더듬이·눈 개수 조건을 만족하는 외계종을 판별하는 백준 6778번 Which Alien? 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 6778
  - C#
  - C++
  - 알고리즘
keywords: "백준 6778, 백준 6778번, BOJ 6778, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6778번 - Which Alien?](https://www.acmicpc.net/problem/6778)

## 설명

외계 생명체의 더듬이 개수와 눈 개수가 주어집니다.<br>

세 종류의 외계종 중 관측된 특징과 일치하는 종의 이름을 모두 출력하는 문제입니다.

여러 종이 조건을 만족할 수 있습니다.<br>

<br>

## 접근법

세 외계종의 조건을 확인합니다.

`TroyMartian`은 더듬이 `3`개 이상, 눈 `4`개 이하입니다.

`VladSaturnian`은 더듬이 `6`개 이하, 눈 `2`개 이상입니다.

`GraemeMercurian`은 더듬이 `2`개 이하, 눈 `3`개 이하입니다.<br>

<br>
입력받은 더듬이와 눈 개수를 각 외계종의 조건과 비교하여, 조건을 만족하는 이름을 순서대로 출력합니다.

여러 외계종이 동시에 조건을 만족하면 모두 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var antenna = int.Parse(Console.ReadLine()!);
      var eyes = int.Parse(Console.ReadLine()!);

      if (antenna >= 3 && eyes <= 4)
        Console.WriteLine("TroyMartian");
      if (antenna <= 6 && eyes >= 2)
        Console.WriteLine("VladSaturnian");
      if (antenna <= 2 && eyes <= 3)
        Console.WriteLine("GraemeMercurian");
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

  int antenna, eyes; cin >> antenna >> eyes;

  if (antenna >= 3 && eyes <= 4)
    cout << "TroyMartian\n";
  if (antenna <= 6 && eyes >= 2)
    cout << "VladSaturnian\n";
  if (antenna <= 2 && eyes <= 3)
    cout << "GraemeMercurian\n";

  return 0;
}
```

