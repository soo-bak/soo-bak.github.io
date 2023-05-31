---
layout: single
title: "[백준 4948] 베르트랑 공준 (C#, C++) - soo:bak"
date: "2023-05-28 16:00:00 +0900"
description: 수학과 베르트랑 공준, 에라토스테네스의 체, 소수 찾기를 주제로 하는 백준 4948번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [4948번 - 베르트랑 공준](https://www.acmicpc.net/problem/4948)

## 설명
`베르트랑 공준` 예 따라 주어진 자연수 `n` 보다 크고, `2n` 보다 작거나 같은 범위에서 <b>소수의 개수</b> 를 찾는 문제입니다. <br>

`에라토스테네스의 체` 알고리즘을 활용하여 `2n` 까지의 범위에서 소수를 찾고, `n` 보다 큰 소수의 개수를 세면 됩니다. <br>

`에라토스테네스의 체` 에 대한 자세한 설명은 [여기](https://soo-bak.github.io/algorithm/theory/) 에서 확인하실 수 있습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      const int MAX = 2 * 123456;

      var isPrime = Enumerable.Repeat(true, MAX + 1).ToArray();
      isPrime[0] = isPrime[1] = false;

      for (int i = 2; i * i <= MAX; i++) {
        if (isPrime[i]) {
          for (int j = i * i; j <= MAX; j += i)
            isPrime[j] = false;
        }
      }

      while (true) {
        var n = int.Parse(Console.ReadLine()!);

        if (n == 0) break ;

        int cntPrime = 0;
        for (int i = n + 1; i <= 2 * n; i++)
          if (isPrime[i]) cntPrime++;

        Console.WriteLine(cntPrime);
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

#define MAX 2 * 123456

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vector<bool> isPrime(MAX + 1, true);
  isPrime[0] = isPrime[1] = false;

  for (int i = 2; i * i <= MAX; i++) {
    if (isPrime[i]) {
      for (int j = i * i; j <= MAX; j += i)
        isPrime[j] = false;
    }
  }

  while (true) {
    int n; cin >> n;

    if (n == 0) break ;

    int cntPrime = 0;
    for (int i = n + 1; i <= 2 * n; i++)
      if (isPrime[i]) cntPrime++;

    cout << cntPrime << "\n";
  }

  return 0;
}
  ```
