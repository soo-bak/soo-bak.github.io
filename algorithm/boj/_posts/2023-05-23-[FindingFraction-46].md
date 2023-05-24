---
layout: single
title: "[백준 1193] 분수찾기 (C#, C++) - soo:bak"
date: "2023-05-23 07:27:00 +0900"
---

## 문제 링크
  [1193번 - 분수찾기](https://www.acmicpc.net/problem/1193)

## 설명
분수의 순서가 지그재그 형태로 나타난다는 점을 바탕으로, `x` 번째 분수를 구하는 문제입니다. <br>

우선, `x` 번째 분수가 어느 대각선에 위치하는지를 찾아야 합니다. <br>

행과 열의 합이 동일한 대각선에서, 행이나 열의 값을 증가시키며 분수를 생성한다는 점을 활용하여 `x` 번쨰 분수가 위치하는 대각선을 계산할 수 있습니다. <br>

이후, 대각선의 번호가 짝수인 경우 분수의 순서는 위에서 아래로, 홀수인 경우 분수의 순서는 아래에서 위로 생성된다는 점을 활용하여 `x` 번째 분수의 위치를 계산합니다. <br>

<br>
대각선 번호가 짝수인 경우 위에서 아래로 분수를 생성하므로,<br>

`x` 번쨰 분수의 분자는 `대각선 번호` - (`해당 대각선까지 들어갈 수 있는 총 분수의 개수` - `x`) 가 됩니다. <br>

`x` 번쨰 분수의 분모는 `1` + (`해당 대각선까지 들어갈 수 있는 총 분수의 개수` - `x`) 가 됩니다. <br>

<br>
대각선 번호가 홀수의 경우에는 아래에서 위로 분수를 생성하므로, 분자와 분모의 계산식이 짝수의 경우와 반대입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var x = int.Parse(Console.ReadLine()!);

      int diagonal = 0, cntFractions = 0;
      while (cntFractions < x) {
        diagonal++;
        cntFractions += diagonal;
      }

      var diff = cntFractions - x;

      int numerator = 0, denominator = 0;
      if (diagonal % 2 == 0) {
        numerator = diagonal - diff;
        denominator = 1 + diff;
      } else {
        numerator = 1 + diff;
        denominator = diagonal - diff;
      }

      Console.WriteLine($"{numerator}/{denominator}");

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

  int x; cin >> x;

  int diagonal = 0, cntFractions = 0;
  while (cntFractions < x) {
    diagonal++;
    cntFractions += diagonal;
  }

  int diff = cntFractions - x;

  int numerator, denominator;
  if (diagonal % 2 == 0) {
    numerator = diagonal- diff;
    denominator = 1 + diff;
  } else {
    numerator = 1 + diff;
    denominator = diagonal - diff;
  }

  cout << numerator << "/" << denominator << "\n";

  return 0;
}
  ```
