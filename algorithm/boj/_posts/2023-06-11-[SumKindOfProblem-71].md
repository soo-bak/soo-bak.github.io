---
layout: single
title: "[백준 11522] Sum Kind of Problem (C#, C++) - soo:bak"
date: "2023-06-11 19:52:00 +0900"
description: 수열과 사칙 연산을 주제로 하는 백준 11522번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [11522번 - Sum Kind of Problem](https://www.acmicpc.net/problem/11522)

## 설명
연속하는 `n` 개의 정수, 홀수, 그리고 짝수의 합을 계산하는 문제입니다. <br>

각각의 합은 다음과 같이 계산할 수 있습니다. <br>

- 연속하는 정수 : 연속하는 정수 합의 가우스 공식을 사용하여 `n` * (`n + 1`) / `2` 로 계산<br>
- 연속하는 홀수 : 연속하는 정수의 합 공식에 `n` 대신 `2n - 1` 을 대입 후 `n` * `n` 으로 일반화하여 계산<br>
- 연속하는 짝수 : 연속하는 정수의 합 공식에서 `n` 대신 `2n` 을 대입 후 `n` * (`n` + `1`) 으로 일반화하여 계산<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntData = int.Parse(Console.ReadLine()!);

      for (int i = 0; i < cntData; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var k = int.Parse(input[0]);
        var n = int.Parse(input[1]);

        var sumSeq1 = n * (n + 1) / 2;
        var sumSeq2 = n * n;
        var sumSeq3 = n * (n + 1);

        Console.WriteLine($"{k} {sumSeq1} {sumSeq2} {sumSeq3}");
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

  int cntData; cin >> cntData;

  for (int i = 0; i < cntData; i++) {
    int k, n; cin >> k >> n;

    int sumSeq1 = n * (n + 1) / 2;
    int sumSeq2 = n * n;
    int sumSeq3 = n * (n + 1);

    cout << k << " " << sumSeq1 << " " << sumSeq2 << " " << sumSeq3 << "\n";
  }

  return 0;
}
  ```
