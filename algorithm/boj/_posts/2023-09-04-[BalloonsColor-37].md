---
layout: single
title: "[백준 9635] Balloons Colors (C#, C++) - soo:bak"
date: "2023-09-04 11:26:00 +0900"
description: 수학, 사칙연산, 구현 등을 주제로 하는 백준 9635번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [9635번 - Balloons Colors](https://www.acmicpc.net/problem/9635)

## 설명
`n` 개의 문제가 난이도 순서대로 주어질 때, 가장 쉬운 문제 (`1`번) 가 `X`색을, 가장 어려운 문제 (`n`번) 가 `Y`색인지 확인하는 문제입니다. <br>
<br>
위 확인을 통해 총 `4` 가지의 결과 중 하나를 출력합니다. <br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var t = int.Parse(Console.ReadLine()!);
      for (int i = 0 ; i < t; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var n = int.Parse(input[0]);
        var x = int.Parse(input[1]);
        var y = int.Parse(input[2]);

        var colors = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();

        var wrongEasy = (colors[0] == x);
        var wrongHard = (colors[n - 1] == y);

        if (wrongEasy && wrongHard)
          Console.WriteLine("BOTH");
        else if (wrongEasy)
          Console.WriteLine("EASY");
        else if (wrongHard)
          Console.WriteLine("HARD");
        else Console.WriteLine("OKAY");
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

  while (t--) {
    int n, x, y; cin >> n >> x >> y;

    vector<int> colors(n);
    for (int i = 0; i < n; i++)
      cin >> colors[i];

    bool wrongEasy = (colors[0] == x);
    bool wrongHard = (colors[n - 1] == y);

    if (wrongEasy && wrongHard) cout << "BOTH\n";
    else if (wrongEasy) cout << "EASY\n";
    else if (wrongHard) cout << "HARD\n";
    else cout << "OKAY\n";
  }

  return 0;
}
  ```
