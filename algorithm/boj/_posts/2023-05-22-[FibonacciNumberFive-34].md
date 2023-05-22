---
layout: single
title: "[백준 10870] 피보나치 수 5 (C#, C++) - soo:bak"
date: "2023-05-22 15:51:00 +0900"
---

## 문제 링크
  [10870번 - 피보나치 수 5](https://www.acmicpc.net/problem/10870)

## 설명
피보나치 수열에서 `n` 번째 피보나치 수를 구하는 문제입니다. <br>

피보나치 수열을 구현하는 방법에는 여러 가지가 있습니다. <br>

그 중 하나는 다이나믹 프로그래밍을 이용하는 방법입니다. <br>

다이나믹 프로그래밍은, 큰 문제를 작은 문제로 나눠서 풀이하며 그 결과를 저장하고 나중에 저장된 값을 사용하여 빠르게 답을 찾는 방법입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      const int MAX = 21;

      var fibo = new int[MAX];
      fibo[0] = 0; fibo[1] = 1;

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 2; i <= n; i++)
        fibo[i] = fibo[i - 1] + fibo[i - 2];

      Console.WriteLine(fibo[n]);

    }
  }
}

  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

#define MAX 21

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vector<int> fibo(MAX);
  fibo[0] = 0; fibo[1] = 1;

  int n; cin >> n;

  for (int i = 2; i <= n; i++)
    fibo[i] = fibo[i - 1] + fibo[i - 2];

  cout << fibo[n] << "\n";

  return 0;
}
  ```
