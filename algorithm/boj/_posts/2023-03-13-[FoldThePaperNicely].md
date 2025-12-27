---
layout: single
title: "[백준 26340] Fold the Paper Nicely (C#, C++) - soo:bak"
date: "2023-03-14 16:09:00 +0900"
description: 수학과 구현에 대한 백준 26340번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 26340
  - C#
  - C++
  - 알고리즘
keywords: "백준 26340, 백준 26340번, BOJ 26340, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [26340번 - Fold the Paper Nicely](https://www.acmicpc.net/problem/26340)

## 설명
  간단한 수학과 구현 관련 문제입니다. <br>

  문제의 목표는 Orooji 박사가 달력을 반복해서 접었을 때, 최종적인 달력의 가로/세로 길이를 구하는 것입니다.<br>

  문제에서 주어진 Orooji 박사의 달력 접기 방법은 다음과 같습니다.
  1. 가로/세로 중 길이가 더 긴쪽을 반으로 접는다.
  2. 입력으로 주어지는 '접는 횟수' 만큼 반복해서 접는다.

  해당 정보를 이용하여 주어진 입력에 따라 계산된 `달력의 최종적인 가로/세로 길이` 를 출력 조건에 맞추어 출력합니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var dataSetNum = int.Parse(Console.ReadLine()!);
      for (int i = 0; i < dataSetNum; i++) {
        var input = Console.ReadLine()?.Split();

        var rectSide_1 = int.Parse(input![0]);
        var rectSide_2 = int.Parse(input![1]);
        var foldingNum = int.Parse(input![2]);

        Console.WriteLine($"Data set: {rectSide_1} {rectSide_2} {foldingNum}");

        for (int j = 0; j < foldingNum; j++) {
          if (rectSide_1 > rectSide_2) rectSide_1 /= 2;
          else rectSide_2 /= 2;
        }

        Console.WriteLine($"{Math.Max(rectSide_1, rectSide_2)} {Math.Min(rectSide_1, rectSide_2)}");
        if (i != dataSetNum - 1) Console.Write("\n");
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

  int dataSetNum; cin >> dataSetNum;

  for (int i = 0; i < dataSetNum; i++) {
    int rectSide_1, rectSide_2, foldingNum;
    cin >> rectSide_1 >> rectSide_2 >> foldingNum;

    cout << "Data set: " << rectSide_1 << " " << rectSide_2 << " " << foldingNum << "\n";

    for (int j = 0; j < foldingNum; j++) {
      if (rectSide_1 > rectSide_2) rectSide_1 /= 2;
      else rectSide_2 /= 2;
    }

    cout << max(rectSide_1, rectSide_2) << " " << min(rectSide_1, rectSide_2) << "\n";
    if (i != dataSetNum - 1) cout << "\n";
  }

  return 0;
}
  ```
