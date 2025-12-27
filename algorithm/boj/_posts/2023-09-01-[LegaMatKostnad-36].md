---
layout: single
title: "[백준 26933] Receptet (C#, C++) - soo:bak"
date: "2023-09-01 23:13:00 +0900"
description: 수학, 구현 등을 주제로 하는 백준 26933번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 26933
  - C#
  - C++
  - 알고리즘
keywords: "백준 26933, 백준 26933번, BOJ 26933, LegaMatKostnad, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [26933번 - Receptet](https://www.acmicpc.net/problem/26933)

## 설명
재료의 갯수 `n`, 각 재료에 대해 현재 가지고 있는 양 `h`, 필요한 양 `b`, 그리고 재료 `1` 개를 사기 위해 필요한 비용 `k` 가 주어질 때,<br>
<br>
요리를 하기 위해 필요한 재료들의 총 비용을 계산하는 문제입니다. <br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      int totalCost = 0;
      for (int i = 0; i < n; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var h = int.Parse(input[0]);
        var b = int.Parse(input[1]);
        var k = int.Parse(input[2]);

        if (h < b) totalCost += (b - h) * k;
      }

      Console.WriteLine(totalCost);

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

  int totalCost = 0;
  for (int i = 0; i < n; i++) {
    int h, b, k; cin >> h >> b >> k;

    if (h < b) totalCost += (b - h) * k;
  }

  cout << totalCost << "\n";

  return 0;
}
  ```
