---
layout: single
title: "[백준 27239] Шахматная доска (C#, C++) - soo:bak"
date: "2023-03-30 23:28:00 +0900"
---

## 문제 링크
  [27239번 - Шахматная доска](https://www.acmicpc.net/problem/27239)

## 설명
간단한 사칙연산을 이용한 구현 문제입니다. <br>

문제의 목표는 입력으로 주어지는 `n` 에 해당되는 체스판의 위치를 출력하는 것입니다. <br>

체스판의 크기는 가로, 세로 각각 `8` 이므로, `n` 에 대하여 다음과 같이 행/열의 값을 계산할 수 있습니다. <br>
- 행 : `(n - 1) / 8`
- 열 : `(n - 1) % 8`

이후 `a` 문자에 위에서 계산한 열의 값을 더하여 해당되는 열의 알파벳을 계산합니다. <br>

또한, 위에서 계산한 행의 값은 `0` 부터 시작하므로, `1` 을 더하여 `1` 부터 시작하는 행의 값을 계산합니다. <br>

최종적으로 문제의 출력 조건에 맞게 행과 열의 결과를 출력합니다.

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var row = (n - 1) / 8;
      var col = (n - 1) % 8;

      char c = (char)('a' + col);

      Console.WriteLine($"{c}{row + 1}");

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

  int row = (n - 1) / 8,
      col = (n - 1) % 8;

  char c = 'a' + col;

  cout << c << row + 1 << "\n";

  return 0;
}
  ```
