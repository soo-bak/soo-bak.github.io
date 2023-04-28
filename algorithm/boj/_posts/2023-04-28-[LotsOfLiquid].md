---
layout: single
title: "[백준 25991] Lots of Liquid (C#, C++) - soo:bak"
date: "2023-04-28 18:36:00 +0900"
---

## 문제 링크
  [25991번 - Lots of Liquid](https://www.acmicpc.net/problem/25991)

## 설명
간단한 수학 문제입니다. <br>

문제의 목표는 분리되어 있는 용기들에 담겨진 <b>BAPC 액체</b>를 한 번에 담을 수 있는 새로운 용기의 한 변의 길이를 구하는 것입니다.<br>

`n` 개의 용기들의 모든 부피를 합산한 후, 그 값을 세제곱근 하여 새로운 용기의 한 변의 길이를 구할 수 있습니다. <br>

최종적으로 계산된 길이를 출력 조건에 맞추어 출력합니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      double volume = 0.0;

      var input = Console.ReadLine()!.Split();
      for (int i = 0; i < n; i++) {
        var len = double.Parse(input![i]);
        volume += Math.Pow(len, 3);
      }

      double ans = Math.Pow(volume, 1.0 / 3);
      Console.WriteLine($"{ans:F6}");

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

  double volume = 0.0;

  for (int i = 0; i < n; i++) {
    double len; cin >> len;
    volume += pow(len, 3);
  }

  double ans = pow(volume, 1.0 / 3);
  cout.setf(ios::fixed); cout.precision(6);
  cout << ans << "\n";

  return 0;
}
  ```
