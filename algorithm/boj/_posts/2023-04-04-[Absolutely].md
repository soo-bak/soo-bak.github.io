---
layout: single
title: "[백준 26500] Absolutely (C#, C++) - soo:bak"
date: "2023-04-04 18:58:00 +0900"
---

## 문제 링크
  [26500번 - Absolutely](https://www.acmicpc.net/problem/26500)

## 설명
간단한 수학 문제입니다. <br>

입력으로 주어지는 두 값 사이의 거리를 계산하여, 한 자리 정밀도로 반올림하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (var i = 0; i < n; i++) {
        var input = Console.ReadLine()?.Split();

        var a = double.Parse(input![0]);
        var b = double.Parse(input![1]);

        var absDist = Math.Abs(a - b);

        Console.WriteLine("{0:F1}", absDist);
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

  for (int i = 0; i < n; i++) {
    double a, b; cin >> a >> b;

    double absDist = abs(a - b);

    cout.setf(ios::fixed); cout.precision(1);
    cout << absDist << "\n";
  }

  return 0;
}
  ```
