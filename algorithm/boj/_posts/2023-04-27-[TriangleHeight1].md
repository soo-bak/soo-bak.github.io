---
layout: single
title: "[백준 26592] Triangle Height (C#, C++) - soo:bak"
date: "2023-04-27 15:53:00 +0900"
---

## 문제 링크
  [26592번 - Triangle Height](https://www.acmicpc.net/problem/26592)

## 설명
간단한 사칙연산 문제입니다. <br>

문제의 목표는 삼각형의 면적과 밑변의 길이가 주어졌을 때, 삼각형의 높이를 구하는 것입니다. <br>

삼각형의 면적을 `a` , 밑변의 길이를 `b`, 높이를 `h` 라고 할 때, 다음과 같은 관계가 성립합니다. <br>

`a` = (`h` * `b`) / `2` <br>

위 관계를 이용하여, 각각의 입력에 대하여 삼각형의 높이를 계산한 후 출력합니다. <br>

소수점 이하 두 자리까지 출력해야 하는 출력 조건에 주의합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int t = 0; t < n; t++) {
        var input = Console.ReadLine()!.Split(' ');
        var a = double.Parse(input![0]);
        var b = double.Parse(input![1]);

        double height = (2 * a) / b;
        Console.WriteLine($"The height of the triangle is {height:F2} units");
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

  cout.setf(ios::fixed); cout.precision(2);
  for (int t = 0; t < n; t++) {
    double a, b; cin >> a >> b;

    double height = (2 * a) / b;
    cout << "The height of the triangle is " << height << " units\n";
  }

  return 0;
}
  ```
