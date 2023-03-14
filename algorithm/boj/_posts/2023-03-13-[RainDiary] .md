---
layout: single
title: "[백준 27182] Rain Diary (C#, C++) - soo:bak"
date: "2023-03-14 16:07:00 +0900"
---

## 문제 링크
  [27182번 - Rain Diary](https://www.acmicpc.net/problem/27182)

## 설명
  간단한 수학 문제입니다. <br>

  문제의 목표는 `지난 주 일요일의 날짜` 를 구하는 것입니다.<br>

  입력으로 주어지는 두 정수는 각각 `현재 날짜`, `2주 전의 날짜` 입니다. <br>

  따라서, 단순히 `현재 날짜 - 7` 을 통해 지난 주 일요일의 날짜를 구할 수 있을 것이라 생각할 수 있지만, <br>

  문제의 조건 중에서 달마다 마지막 날짜의 범위가 `28일 ~ 31일` 로 다를 수 있다는 조건이 있습니다.<br>

  따라서, `2주 전의 날짜` 와 `현재의 날짜` 의 관계를 이용하여 `이전 달의 마지막 날짜` 를 계산해야 합니다. <br>

  최종적으로,`현재의 날짜 - 7` 값과 위에서 계산한 `이전 달의 마지막 날짜` 를 이용하여 지난 주 일요일의 날짜를 계산하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {
      var input = Console.ReadLine()?.Split();
      var currentDay = int.Parse(input![0]);
      var lastRecordedDay = int.Parse(input![1]);

      var daysInMonth = 0;
      switch (lastRecordedDay - currentDay + 14) {
        case 28:
          daysInMonth = 28;
          break;
        case 29:
          daysInMonth = 29;
          break;
        case 30:
          daysInMonth = 30;
          break;
        case 31:
          daysInMonth = 31;
          break;
      }

      int ans = currentDay - 7;
      if (ans <= 0) ans += daysInMonth;

      Console.WriteLine(ans);
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
    int currentDay, lastlRecordedDay; cin >> currentDay >> lastlRecordedDay;

    int daysInMonth = 0;
    switch (lastlRecordedDay - currentDay + 14) {
      case 28:
        daysInMonth = 28; break ;
      case 29:
        daysInMonth = 29; break ;
      case 30:
        daysInMonth = 30; break ;
      case 31:
        daysInMonth = 31; break ;
    }

    int ans = currentDay - 7;
    if (ans <= 0) ans += daysInMonth;

    cout << ans << "\n";

    return 0;
}
  ```
