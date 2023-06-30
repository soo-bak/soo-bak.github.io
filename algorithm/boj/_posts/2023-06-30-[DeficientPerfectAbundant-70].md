---
layout: single
title: "[백준 6975] Deficient, Perfect, and Abundant (C#, C++) - soo:bak"
date: "2023-06-30 14:56:00 +0900"
description: 수학, 약수, 구현, 조건 분기 등을 주제로 하는 백준 6975번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [6975번 - Deficient, Perfect, and Abundant](https://www.acmicpc.net/problem/6975)

## 설명
입력으로 주어지는 양의 정수 `n` 이 `부족한 수(deficient number)` 인지, `완전한 수(perfect number)` 인지,<br>

아니면 `풍부한 수(perfect number)` 인지 판별하는 문제입니다. <br>

문제의 조건에 따르면, 양의 정수 `n` 이 `완전한 수`라는 것은 자기 자신을 제외한 약수들의 합이 `n` 과 같다는 것을 의미합니다. <br>

만약, 합이 `n` 보다 <b>작으면</b> 그 수는 `부족한 수` 이며, 합이 `n` 보다 <b>크다면</b> 그 수는 `풍부한 수` 입니다. <br>

위 조건에 따라 구현을 진행한 후 `n` 이 어떤 수인지 판별하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var t = int.Parse(Console.ReadLine()!);

      for (int c = 0; c < t; c++) {
        var n = int.Parse(Console.ReadLine()!);

        int sum = 1;
        for (int i = 2; i * i <= n; i++) {
          if (n % i == 0) {
            if (i * i != n) sum += i + n / i;
            else sum += i;
          }
        }

        if (sum < n) Console.WriteLine($"{n} is a deficient number.");
        else if (sum == n) Console.WriteLine($"{n} is a perfect number.");
        else Console.WriteLine($"{n} is an abundant number.");

        if (c != t - 1) Console.WriteLine();
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;

  for (int c = 0; c < t; c++) {
    int n; cin >> n;

    int sum = 1;
    for (int i = 2; i * i <= n; i++) {
      if (n % i == 0) {
        if (i * i != n)
          sum += i + n / i;
        else
          sum += i;
      }
    }

    if (sum < n) cout << n << " is a deficient number.\n";
    else if (sum == n) cout << n << " is a perfect number.\n";
    else cout << n << " is an abundant number.\n";

    if (c != t - 1) cout << "\n";
  }

  return 0;
}
  ```
