---
layout: single
title: "[백준 13221] Manhattan (C#, C++) - soo:bak"
date: "2023-06-21 08:47:00 +0900"
description: 구현과 수학, 사칙연산 등을 주제로 하는 백준 13221번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 13221
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 기하학
  - arithmetic
keywords: "백준 13221, 백준 13221번, BOJ 13221, ManhattanDist, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [13221번 - Manhattan](https://www.acmicpc.net/problem/13221)

## 설명
택시 기하학의 맨해튼 거리와 관련된 문제입니다. <br>

뉴욕 맨해튼 섬의 격자처럼 교차하는 거리들에서, 택시들이 북쪽, 남쪽, 동쪽, 서쪽 방향으로만 이동할 수 있다고 가정했을 때, <br>

한 교차점에서 다른 교차점까지의 거리를 `Manhatten Distance` 라고 합니다. <br>

각 택시들의 위치가 입력으로 주어질 때, 승객과 택시 사이의 맨해튼 거리를 계산하여 승객과 거리가 가장 가까운 택시의 위치를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    public struct Taxi {
      public int X, Y, Dist;
    }

    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var x = int.Parse(input[0]);
      var y = int.Parse(input[1]);
      var n = int.Parse(Console.ReadLine()!);

      var taxis = new Taxi[n];
      for (int i = 0; i < n; i++) {
        var coords = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();
        taxis[i] = new Taxi {
          X = coords[0],
          Y = coords[1],
          Dist = Math.Abs(x - coords[0]) + Math.Abs(y - coords[1])
        };
      }

      taxis = taxis.OrderBy(t => t.Dist).ToArray();

      Console.WriteLine($"{taxis[0].X} {taxis[0].Y}");
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

struct Taxi {
  int x, y, dist;
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int x, y, n; cin >> x >> y >> n;

  vector<Taxi> taxis(n);
  for (int i = 0; i < n; i++) {
    cin >> taxis[i].x >> taxis[i].y;
    taxis[i].dist = abs(x - taxis[i].x) + abs(y - taxis[i].y);
  }

  sort(taxis.begin(), taxis.end(), [](const Taxi& a, const Taxi& b) { return a.dist < b.dist;});

  cout << taxis[0].x << " " << taxis[0].y << "\n";

  return 0;
}
  ```
