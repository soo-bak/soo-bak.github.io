---
layout: single
title: "[백준 5163] Isn’t It Funny How a Bear Likes Honey? (C#, C++) - soo:bak"
date: "2023-05-27 16:23:00 +0900"
---

## 문제 링크
  [5163번 - Isn’t It Funny How a Bear Likes Honey?](https://www.acmicpc.net/problem/5163)

## 설명
곰돌이 푸가 헬륨 풍선을 사용하여 높이 있는 벌집으로 올라가려고 할 때, 충분한 부력을 가지는지 아닌지를 판별하는 문제입니다. <br>

`곰돌이 푸의 무게` 와 `풍선들의 반지름` 이 입력으로 주어지며, 이를 이용하여 부력에 관하여 계산해야 합니다. <br>

<br>
문제의 조건에 따르면, 풍선의 부력은 그 풍선이 갖고 있는 헬륨의 부피에 비례하며, <br>
<b>1리터</b>, 즉, <b>1000cm<sup>3</sup></b> 의 헬륨은 <b>1g</b> 의 무게를 들어올릴 수 있습니다. <br>

<br>
풍선의 부피는 반지름을 활용하여 계산할 수 있습니다. <br>
구체의 부피를 구하는 공식인 <b>V = 4 / 3 πr<sup>3</sup></b> 공식을 이용하여 각 풍선의 부피를 구한 후 합하여 총 부력을 구합니다.

<br>
계산한 총 부력과 곰돌이 푸의 무게를 비교하면, 곰돌이 푸가 벌집으로 올라갈 수 있는지 없는지 판별할 수 있습니다. <br>

<br>
풍선의 부피 단위와 무게 단위, 그리고 부력의 단위 사이의 변환에 주의합니다. <br>

1L는 1,000cm<sup>3</sup> 입니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntDataSet = int.Parse(Console.ReadLine()!);

      for (int d = 1; d <= cntDataSet; d++) {
        var input = Console.ReadLine()!.Split(' ');
        var numBalloons = int.Parse(input[0]);
        var weight = double.Parse(input[1]);

        double totalBuoyancy = 0.0;
        for (int i = 0; i < numBalloons; i++) {
          var radius = double.Parse(Console.ReadLine()!);

          var volume = 4.0 / 3 * Math.PI * Math.Pow(radius, 3);
          var buoyancy = volume / 1_000;

          totalBuoyancy += buoyancy;
        }

        Console.WriteLine($"Data Set {d}:");
        if (totalBuoyancy >= weight) Console.WriteLine("Yes");
        else Console.WriteLine("No");
        if (d != cntDataSet) Console.WriteLine();
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

#define PI acos(-1.0)

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntDataSet; cin >> cntDataSet;

  for (int d = 1; d <= cntDataSet; d++) {
    int numBalloons; double weight;
    cin >> numBalloons >> weight;

    double totalBuoyancy = 0.0;
    for (int i = 0 ; i < numBalloons; i++) {
      double radius; cin >> radius;

      double volume = 4.0 / 3 * PI * pow(radius, 3);
      double buoyancy = volume / 1'000;

      totalBuoyancy += buoyancy;
    }

    cout << "Data Set " << d << ":\n";
    if (totalBuoyancy >= weight) cout << "Yes\n";
    else cout << "No\n";
    if (d != cntDataSet) cout << "\n";
  }

  return 0;
}
  ```
