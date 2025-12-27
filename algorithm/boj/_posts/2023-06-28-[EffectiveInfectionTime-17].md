---
layout: single
title: "[백준 9428] Effective Infection Time (C#, C++) - soo:bak"
date: "2023-06-28 14:03:00 +0900"
description: 수학, 구현, 사칙연산 등을 주제로 하는 백준 9428번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9428
  - C#
  - C++
  - 알고리즘
keywords: "백준 9428, 백준 9428번, BOJ 9428, EffectiveInfectionTime, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [9428번 - Effective Infection Time](https://www.acmicpc.net/problem/9428)

## 설명
A.Z(After Zombie), 즉 좀비 사태 이후 격리 구역의 EIT(Effective Infection Time)을 계산하는 문제입니다. <br>

문제에서 설명하는 EIT 의 계산 규칙은 다음과 같습니다.<br>
- 감염 날짜(Infection date) 와 증상 발생 날짜(Strike date) 의 두 가지 요인에 의해 계산 <br>
- 각 월은 해당 월의 마지막 날이 지난 후에만 EIT 의 일부로 계산<br>
- 감염의 첫 해는 (`1` / `2`)EIT 로 계산<br>
  - 다만, 아직 해당 연도가 끝나지 않았다면, 각 월은 (`1` / `2`)EIT 의 일부로만 계산<br>
  - 예시
    - 감염이 첫 해의 `1`월에 발생하였다면, (`1` / `2`)EIT 가 `12`개월 동안 분배되어 (`0.0417`EIT / 월)<br>
    - 감염이 첫 해의 `3`월에 발생하였다면, (`1` / `2`)EIT 가 `10`개월 동안 분배되어 (`0.0500`EIT / 월)<br>
- 연도가 끝났다면, 감염 월에 상관없이 무조건 그 해의 EIT 는 (`1` / `2`) 가 됨<br>
- 이후의 모든 해는 `1`EIT 로 계산되며, 각 달의 EIT 는 (`0.0833`EIT / 월) 으로 분배 됨<br>

입력으로 감염 날짜와 감염 연도, 증상 발생 날짜와 증상 발생 연도가 주어졌을 때, <br>

위 EIT 계산 규칙에 맞추어 EIT 를 계산하여 출력합니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      const int MONTH = 0;
      const int YEAR = 1;

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 0; i < n; i++) {
        var infection = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();
        var strike = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();

        double eit = 0.0;
        if (infection[YEAR] == strike[YEAR])
          eit += 0.5 * (strike[MONTH] - infection[MONTH]) / (12.0 - infection[MONTH] + 1);
        else
          eit += 0.5 + (strike[YEAR] - infection[YEAR] - 1) + (strike[MONTH] - 1) / 12.0;

        Console.WriteLine($"{eit:F4}");
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
    int iMonth, iYear, sMonth, sYear;
    cin >> iMonth >> iYear >> sMonth >> sYear;

    double eit = 0.0;
    if (iYear == sYear)
      eit += 0.5 * (sMonth - iMonth) / (12.0 - iMonth + 1);
    else
      eit += 0.5 + (sYear - iYear - 1) + (sMonth - 1) / 12.0;

    cout.setf(ios::fixed); cout.precision(4);
    cout << eit << "\n";
  }

  return 0;
}
  ```
