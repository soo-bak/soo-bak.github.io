---
layout: single
title: "[백준 9310] Arithmetic and Geometric Sums (C#, C++) - soo:bak"
date: "2023-08-29 11:59:00 +0900"
description: 수학, 구현 등을 주제로 하는 백준 9310번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9310
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 9310, 백준 9310번, BOJ 9310, ArithmeticGeometricSums, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [9310번 - Arithmetic and Geometric Sums](https://www.acmicpc.net/problem/9310)

## 설명
주어진 세 수가 산술 혹은 기하 급수의 처음 세 항일 때,<br>
<br>
해당 세 항을 통하여 주어진 급수가 산술 급수인지 기하 급수인지 판별하고, <br>
<br>
해당 급수의 합을 `n` 번째 항 까지 계산하여 출력하는 문제입니다.<br>
<br>
산술 급수와 기하 급수를 구분하기 위해, 두 번째 항과 첫 번째 항의 차이, 그리고 세 번째 항과 두 번째 항의 차이를 비교한 후,<br>
<br>
두 차이가 동일하다면 주어진 급수는 산술 급수임을, 그렇지 않다면 주어진 급수는 기하 급수임을 이용하여 문제를 풀이합니다. <br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

       while (true) {
        var n = int.Parse(Console.ReadLine()!);
        if (n == 0) break ;

        var input = Console.ReadLine()!.Split(' ');
        var a = long.Parse(input[0]);
        var b = long.Parse(input[1]);
        var c = long.Parse(input[2]);

        long ans = 0;
        if (b - a == c - b) ans = n * (2 * a + (n - 1) * (b - a)) / 2;
        else ans = (long)(a * (Math.Pow((double) b / a, n) - 1) / ((double) b / a - 1));

        Console.WriteLine(ans);
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

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  while (true) {
    int n; cin >> n;
    if (n == 0) break ;

    ll a, b, c; cin >> a >> b >> c;

    ll ans = 0;
    if (b - a == c - b) ans = n * (2 * a + (n - 1) * (b - a)) / 2;
    else ans = a * (pow(b / a, n) - 1) / (b / a - 1);

    cout << ans << "\n";
  }


  return 0;
}
  ```
