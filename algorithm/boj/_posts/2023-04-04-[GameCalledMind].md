---
layout: single
title: "[백준 25850] A Game Called Mind (C#, C++) - soo:bak"
date: "2023-04-04 19:00:00 +0900"
description: 구현고 정렬을 주제로 하는 백준 25850번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 25850
  - C#
  - C++
  - 알고리즘
keywords: "백준 25850, 백준 25850번, BOJ 25850, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [25850번 - A Game Called Mind](https://www.acmicpc.net/problem/25850)

## 설명
정렬과 구현에 관한 간단한 문제입니다. <br>

입력된 카드들을 정렬한 후, 각 플레이어가 카드를 내려놓을 순서를 출력합니다. <br>

각 플레이어의 카드 값을 묶어서 정렬하기 위하여 C# 에서는 `Tuple<>` 을, C++ 에서는 `Pair<>` 을 사용했습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var p = int.Parse(Console.ReadLine()!);
      var cards = new List<Tuple<int, char>>();

      for (var i = 0; i < p; i++) {
        var input = Console.ReadLine()?.Split();
        var c = int.Parse(input![0]);
        for (var j = 1; j < c + 1; j++) {
          var card = int.Parse(input![j]);
          cards.Add(new Tuple<int, char>(card, (char)('A' + i)));
        }
      }

      cards.Sort();

      foreach (var card in cards)
        Console.Write(card.Item2);
      Console.WriteLine();

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

typedef pair<int , char> pic;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int p; cin >> p;

  vector<pic> cards;

  for (int i = 0; i < p; i++) {
    int c; cin >> c;
    for (int j = 0; j < c; j++) {
      int card; cin >> card;
      cards.push_back({card, 'A' + i});
    }
  }

  sort(cards.begin(), cards.end());

  for (const auto& card : cards)
      cout << card.second;
  cout << "\n";

  return 0;
}
  ```
