---
layout: single
title: "[백준 10797] 10부제 (C#, C++) - soo:bak"
date: "2025-04-14 20:34:12 +0900"
description: 차량 번호 끝자리와 날짜 숫자를 비교하여 통과 차량 수를 계산하는 백준 10797번 10부제 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10797
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 10797, 백준 10797번, BOJ 10797, trafficRestriction, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10797번 - 10부제](https://www.acmicpc.net/problem/10797)

## 설명
**차량 번호의 끝자리를 보고 10부제 제한일에 해당하는 차량이 몇 대인지**를 세는 간단한 구현 문제입니다.

---

## 접근법
- 입력으로 오늘의 날짜 끝자리 숫자 `D`가 주어집니다.
- 이후 `5`대의 차량 번호의 `끝자리 숫자`가 주어집니다.
- 각 차량 번호의 끝자리가 `D`와 같은지 비교하며 카운트합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int d = int.Parse(Console.ReadLine()!);
      var input = Console.ReadLine()!.Split();

      int cnt = 0;
      foreach (var car in input)
        if (int.Parse(car) == d) cnt++;

      Console.WriteLine(cnt);
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int digitDay; cin >> digitDay;

  int cnt = 0;
  for (int i = 0; i < 5; i++) {
    int input; cin >> input;
    if (digitDay == input) cnt++;
  }

  cout << cnt << "\n";

  return 0;
}
```
