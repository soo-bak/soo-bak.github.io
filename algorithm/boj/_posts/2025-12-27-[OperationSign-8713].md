---
layout: single
title: "[백준 8713] Znak działania (C#, C++) - soo:bak"
date: "2025-12-27 05:45:00 +0900"
description: 두 정수 사이에 +, -, * 중 최댓값을 만드는 연산을 선택하는 문제
---

## 문제 링크
[8713번 - Znak działania](https://www.acmicpc.net/problem/8713)

## 설명
두 정수 a, b에 대해 +, -, * 중 결과가 가장 큰 연산을 골라 식을 출력합니다. 최대값을 만드는 연산이 여러 개면 "NIE"를 출력합니다.

음수는 괄호로 감싸서 출력합니다.

<br>

## 접근법
덧셈, 뺄셈, 곱셈 결과를 각각 계산합니다. 세 값 중 두 개 이상이 같으면 NIE, 아니면 가장 큰 값에 해당하는 연산으로 식을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static string Format(int n) => n < 0 ? $"({n})" : n.ToString();

  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = int.Parse(parts[0]);
    var b = int.Parse(parts[1]);

    var sum = a + b;
    var diff = a - b;
    var prod = a * b;

    if (sum == diff || sum == prod || diff == prod) Console.WriteLine("NIE");
    else if (sum >= diff && sum >= prod) Console.WriteLine($"{Format(a)}+{Format(b)}={Format(sum)}");
    else if (diff >= sum && diff >= prod) Console.WriteLine($"{Format(a)}-{Format(b)}={Format(diff)}");
    else Console.WriteLine($"{Format(a)}*{Format(b)}={Format(prod)}");
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

string format(int n) {
  return n < 0 ? '(' + to_string(n) + ')' : to_string(n);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int a, b; cin >> a >> b;

  int sum = a + b, diff = a - b, prod = a * b;

  if (sum == diff || sum == prod || diff == prod) cout << "NIE";
  else if (sum >= diff && sum >= prod) cout << format(a) << "+" << format(b) << "=" << format(sum);
  else if (diff >= sum && diff >= prod) cout << format(a) << "-" << format(b) << "=" << format(diff);
  else cout << format(a) << "*" << format(b) << "=" << format(prod);

  return 0;
}
```
