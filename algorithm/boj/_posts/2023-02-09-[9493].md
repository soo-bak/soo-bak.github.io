---
layout: single
title: "[백준 9493] 길면 기차, 기차는 빨라, 빠른 것은 비행기 (C#, C++) - soo:bak"
date: "2023-02-09 14:39:00 +0900"
---

## 문제 링크
  [9493번 - 길면 기차, 기차는 빨라, 빠른 것은 비행기](https://www.acmicpc.net/problem/9493)

## 설명
  사칙연산과 입출력에 관한 문제입니다.<br>

  문제에서 주어진 조건에 따라서,<br>
  기차의 속도, 비행기의 속도로 동일 거리를 이동하는 데에 소요되는 시간을 각각 계산합니다.<br>

  이후, 두 시간의 차이를 문제의 조건에 맞는 형식에 맞추어 출력합니다.
  <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    readonly static int HToS = 3600, MToS = 60;

    static void Main(string[] args) {

      while (true) {
        string[]? input = Console.ReadLine()?.Split();
        int.TryParse(input?[0], out int dist);
        int.TryParse(input?[1], out int veloTrain);
        int.TryParse(input?[2], out int veloPlane);

        if (dist == 0 && veloTrain == 0 && veloPlane == 0) break ;

        double timeTrain = dist / (double)veloTrain * HToS,
               timePlane = dist / (double)veloPlane * HToS;

        int delta = (int)Math.Round(Math.Abs(timeTrain - timePlane));

        Console.WriteLine("{0}:{1:00}:{2:00}", delta / HToS, delta % HToS / MToS, delta % HToS % MToS);
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

  const int HToS = 3600, MToS = 60;

  while (true) {
    int dist, veloTrain, veloPlane; cin >> dist >> veloTrain >> veloPlane;

    if (dist == 0 && veloTrain == 0 && veloPlane == 0) break ;

    double timeTrain = dist / (double)veloTrain * HToS,
            timePlane = dist / (double)veloPlane * HToS;

    int delta = round(abs(timeTrain - timePlane));

    cout << delta / HToS << ":" <<
      setw(2) << setfill('0') << delta % HToS / MToS << ":" <<
      setw(2) << setfill('0') << delta % HToS % MToS << "\n";
  }

  return 0;
}
  ```
