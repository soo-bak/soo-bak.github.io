---
layout: single
title: "[백준 3053] 택시 기하학 (C#, C++) - soo:bak"
date: "2023-05-28 16:20:00 +0900"
description: 수학과 택시 기하학, 유클리드 기하학을 주제로 하는 백준 3053번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [3053번 - 택시 기하학](https://www.acmicpc.net/problem/3053)

## 설명
`유클리드 기하학` 과 `택시 기하학` 에서의 원의 넓이를 구하는 문제입니다. <br>

`유클리드 기하학` 에서 원의 넓이는 <b>π * r<sup>2</sup></b> 입니다. 여기서, <b>π</b> 는 원주율이고, <b>r</b> 은 반지름 입니다. <br>

`택시 기하학` 에서 원은 마름로 형태를 띄며, `택시 기하학` 에서 <b>마름모의 대각선 길이</b>는 `유클리드 기하학` 에서의 <b>원의 지름</b>과 같습니다. <br>

따라서, `택시 기하학` 에서의 원의 넓이는, 두 대각선의 길이가 <b>2 * r</b> 인 마름모의 넓이, 즉, <b>2 * r<sup>2</sup></b> 과 같습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var r = double.Parse(Console.ReadLine()!);

      var euclideanArea = Math.PI * r * r;
      var taxicapArea = 2 * r * r;

      Console.WriteLine($"{euclideanArea:F4}");
      Console.WriteLine($"{taxicapArea:F4}");

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

  double r; cin >> r;

  double euclideanArea = M_PI * r * r;
  double taxicapArea = 2 * r * r;

  cout.setf(ios::fixed); cout.precision(4);
  cout << euclideanArea << "\n";
  cout << taxicapArea << "\n";

  return 0;
}
  ```
