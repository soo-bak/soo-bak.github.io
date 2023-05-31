---
layout: single
title: "[백준 1110] 더하기 사이클 (C#, C++) - soo:bak"
date: "2023-05-17 15:08:00 +0900"
description: 수학과 시뮬레이션, 규칙 발견을 주제로 하는 백준 1110번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [1110번 - 더하기 사이클](https://www.acmicpc.net/problem/1110)

## 설명
문제에서 주어진 규칙에 따라서 새로운 숫자를 만드는 과정을 진행하고,<br>

만들어진 새로운 숫자가 원래의 숫자가 되기까지 과정이 몇 번 반복되는지 계산하는 문제입니다.<br>

문제에서 주어진 규칙을 수학적으로 변환하는 부분이 핵심인 것 같습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      if (n == 0) Console.WriteLine(1);
      else {
        int lenCycle = 0;
        var num = n;
        while (true) {
          var sumDigits = num / 10 + num % 10;
          num = (num % 10) * 10 + sumDigits % 10;
          lenCycle++;

          if (num == n) break ;
        }

        Console.WriteLine(lenCycle);
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

  if (n == 0) cout << "1\n";
  else {
    int lenCycle = 0, num = n;
    while (true) {
      int sumDigits = num / 10 + num % 10;
      num = (num % 10) * 10 + sumDigits % 10;
      lenCycle++;

      if (num == n) break ;
    }

    cout << lenCycle << "\n";
  }

  return 0;
}
  ```
