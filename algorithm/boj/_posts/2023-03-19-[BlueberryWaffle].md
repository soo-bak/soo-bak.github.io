---
layout: single
title: "[백준 27566] Blueberry Waffle (C#, C++) - soo:bak"
date: "2023-03-19 09:59:00 +0900"
---

## 문제 링크
  [27566번 - Blueberry Waffle](https://www.acmicpc.net/problem/27566)

## 설명
  간단한 수학 구현 문제입니다. <br>

  문제의 설명에 따르면, 와플의 한 쪽 면에만 블루베리가 올려져 있습니다. <br>
  이 때, 입력으로 주어지는 `r` 과 `f` 를 통해 와플이 회전한 총 각도를 계산한 후, <br>
  총 회전 후 블루베리가 `윗면` 에 있는지, `아랫면` 에 있는지를 판별하는 문제입니다. <br>

  <b>문제에서 주의해야할 조건은 다음과 같습니다.</b>
  1. `r` 은 와플판이 매 `180` 도를 회전하는 데에 걸리는 <i>초(sec)</i> 이다.
  2. 와플판이 수평이 아닐 경우, <b>항상 수평 방향으로 더 작은 각도 쪽으로 회전하여</b> 수평을 맞춘다.

  위 조건들에 따라 최종적으로 블루베리가 있는 면의 위치를 계산하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()?.Split();
      var r = int.Parse(input![0]);
      var f = int.Parse(input![1]);

      var totalRotation = 180.0 * (f / (double)r);
      var remainedRotation = totalRotation % 360.0;

      if (remainedRotation < 90.0 || remainedRotation > 270.0)
        Console.WriteLine("up");
      else Console.WriteLine("down");

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

  int r, f; cin >> r >> f;

  double totalRotation = 180.0 * (f / (double)r);
  double remainedRotation = fmod(totalRotation, 360.0);

  if (remainedRotation < 90.0 || remainedRotation > 270.0)
    cout << "up\n";
  else cout << "down\n";

  return 0;
}
  ```
