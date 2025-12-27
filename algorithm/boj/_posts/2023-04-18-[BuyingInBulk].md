---
layout: single
title: "[백준 26332] Buying in Bulk (C#, C++) - soo:bak"
date: "2023-04-18 17:29:00 +0900"
description: 수학과 사칙연산 주제로 하는 백준 26332번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 26332
  - C#
  - C++
  - 알고리즘
keywords: "백준 26332, 백준 26332번, BOJ 26332, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [26332번 - Buying in Bulk](https://www.acmicpc.net/problem/26332)

## 설명
간단한 사칙연산 문제입니다. <br>

문제의 목표는 `고객이 구매한 품목의 수` 와 `품목 당 가격` 이 주어졌을 때, <br>

품목에 수에 따른 할인이 적용된 최종 가격을 계산하는 것입니다. <br>

문제의 조건에 따르면, 품목의 수가 2 이상인 경우에만 품목 당 $2 의 할인이 적용되므로, <br>

`할인되는 금액` = `2` * (`품목의 수` - `1`) 입니다. <br>

할인 후 최종 금액을 계산하여 문제에서 주어진 출력 형식에 맞추어 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 0; i < n; i++) {
        var input = Console.ReadLine()?.Split();
        var c = int.Parse(input![0]);
        var p = int.Parse(input![1]);

        var beforeDiscount = c * p;
        var discount = 2 * (c - 1);
        var afterDiscount = beforeDiscount - discount;

        Console.WriteLine($"{c} {p}");
        Console.WriteLine(afterDiscount);
      }

    }
  }
}
  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  for (int i = 0; i < n; i++) {
    int c, p; cin >> c >> p;

    int beforeDiscount = c * p;
    int discount = 2 * (c - 1);
    int afterDiscount = beforeDiscount - discount;

    cout << c << " " << p << "\n";
    cout << afterDiscount << "\n";
  }

  return 0;
}
  ```
