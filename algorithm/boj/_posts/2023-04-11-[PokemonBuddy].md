---
layout: single
title: "[백준 18691] Pokemon Buddy (C#, C++) - soo:bak"
date: "2023-04-11 13:47:00 +0900"
description: 수학과 사칙연산을 주제로 하는 백준 18691번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [18691번 - Pokemon Buddy](https://www.acmicpc.net/problem/18691)

## 설명
간단한 사칙연산 문제입니다. <br>

문제의 조건에 따라서 포켓몬의 그룹 별로 사탕 하나를 획득할 수 있는 거리를 구한 후,<br>

진화를 위해 필요한 사탕 개수를 충족할 때 까지 걸어야 하는 거리를 구하여 출력합니다.<br>

<br>
문제의 조건에 처음에 가지고 있는 사탕의 개수가 진화를 위해 필요한 사탕의 개수보다 작다는 보장이 없으므로, <br>

해당 부분에 대한 예외처리에 주의합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var caseCnt = int.Parse(Console.ReadLine()!);

      for (var i = 0; i < caseCnt; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var group = int.Parse(input[0]);
        var initialCandies = int.Parse(input[1]);
        var evolveCandies = int.Parse(input[2]);

        var requiredCandies = evolveCandies - initialCandies;

        int requriedKm;
        if (group == 1) requriedKm = requiredCandies;
        else if (group == 2) requriedKm = 3 * requiredCandies;
        else requriedKm = 5 * requiredCandies;

        if (requriedKm <= 0) Console.WriteLine("0");
        else Console.WriteLine($"{requriedKm}");
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

  int caseCnt; cin >> caseCnt;

  for (int i = 0; i < caseCnt; i++) {
    int group, initialCandies, evolveCandies;
    cin >> group >> initialCandies >> evolveCandies;

    int requiredCandies = evolveCandies - initialCandies;

    int requriedKm;
    if (group == 1) requriedKm = requiredCandies;
    else if (group == 2) requriedKm = 3 * requiredCandies;
    else requriedKm = 5 * requiredCandies;

    if (requriedKm <= 0) cout << "0\n";
    else  cout << requriedKm << "\n";
  }

  return 0;
}
  ```
