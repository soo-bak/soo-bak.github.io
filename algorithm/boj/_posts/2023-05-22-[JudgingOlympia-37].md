---
layout: single
title: "[백준 4909] Judging Olympia (C#, C++) - soo:bak"
date: "2023-05-22 15:23:00 +0900"
---

## 문제 링크
  [4909번 - Judging Olympia](https://www.acmicpc.net/problem/4909)

## 설명
입력으로 `6` 가지 측면에 대한 등급이 주어질 때, 최종 평점을 게산하는 문제입니다. <br>

최종 평점은 가장 높은 점수와 가장 낮은 점수를 제외한, 나머지 점수들의 평균으로 계산됩니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      while (true) {
        var grades = Console.ReadLine()!.Split(' ').Select(int.Parse).ToList();

        if (grades.All(grade => grade == 0)) break ;

        grades.Sort();

        double sum = 0.0;
        for (int i = 1; i < 5; i++)
          sum += grades[i];

        var average = sum / 4.0;
        Console.WriteLine(average);
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

  vector<int> grades(6);

  while (true) {
    for (int i = 0; i < 6; i++)
      cin >> grades[i];

    if (all_of(grades.begin(), grades.end(), [](int grade) { return grade == 0; }))
      break ;

    sort(grades.begin(), grades.end());

    double sum = 0.0;
    for (int i = 1; i < 5; i++)
      sum += grades[i];

    double average = sum / 4.0;
    cout << average << "\n";
  }

  return 0;
}
  ```
