---
layout: single
title: "[백준 2869] 달팽이는 올라가고 싶다 (C#, C++) - soo:bak"
date: "2023-05-23 09:51:00 +0900"
---

## 문제 링크
  [2869번 - 달팽이는 올라가고 싶다](https://www.acmicpc.net/problem/2869)

## 설명
달팽이가 나무 막대를 올라가는 데 걸리는 시간을 계산하는 문제입니다. <br>

달팽이는 낮에 `a` 미터를 올라가지만, 밤에는 `b` 미터만큼 미끄러집니다. <br>

하지만, 막대의 정상에 도달하면 미끄러지지 않습니다. <br>

따라서, 낮에 마지막으로 올라갈 때에는 미끄러지지 않기 때문에 이를 고려하여 수식을 세워 계산해야 합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var a = int.Parse(input[0]);
      var b = int.Parse(input[1]);
      var v = int.Parse(input[2]);

      var day = (v - b - 1) / (a - b) + 1;
      Console.WriteLine(day);

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

  int a, b, v; cin >> a >> b >> v;

  int day = (v - b - 1) / (a - b) + 1;

  cout << day << "\n";

  return 0;
}
  ```
