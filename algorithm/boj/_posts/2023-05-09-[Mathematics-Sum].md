---
layout: single
title: "[백준 26545] Mathematics (C#, C++) - soo:bak"
date: "2023-05-09 23:48:00 +0900"
---

## 문제 링크
  [26545번 - Mathematics](https://www.acmicpc.net/problem/26545)

## 설명
입력으로 주어지는 정수 목록의 합을 구하는 문제입니다. <br>

입력의 첫 번째 줄에서 주어지는 정수 `n` 개 만큼 정수를 읽어들이고, 숫자들의 합을 구하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      int sum = 0;
      for (int i = 0; i < n; i++) {
        var num = int.Parse(Console.ReadLine()!);
        sum += num;
      }

      Console.WriteLine(sum);
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

  int sum = 0;
  for (int i = 0; i < n; i++) {
    int num; cin >> num;
    sum += num;
  }

  cout << sum << "\n";

  return 0;
}
  ```
