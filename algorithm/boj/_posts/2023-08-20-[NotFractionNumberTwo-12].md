---
layout: single
title: "[백준 29196] 소수가 아닌 수 2 (C#, C++) - soo:bak"
date: "2023-08-20 10:02:00 +0900"
description: 수학, 사칙연산, 구현 등을 주제로 하는 백준 29196번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 29196
  - C#
  - C++
  - 알고리즘
keywords: "백준 29196, 백준 29196번, BOJ 29196, NotFractionNumberTwo, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [29196번 - 소수가 아닌 수 2](https://www.acmicpc.net/problem/29196)

## 설명
문제의 목표는 소수 `k` 를 입력받아, `k` 의 근사치로 나타낼 수 있는 분수 `p / q` 를 찾는 것입니다. <br>
<br>
이 때, `k` 와 `p / q` 의 절대오차 또는 상대오차는 <b>10<sup>-6</sup></b> 이하여야 합니다.<br>
<br>
풀이과정은 다음과 같습니다.<br>
<br>
- <b>문자열 처리</b> : 주어진 소수 `k` 에서 소수점 아래 부분만 추출합니다. <br>
<br>
- <b>비반복 소수와 반복 소수 구분</b> :<br>
<br>
  - 비반복 소수와 반복 소수를 구분하는 것은 해당 소수를 분수로 변환할 때 사용할 방법이 다르기 때문입니다. <br>
<br>
  - <b>비반복 소수</b> : 소수점 아래의 숫자가 반복되지 않는 경우, 예를들어 `0.12` 또는 `0.12345` 등<br>
<br>
  - <b>반복 소수</b> : 소수점 아래의 숫자가 반복되는 경우, 예를 들어 `0.3333...` 또는 `0.4646...` 등<br>
<br>
  - 반복 여부를 판단하는 방법으로, 간단하게 첫 번째 숫자와 마지막 숫자가 같은 경우를 반복 소수로 간주합니다.<br>
(절대오차 또는 상대오차 <b>10<sup>-6</sup> 내에서 충분히 유효하게 판정할 수 있습니다.)<br>
<br>
- <b>분수 변환</b><br>
<br>
  - <b>비반복 소수의 경우</b> : 소수점 아래 숫자를 분자로 사용하고, 분모는 해당 숫자의 길이에 따른 `10` 의 거듭제곱으로 설정합니다.<br>
<br>
  - <b>반복 소수의 경우</b> : 분자는 소수점 아래의 숫자로 사용하고, 분모는 해당 숫자의 길이만큼 `9` 를 반복하여 설정합니다.<br>
이는 반복하는 소수의 특성을 이용한 것으로 `0.3333...` 을 해당 방법으로 분수로 표현하면 `1 / 3` 이 됩니다.<br>
<br>
- <b>최대공약수를 이용하여 기약분수로 변환</b> : 분자와 분모의 최대공약수를 구한 후, 분자와 분모를 최대 공약수로 나누어 기약분수 형태로 변환합니다.<br>

> 참고 : [GCD(최대공약수)와 유클리드 호제법의 원리 - soo:bak](https://soo-bak.github.io/algorithm/theory/gcd-euclidean-explained/)

<br>
- <b>결과 출력</b> : 구한 분수를 출력합니다.<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    static int Gcd(int a, int b) {
      if (b == 0) return a;
      return Gcd(b, a % b);
    }

    static void Main(string[] args) {

      var k = Console.ReadLine()!;
      k = k[2..];

      int numerator, denominator;
      if (k.Length == 1 || k[0] != k[k.Length - 1]) {
        numerator = int.Parse(k);
        denominator = (int)Math.Pow(10, k.Length);
      } else {
        numerator = int.Parse(k);
        denominator = 0;
        for (int i = 0; i < k.Length; i++)
          denominator = (denominator * 10) + 9;
      }

      int commonDivisor = Gcd(numerator, denominator);
      numerator /= commonDivisor;
      denominator /= commonDivisor;

      Console.WriteLine("YES");
      Console.WriteLine($"{numerator} {denominator}");

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

int gcd(int a, int b) {
  if (b == 0) return a;
  return gcd(b, a % b);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string k; cin >> k;

  k = k.substr(2);

  int numerator, denominator;
  if (k.length() == 1 || k[0] != k[k.length()-1]) {
    numerator = stoi(k);
    denominator = pow(10, k.length());
  } else {
    numerator = stoi(k);
    denominator = 0;
    for (size_t i = 0; i < k.length(); i++)
      denominator = (denominator * 10) + 9;
  }

  int commonDivisor = gcd(numerator, denominator);
  numerator /= commonDivisor;
  denominator /= commonDivisor;

  cout << "YES\n";
  cout << numerator << " " << denominator << "\n";

  return 0;
}
  ```
