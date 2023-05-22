---
layout: single
title: "[백준 4850] Baskets of Gold Coins (C#, C++) - soo:bak"
date: "2023-05-23 07:27:00 +0900"
---

## 문제 링크
  [4850번 - Baskets of Gold Coins](https://www.acmicpc.net/problem/4850)

## 설명
각각의 바구니에서 골드 코인을 특정 개수만큼 꺼내어 그 무게를 측정하여, 가장 가벼운 코인이 들어있는 바구니를 찾는 문제입니다. <br>

문제의 설명에 따르면, 마법사는 `1` 번 바구니에서 `1` 개, `2` 번 바구니에서 `2` 개, ... , `n - 1` 번 바구니에서 `n - 1` 개의 코인을 선택하여 측정합니다. <br>

입력으로는 바구니의 개수 `n` , 코인의 표준 무게 `w` , 가장 가벼운 코인과의 무게 차이 `d` , 그리고 마법사가 측정한 코인들의 `총 무게` 가 주어집니다. <br>

이 떄, <b>코인이 모두 표준 무게였을 때의 총 무게</b>에서 <b>마법사가 측정한 코인들의 총 무게</b>를 빼고, 그 차이를 `d` 로 나누면 가장 가벼운 코인이 들어있는 바구니의 번호를 알 수 있습니다. <br>

`n` 번쨰 바구니가 가장 가벼운 바구니가 될 수도 있다는 점에 주의합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      while (true) {
        var input = Console.ReadLine()?.Split(' ');
        if (input == null) break ;

        var n = int.Parse(input[0]);
        var w = int.Parse(input[1]);
        var d = int.Parse(input[2]);
        var totalWeight = int.Parse(input[3]);

        var standardWeight = w * ((n - 1) * n) / 2;
        var numBasket = (standardWeight - totalWeight) / d;

        if (numBasket == 0) Console.WriteLine(n);
        else Console.WriteLine(numBasket);
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

  while (true) {
    int n, w, d, totalWeight;
    cin >> n >> w >> d >> totalWeight;
    if (cin.eof()) break ;

    int standardWeight = w * ((n - 1) * n) / 2;
    int numBasket = (standardWeight - totalWeight) / d;

    if (numBasket == 0) cout << n << "\n";
    else cout << numBasket << "\n";
  }

  return 0;
}
  ```
