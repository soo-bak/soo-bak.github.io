---
layout: single
title: "[백준 16864] So You Like Your Food Hot? (C#, C++) - soo:bak"
date: "2026-04-19 20:44:00 +0900"
description: "백준 16864번 C#, C++ 풀이 - 총이익을 센트 단위 정수로 바꾼 뒤 피타와 피자 개수 조합을 찾는 문제"
tags:
  - 백준
  - BOJ
  - 16864
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
keywords: "백준 16864, 백준 16864번, BOJ 16864, So You Like Your Food Hot, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16864번 - So You Like Your Food Hot?](https://www.acmicpc.net/problem/16864)

## 설명
한 달 총이익과 피타, 피자의 개당 이익이 주어질 때, 가능한 판매 개수 조합을 모두 찾는 문제입니다.

<br>

## 접근법
금액은 모두 달러와 센트로 주어지므로, 먼저 센트 단위 정수로 바꾸면 계산이 깔끔해집니다.

피타를 `a`개 팔았다고 하면 남는 금액은 `총이익 - a × 피타이익`입니다. 이 값이 음수가 아니고 피자 이익으로 나누어떨어지면, 그때의 피자 개수도 정수로 정해집니다.

피타 개수를 `0`부터 가능한 최대 개수까지 오름차순으로 확인하면, 출력 순서도 문제에서 요구한 그대로 맞출 수 있습니다. 가능한 조합이 하나도 없으면 `none`을 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Globalization;
using System.Text;

class Program {
  static void Main() {
    string[] input = Console.ReadLine()!.Split();
    long total = ToCents(input[0]);
    long pita = ToCents(input[1]);
    long pizza = ToCents(input[2]);

    var sb = new StringBuilder();
    bool found = false;

    for (long pitas = 0; pitas * pita <= total; pitas++) {
      long remain = total - pitas * pita;
      if (remain % pizza == 0) {
        long pizzas = remain / pizza;
        sb.Append(pitas).Append(' ').Append(pizzas).Append('\n');
        found = true;
      }
    }

    if (found)
      Console.Write(sb.ToString());
    else
      Console.WriteLine("none");
  }

  static long ToCents(string s) {
    decimal value = decimal.Parse(s, CultureInfo.InvariantCulture);
    return (long)(value * 100m);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

long long toCents(const string& s) {
  size_t pos = s.find('.');
  if (pos == string::npos) {
    return stoll(s) * 100;
  }

  string dollars = s.substr(0, pos);
  string cents = s.substr(pos + 1);
  while ((int)cents.size() < 2) {
    cents += '0';
  }

  return stoll(dollars) * 100 + stoll(cents.substr(0, 2));
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string totalStr, pitaStr, pizzaStr;
  cin >> totalStr >> pitaStr >> pizzaStr;

  long long total = toCents(totalStr);
  long long pita = toCents(pitaStr);
  long long pizza = toCents(pizzaStr);

  bool found = false;

  for (long long pitas = 0; pitas * pita <= total; pitas++) {
    long long remain = total - pitas * pita;
    if (remain % pizza == 0) {
      long long pizzas = remain / pizza;
      cout << pitas << " " << pizzas << "\n";
      found = true;
    }
  }

  if (!found) {
    cout << "none\n";
  }

  return 0;
}
```
