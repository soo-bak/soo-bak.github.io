---
layout: single
title: "[백준 27246] Различные квадраты (C#, C++) - soo:bak"
date: "2023-03-25 16:29:00 +0900"
description: 수학과 구현을 주제로 하는 백준 27246번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [27246번 - Различные квадраты](https://www.acmicpc.net/problem/27246)

## 설명
간단한 수학과 구현에 대한 문제입니다. <br>

문제의 목표는 입력으로 주어지는 `n` 개의 `단위 정사각형`을 이용하여, 가능한 다양한 크기의 정사각형을 만드는 것입니다.<br>

이 때, 한 변의 길이가 `k` 인 정사각형을 만들기 위해서는 <b>k<sup>2</sup></b> 개의 `단위 정사각형`이 필요합니다. <br>

따라서, 위 내용에 대해 적절히 구현을 진행하면 문제를 해결할 수 있습니다. <br>

주의해야 할 점은 문제에서 입력으로 주어지는 `n` 의 범위가 크므로, `64 비트` 데이터를 담을 수 있는 자료형이 필요하다는 것 입니다.<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = long.Parse(Console.ReadLine()!);

      var maxSquares = 0L;
      var k = 1L;
      while (n >= k * k) {
        n -= k * k;
        maxSquares++;
        k++;
      }

      Console.WriteLine(maxSquares);

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

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll n; cin >> n;

  ll maxSquares = 0, k = 1;
  while (n >= k * k) {
    n -= k * k;
    maxSquares++;
    k++;
  }

  cout << maxSquares << "\n";

  return 0;
}
  ```
