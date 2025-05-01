---
layout: single
title: "[백준 2985] 세 수 (C#, C++) - soo:bak"
date: "2025-05-02 04:33:00 +0900"
description: 세 개의 정수로부터 사칙연산을 복원하는 백준 2985번 세 수 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[2985번 - 세 수](https://www.acmicpc.net/problem/2985)

## 설명
세 개의 정수가 주어졌을 때,

이들 사이에 하나의 사칙연산 기호와 등호를 적절히 배치하여 **올바른 등식 하나를 구성하는 문제**입니다.

<br>
등식의 형태는 다음 두 가지 중 하나입니다:

- 첫 번째와 두 번째 수 사이에 연산 기호를 넣고, 그 결과가 세 번째 수가 되는 경우
  (예: `a + b = c`)
- 두 번째와 세 번째 수 사이에 연산 기호를 넣고, 그 결과가 첫 번째 수가 되는 경우
  (예: `a = b * c`)

입력으로 주어진 세 정수의 순서를 바꾸지 않고, 조건을 만족하는 등식을 출력합니다.

<br>

## 접근법

- 세 정수를 입력받고, 가능한 연산 조합을 순서대로 검사합니다.
- 사칙연산(`+`, `-`, `*`, `/`)을 각각 적용한 결과가 나머지 값과 일치하는지 확인합니다.
- 앞에서부터 먼저 성립하는 등식을 찾고, 조건을 만족하면 즉시 출력합니다.
- 항상 정답이 존재하는 입력만 주어지므로, 하나의 등식을 출력하면 됩니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    int a = int.Parse(input[0]);
    int b = int.Parse(input[1]);
    int c = int.Parse(input[2]);

    if (a + b == c) Console.WriteLine($"{a}+{b}={c}");
    else if (a - b == c) Console.WriteLine($"{a}-{b}={c}");
    else if (a * b == c) Console.WriteLine($"{a}*{b}={c}");
    else if (a / b == c) Console.WriteLine($"{a}/{b}={c}");
    else if (a == b + c) Console.WriteLine($"{a}={b}+{c}");
    else if (a == b - c) Console.WriteLine($"{a}={b}-{c}");
    else if (a == b * c) Console.WriteLine($"{a}={b}*{c}");
    else if (a == b / c) Console.WriteLine($"{a}={b}/{c}");
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int a, b, c; cin >> a >> b >> c;

  if (a + b == c) cout << a << '+' << b << '=' << c;
  else if (a - b == c) cout << a << '-' << b << '=' << c;
  else if (a * b == c) cout << a << '*' << b << '=' << c;
  else if (a / b == c) cout << a << '/' << b << '=' << c;
  else if (a == b + c) cout << a << '=' << b << '+' << c;
  else if (a == b - c) cout << a << '=' << b << '-' << c;
  else if (a == b * c) cout << a << '=' << b << '*' << c;
  else if (a == b / c) cout << a << '=' << b << '/' << c;
  cout << "\n";

  return 0;
}
```
