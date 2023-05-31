---
layout: single
title: "[백준 5220] Error Detection (C#, C++) - soo:bak"
date: "2023-05-28 07:09:00 +0900"
description: 수학과 비트 연산, 비트 다루기, 탐색 등을 주제로 하는 백준 5220번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [5220번 - Error Detection](https://www.acmicpc.net/problem/5220)

## 설명
입력으로 주어진 정수를 `16` 비트의 `2` 진수로 변환했을 때,<br>

해당 `2` 진수에서 `1` 의 개수의 `홀수` 인지, `짝수` 인지를 `체크 비트` 를 통해 확인하는 문제입니다. <br>

문제의 조건에 따르면, `체크 비트` 는 `1` 의 개수가 홀수일 때 `1` 이고, 짝수일 때 `0` 입니다. <br>

따라서, `1` 의 개수가 `홀수` 이고 `체크 비트` 가 `1` 이거나, `1` 의 개수가 `짝수` 이고 `체크 비트` 가 `0` 이라면 `Valid` 를, <br>

그렇지 않으면, `Corrupt` 를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntCase = int.Parse(Console.ReadLine()!);

      for (int c = 0; c < cntCase; c++) {
        var input = Console.ReadLine()!.Split(' ');

        var num = int.Parse(input[0]);
        var checkBit = int.Parse(input[1]);

        var cntOne = Convert.ToString(num, 2).ToCharArray().Sum(b => b - '0');

        if (cntOne % 2 == checkBit) Console.WriteLine("Valid");
        else Console.WriteLine("Corrupt");
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

  int cntCase; cin >> cntCase;

  for (int c = 0; c < cntCase; c++) {
    int num, checkBit; cin >> num >> checkBit;

    bitset<16> binary(num);
    int cntOne = binary.count();

    if (cntOne % 2 == checkBit) cout << "Valid\n";
    else cout << "Corrupt\n";
  }

  return 0;
}
  ```
