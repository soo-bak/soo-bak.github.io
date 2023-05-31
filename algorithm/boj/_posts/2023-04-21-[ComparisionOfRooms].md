---
layout: single
title: "[백준 27267] Сравнение комнат (C#, C++) - soo:bak"
date: "2023-04-21 15:33:00 +0900"
description: 수학과 사칙연산을 주제로 하는 백준 27267번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [27267번 - Сравнение комнат](https://www.acmicpc.net/problem/27267)

## 설명
간단한 사칙연산 문제입니다. <br>

문제의 목표는 두 개의 직사각형 모양 방들의 크기를 비교하고, 누구의 방이 더 큰지를 결정하는 것입니다.<br>

첫 번째 방의 크기는 `a` * `b` 이고, 두 번째 방의 크기는 `c` * `d` 입니다. <br>

만약, 첫 번째 방이 더 크다면 `M` 을, 두 번째 방이 더 큰 경우 `P` 를, 두 방의 크기가 같은 경우 `E` 를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()?.Split(' ');

      var a = int.Parse(input![0]);
      var b = int.Parse(input![1]);
      var c = int.Parse(input![2]);
      var d = int.Parse(input![3]);

      var area1 = a * b;
      var area2 = c * d;

      if (area1 > area2) Console.WriteLine("M");
      else if (area1 < area2) Console.WriteLine("P");
      else Console.WriteLine("E");

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

  int a, b, c, d; cin >> a >> b >> c >> d;

  int area1 = a * b, area2 = c * d;

  if (area1 > area2) cout << "M\n";
  else if (area1 < area2) cout << "P\n";
  else cout << "E\n";

  return 0;
}
  ```
