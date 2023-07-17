---
layout: single
title: "[백준 28249] Chili Peppers (C#, C++) - soo:bak"
date: "2023-07-17 21:15:00 +0900"
description: 문자열, 파싱, 맵, 자료구조, 구현 등을 주제로 하는 백준 28249번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [28249번 - Chili Peppers](https://www.acmicpc.net/problem/28249)

## 설명
문제에서 주어진 `SHU, (Scoville Heat Units)` 지수 표를 바탕으로, <br>

입력으로 주어지는 매운 고추들의 `SHU` 지수 총합을 구하는 문제입니다.<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      Dictionary<string, int> m = new Dictionary<string, int> {
        {"Poblano", 1500},
        {"Mirasol", 6000},
        {"Serrano", 15500},
        {"Cayenne", 40000},
        {"Thai", 75000},
        {"Habanero", 125000}
      };

      var n = int.Parse(Console.ReadLine()!);

      int totalSHU = 0;
      for (int i = 0; i < n; i++) {
        string pepper = Console.ReadLine()!;
        totalSHU += m[pepper];
      }

      Console.WriteLine(totalSHU);

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

  map<string, int> m = {
    {"Poblano", 1500},
    {"Mirasol", 6000},
    {"Serrano", 15500},
    {"Cayenne", 40000},
    {"Thai", 75000},
    {"Habanero", 125000}
  };

  int n; cin >> n;

  int totlaSHU = 0;
  for (int i = 0; i < n; i++) {
    string pepper; cin >> pepper;
    totlaSHU += m[pepper];
  }

  cout << totlaSHU << "\n";

  return 0;
}
  ```
