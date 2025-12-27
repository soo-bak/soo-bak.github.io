---
layout: single
title: "[백준 5565] 영수증 (C#, C++) - soo:bak"
date: "2025-04-14 20:57:52 +0900"
description: 10권 중 9권의 금액만 주어졌을 때 남은 1권의 가격을 추론하는 백준 5565번 영수증 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 5565
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 5565, 백준 5565번, BOJ 5565, receiptChecker, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5565번 - 영수증](https://www.acmicpc.net/problem/5565)

## 설명
책 10권의 **총 가격 합계**과 **10권 중 9권의 책 가격**이 주어졌을 때,  <br>
마지막 `1`개의 책 가격을 찾아 출력하는 간단한 산술 문제입니다.

---

## 접근법
- 입력 첫 줄에서 총 금액 을 입력받습니다.
- 이후 `9`개의 정수를 입력받아, 총 금액에서 하나씩 차감해 나갑니다.
- 위 과정이 끝난 후 남은 값이 **남은 책의 가격**입니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int total = int.Parse(Console.ReadLine()!);
      for (int i = 0; i < 9; i++) {
        int cost = int.Parse(Console.ReadLine()!);
        total -= cost;
      }
      Console.WriteLine(total);
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

  int total; cin >> total;
  for (int i = 0; i < 9; i++) {
    int cost; cin >> cost;
    total -= cost;
  }
  cout << total << "\n";

  return 0;
}
```
