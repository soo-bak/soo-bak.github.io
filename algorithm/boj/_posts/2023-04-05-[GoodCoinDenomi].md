---
layout: single
title: "[백준 26350] Good Coin Denomination (C#, C++) - soo:bak"
date: "2023-04-05 23:10:00 +0900"
description: 구현과 수학, 시뮬레이션을 주제로 하는 백준 26350번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [26350번 - Good Coin Denomination](https://www.acmicpc.net/problem/26350)

## 설명
단순한 구현 문제입니다. <br>

문제의 목표는 입력으로 주어지는 동전들에 대하여, 이전 동전이 그 다음 동전의 `2` 배 미만인지, 아닌지를 판별하는 것입니다.<br>

판별이 완료되면, 문제의 출력 조건에 맞추어 적절히 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);

      for (var i = 0; i < n; i++) {
        var input = Console.ReadLine()?.Split();
        var d = int.Parse(input![0]);

        var coins = new List<int>();
        for (var j = 0; j < d; j++)
          coins.Add(int.Parse(input![j + 1]));

        Console.Write("Denominations: ");
        for (var j = 0; j < d; j++)
          Console.Write(coins[j] + " ");
        Console.WriteLine();

        var isValid = true;
        var prev = coins[0];
        for (var j = 1; j < d; j++) {
          if (coins[j] < 2 * prev) {
            isValid = false;
            break;
          }
          prev = coins[j];
        }

        if (isValid) Console.WriteLine("Good coin denominations!");
        else Console.WriteLine("Bad coin denominations!");
        if (i != n - 1) Console.WriteLine();
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

  int n; cin >> n;

  for (int i = 0; i < n; i++) {
    int d; cin >> d;
    vector<int> coins(d);

    for (int j = 0; j < d; j++)
      cin >> coins[j];

    cout << "Denominations: ";
    for (int j = 0; j < d; j++)
      cout << coins[j] << " ";
    cout << "\n";

    bool isValid = true;
    int prev = coins[0];
    for (int j = 1; j < d; j++) {
      if (coins[j] < 2 * prev) {
        isValid = false;
        break;
      }
      prev = coins[j];
    }

    if (isValid) cout << "Good coin denominations!\n";
    else cout << "Bad coin denominations!\n";
    if (i != n - 1) cout << "\n";
  }

  return 0;
}
  ```
