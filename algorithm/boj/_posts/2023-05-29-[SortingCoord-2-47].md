---
layout: single
title: "[백준 11651] 좌표 정렬하기 2 (C#, C++) - soo:bak"
date: "2023-05-29 09:38:00 +0900"
description: 정렬과 탐색, 좌표 평면 등을 주제로 하는 백준 11651번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [11651번 - 좌표 정렬하기 2](https://www.acmicpc.net/problem/11651)

## 설명
2차원 평면 위의 점들을 문제의 조건에 따른 정렬 기준에 따라서 정렬하는 문제입니다. <br>

정렬 기준은 다음과 같습니다. <br>

- `y` 좌표가 증가하는 순으로 정렬 <br>
- `y` 좌표가 같다면, `x` 좌표가 증가하는 순으로 정렬 <br>

`C#` 에서는 `LINQ` 를 활용하여 정렬하였고,<br>

`C++` 에서는 `sort()` 함수의 세 번째 매개변수로 사용될 별도의 비교함수를 구현하여 정렬하였습니다. <br>

<br>
`C#` 에서는 `StringBuilder` 을 사용하지 않으면 `시간 초과` 가 됨에 주의합니다. <br>

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

      var coord = new (int, int)[n];
      for (int i = 0; i < n; i++) {
        var points = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();
        coord[i] = (points[0], points[1]);
      }

      coord = coord
            .OrderBy(p => p.Item2)
            .ThenBy(p => p.Item1)
            .ToArray();

      var sb = new StringBuilder();
      foreach (var points in coord)
        sb.AppendLine($"{points.Item1} {points.Item2}");

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

bool comp(const pii& a, const pii& b) {
  if (a.second == b.second)
    return a.first < b.first;
  return a.second < b.second;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vector<pii> coord(n);
  for (int i = 0; i < n; i++)
    cin >> coord[i].first >> coord[i].second;

  sort(coord.begin(), coord.end(), comp);

  for (const auto& points : coord)
    cout << points.first << " " << points.second << "\n";

  return 0;
}
  ```
