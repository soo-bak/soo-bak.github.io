---
layout: single
title: "[백준 26849] Non Classical Problem (C#, C++) - soo:bak"
date: "2024-03-29 00:01:00 +0900"
description: 수학, 구현, 사칙연산 등을 주제로 하는 백준 26849번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [26849번 - Non Classical Problem](https://www.acmicpc.net/problem/26849)

## 설명
입력으로주어지는 정수 `a` 와 `b` 의 한 쌍에 대하여, `a` / `b` 를 계산한 실수 결과의 최솟값, 최댓값을 탐색하고, 합을 계산하는 단순한 문제입니다.<br>

<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var numbers = Enumerable.Range(0, n)
        .Select(_ => {
          var input = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();
          return (double)input[0] / input[1];
        }).ToList();

      var sum = numbers.Sum();
      var min = numbers.Min();
      var max = numbers.Max();

      Console.WriteLine($"{min:F6} {max:F6} {sum:F6}");

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

  vector<double> numbers(n);
  double sum = 0;
  for (int i = 0; i < n; i++) {
    int a, b; cin >> a >> b;
    numbers[i] = static_cast<double>(a) / b;
    sum += numbers[i];
  }

  auto minMax = minmax_element(numbers.begin(), numbers.end());

  cout << fixed << setprecision(6);
  cout << *minMax.first << " " << *minMax.second << " " << sum << "\n";

  return 0;
}
  ```
