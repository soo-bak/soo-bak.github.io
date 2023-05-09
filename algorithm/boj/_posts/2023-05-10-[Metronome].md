---
layout: single
title: "[백준 27389] Metronome (C#, C++) - soo:bak"
date: "2023-05-10 03:03:00 +0900"
---

## 문제 링크
  [27389번 - Metronome](https://www.acmicpc.net/problem/27389)

## 설명
노래의 길이가 '틱' 으로 표시될 떄, 노래의 끝에 정확히 멈추기 위하여 메트로놈 열쇠를 몇 번 회전해야 하는지 계산하는 문제입니다. <br>

문제의 조건에 따르면, 열쇠를 한 번 회전할 때마다 `4` 개의 틱을 발생시킵니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var cntRevolution = n / 4.0;

      Console.WriteLine($"{cntRevolution:F2}");
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

  double cntRevolution = n / 4.0;

  cout.setf(ios::fixed); cout.precision(2);
  cout << cntRevolution << "\n";

  return 0;
}
  ```
