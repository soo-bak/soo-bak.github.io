---
layout: single
title: "[백준 9724] Perfect Cube (C#, C++) - soo:bak"
date: "2023-08-27 21:07:00 +0900"
description: 수학, 구현, 기하 등을 주제로 하는 백준 9724번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9724
  - C#
  - C++
  - 알고리즘
  - 수학
keywords: "백준 9724, 백준 9724번, BOJ 9724, PerfectCube, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [9724번 - Perfect Cube](https://www.acmicpc.net/problem/9724)

## 설명
입력으로 주어진 범위 내에서 `완벽한 큐브` 를 찾는 문제입니다. <br>
<br>
문제의 설명에 따르면, `완벽한 큐브` 라면 그 큐브의 세제곱근 역시 정수일 것이라고 알려주므로, <br>
<br>
주어진 범위 내에서 세제곱근이 정수인 수를 찾아 출력하면 됩니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var t = int.Parse(Console.ReadLine()!);

      for (int i = 1; i <= t; i++) {
        var input = Console.ReadLine()!.Split();
        var a = int.Parse(input[0]);
        var b = int.Parse(input[1]);

        var start = (int)Math.Ceiling(Math.Pow(a, 1.0 / 3));
        var end = (int)Math.Floor(Math.Pow(b, 1.0 / 3));

        Console.WriteLine($"Case #{i}: {end - start + 1}");
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

  int t; cin >> t;
  for (int i = 1; i <= t; i++) {
    int a, b; cin >> a >> b;

    int start = ceil(cbrt(a));
    int end = floor(cbrt(b));

    cout << "Case #" << i << ": " << end - start + 1 << "\n";
  }

  return 0;
}
  ```
