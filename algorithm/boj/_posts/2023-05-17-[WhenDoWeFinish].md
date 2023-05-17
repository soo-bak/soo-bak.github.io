---
layout: single
title: "[백준 5074] When Do We Finish? (C#, C++) - soo:bak"
date: "2023-05-17 12:27:00 +0900"
---

## 문제 링크
  [5074번 - When Do We Finish?](https://www.acmicpc.net/problem/5074)

## 설명
입력으로 주어지는 이벤트의 시작 시간과 지속 시간을 바탕으로, 이벤트가 언제 종료되는지를 계산하는 문제입니다. <br>

또한 계산된 종료 시간이 다음 날인지 아닌지에 대해서도 판별해야 합니다. <br>

계산은 쉽지만 문자열의 출력 형식에 대한 지식을 확인할 수 있다는 점에서 좋은 문제 같습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      while (true) {
        var input = Console.ReadLine()!.Split(' ');

        var startTime = input[0];
        var durTime = input[1];

        if (startTime == "00:00" && durTime == "00:00") break ;

        var startHour = int.Parse(startTime.Substring(0, 2));
        var startMin = int.Parse(startTime.Substring(3, 2));
        var durHour = int.Parse(durTime.Substring(0, 2));
        var durMin = int.Parse(durTime.Substring(3, 2));

        var endHour = startHour + durHour;
        var endMin = startMin + durMin;

        int extraDay = 0;
        if (endMin >= 60) {
          endHour++;
          endMin -= 60;
        }
        if (endHour >= 24) {
          extraDay = endHour / 24;
          endHour %= 24;
        }

        Console.Write($"{endHour:D2}:{endMin:D2}");

        if (extraDay > 0) Console.Write($" +{extraDay}");

        Console.WriteLine();
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

  while (true) {
    string startTime, durTime; cin >> startTime >> durTime;

    if (startTime == "00:00" && durTime == "00:00") break ;

    int startHour = stoi(startTime.substr(0, 2)),
        startMin = stoi(startTime.substr(3, 2)),
        durHour = stoi(durTime.substr(0, 2)),
        durMin = stoi(durTime.substr(3, 2));

    int endHour = startHour + durHour,
        endMin = startMin + durMin;

    int extraDay = 0;
    if (endMin >= 60) {
      endHour++;
      endMin -= 60;
    }
    if (endHour >= 24) {
      extraDay = endHour / 24;
      endHour %= 24;
    }

    cout << setw(2) << setfill('0') << endHour << ":";
    cout << setw(2) << setfill('0') << endMin;

    if (extraDay > 0) cout << " +" << extraDay;

    cout << "\n";
  }

  return 0;
}
  ```
