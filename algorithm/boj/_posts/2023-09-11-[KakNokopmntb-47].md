---
layout: single
title: "[백준 28840] Как покормить дракона (C#, C++) - soo:bak"
date: "2023-09-11 04:43:00 +0900"
description: 수학, 시간 계산, 문자열, 구현 등을 주제로 하는 백준 28840번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [28840번 - Как покормить дракона](https://www.acmicpc.net/problem/28840)

## 설명
문제의 목표는 두 시간(오늘의 먹이 주는 시간, 내일의 먹이 주는 시간)이 주어졌을 때,<br>
<br>
두 시간 사이에 얼마나 시간이 지났는지 계산하는 것입니다. <br>
<br>
`"HH:MM"` 형식으로 주어지는 각 시간을 `60` * `HH` + `MM` 형식으로 변환한 후, <br>
<br>
두 시간을 분 단위로 뺄셈하여 시간 차이를 구합니다. <br>
<br>
오늘의 시간이 내일의 시간보다 큰 경우, 하루가 지난 것으로 가눚해야 함에 주의합니다.<br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var currentTime = Console.ReadLine()!;
      var nextTime = Console.ReadLine()!;

      var currHours = int.Parse(currentTime.Substring(0, 2));
      var currMinutes = int.Parse(currentTime.Substring(3, 2));
      var nextHours = int.Parse(nextTime.Substring(0, 2));
      var nextMinutes = int.Parse(nextTime.Substring(3, 2));

      var currTotalMinutes = 24 * 60 - (60 * currHours + currMinutes);
      var nextTotalMinutes = 60 * nextHours + nextMinutes;

      var total = currTotalMinutes + nextTotalMinutes;

      var hours = total / 60;
      var minutes = total % 60;

      Console.WriteLine($"{hours:D2}:{minutes:D2}");
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

  string currentTime, nextTime; cin >> currentTime >> nextTime;

  int currHours = stoi(currentTime.substr(0, 2));
  int currMinutes = stoi(currentTime.substr(3, 2));
  int nextHours = stoi(nextTime.substr(0, 2));
  int nextMinutes = stoi(nextTime.substr(3, 2));

  int currTotalMinutes = 24 * 60 - (60 * currHours + currMinutes);
  int nextTotalMinutes = 60 * nextHours + nextMinutes;

  int total = currTotalMinutes + nextTotalMinutes;

  int hours = total / 60;
  int minutes = total % 60;

  cout << setw(2) << setfill('0');
  cout << hours << ":";
  cout << setw(2) << setfill('0');
  cout << minutes << "\n";

  return 0;
}
  ```
