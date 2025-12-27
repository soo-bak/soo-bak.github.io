---
layout: single
title: "[백준 9298] Ant Entrapment (C#, C++) - soo:bak"
date: "2023-08-23 18:57:00 +0900"
description: 수학, 기하학 등을 주제로 하는 백준 9298번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9298
  - C#
  - C++
  - 알고리즘
  - 수학
  - 기하학
keywords: "백준 9298, 백준 9298번, BOJ 9298, AntEntrapment, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [9298번 - Ant Entrapment](https://www.acmicpc.net/problem/9298)

## 설명
개미들의 위치들이 주어질 때, 모든 개미들을 포함하는 가장 작은 직사각형 영역의 넓이와 둘레는 계산하는 문제입니다. <br>
<br>
풀이과정은 다음과 같습니다. <br>
<br>
- <b>최소 및 최대 좌표 찾기</b> <br>
<br>
입력받은 모든 개미의 위치 중 `x` 좌표의 최솟값과 최댓값, `y` 좌표의 최솟값과 최댓값을 찾습니다.<br>
<br>
이 값을 이용해 직사각형의 꼭지점들을 결정할 수 있습니다.<br>
<br>
- <b> 넓이 및 둘레 계산 </b><br>
  - 넓이 = (`x의 최댓값` - `x의 최솟값`) * (`y의 최댓값` - `y의 최솟값`)<br>
  - 둘레 = `2` * ((`x의 최댓값` - `x의 최솟값`) + (`y의 최댓값` - `y의 최솟값`))<br>
<br>

이후 주어진 출력 형식에 맞추어 각 테스트 케이스별로 계산된 넓이와 둘레를 출력합니다. <br>
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
      for (int tc = 1; tc <= t; tc++) {
        var n = int.Parse(Console.ReadLine()!);

        double minX = 1001, minY = 1001, maxX = -1001, maxY = -1001;
        for (int i = 0 ; i < n; i++) {
          var input = Console.ReadLine()!.Split(' ');
          var x = double.Parse(input[0]);
          var y = double.Parse(input[1]);

          minX = Math.Min(minX, x); minY = Math.Min(minY, y);
          maxX = Math.Max(maxX, x); maxY = Math.Max(maxY, y);
        }

        var area = (maxX - minX) * (maxY - minY);
        var perimeter = 2 * ((maxX - minX) + (maxY - minY));

        Console.WriteLine($"Case {tc}: Area {area:F9}, Perimeter {perimeter:F9}");
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
  for (int tc = 1; tc <= t; tc++) {
    int n; cin >> n;

    double minX = 1001, minY = 1001, maxX = -1001, maxY = -1001;
    for (int i = 0; i < n; i++) {
      double x, y; cin >> x >> y;

      minX = min(minX, x), minY = min(minY, y);
      maxX = max(maxX, x), maxY = max(maxY, y);
    }

    double area = (maxX - minX) * (maxY - minY);
    double perimeter = 2 * ((maxX - minX) + (maxY - minY));

    cout.setf(ios::fixed); cout.precision(9);
    cout << "Case " << tc << ": Area " << area << ", Perimeter " << perimeter << "\n";
  }

  return 0;
}
  ```
