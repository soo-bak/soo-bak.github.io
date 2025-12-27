---
layout: single
title: "[백준 11650] 좌표 정렬하기 (C#, C++) - soo:bak"
date: "2023-05-29 21:19:00 +0900"
description: 정렬과 좌표 평면 등을 주제로 하는 백준 11650번 알고리즘 문제를 C# 의 튜플, Tuple 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11650
  - C#
  - C++
  - 알고리즘
  - 정렬
keywords: "백준 11650, 백준 11650번, BOJ 11650, SortingCoord, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [11650번 - 좌표 정렬하기](https://www.acmicpc.net/problem/11650)

## 설명
입력으로 주어지는 2차원 평면 위의 점들을 정렬하는 문제입니다. <br>

정렬의 규칙은 다음과 같습니다. <br>

- `x` 좌표가 증가하는 순으로 정렬 <br>
- `x` 좌표가 같다면 `y` 좌표가 증가하는 순으로 정렬 <br>

<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  using System.Text;
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var points = new Tuple<int, int>[n];
      for (int i = 0; i < n; i++) {
        var input = Console.ReadLine()!.Split(' ');
        points[i] = Tuple.Create(int.Parse(input[0]), int.Parse(input[1]));
      }

      Array.Sort(points);

      var sb = new StringBuilder();

      foreach (var point in points)
        sb.AppendLine($"{point.Item1} {point.Item2}");
      Console.Write(sb.ToString());

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

typedef pair<int, int> pii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vector<pii> points(n);
  for (int i = 0; i < n; i++)
    cin >> points[i].first >> points[i].second;

  sort(points.begin(), points.end());

  for (const auto& point : points)
    cout << point.first << " " << point.second << "\n";

  return 0;
}
  ```
