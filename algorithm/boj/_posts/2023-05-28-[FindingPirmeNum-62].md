---
layout: single
title: "[백준 1929] 소수 구하기 (C#, C++) - soo:bak"
date: "2023-05-28 15:49:00 +0900"
description: 수학과 소수 찾기, 에라토스테네스의 체를 주제로 하는 백준 1929번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [1929번 - 소수 구하기](https://www.acmicpc.net/problem/1929)

## 설명
`에라토스테네스의 체` 를 활용하여 주어진 숫자 `m` 이상 `n` 이하의 범위에서 모든 소수를 찾고 출력하는 문제입니다. <br>

`에라토스테네스의 체` 에 대한 자세한 설명은 [여기](https://soo-bak.github.io/algorithm/theory/) 에서 확인하실 수 있습니다. <br>

<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {

  using System.Text;

  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var m = int.Parse(input[0]);
      var n = int.Parse(input[1]);

      var isPrime = Enumerable.Repeat(true, n + 1).ToArray();
      isPrime[0] = isPrime[1] = false;

      for (int i = 2; i * i <= n; i++) {
        if (isPrime[i]) {
          for (int j = i * i; j <= n; j += i)
            isPrime[j] = false;
        }
      }

      var sb = new StringBuilder();
      for (int i = m; i <= n; i++) {
        if (isPrime[i])
          sb.AppendLine(i.ToString());
      }

      Console.Write(sb.ToString());

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

  int m, n; cin >> m >> n;

  vector<bool> isPrime(n + 1, true);
  isPrime[0] = isPrime[1] = false;

  for (int i = 2; i * i <= n; i++) {
    if (isPrime[i]) {
      for (int j = i * i; j <= n; j += i)
        isPrime[j] = false;
    }
  }

  for (int i = m; i <= n; i++) {
    if (isPrime[i]) cout << i << "\n";
  }

  return 0;
}
  ```
