---
layout: single
title: "[백준 6322] 직각 삼각형의 두 변 (C#, C++) - soo:bak"
date: "2025-11-30 01:48:00 +0900"
description: 세 변 중 하나가 비어 있는 직각삼각형에서 피타고라스 법칙으로 나머지 한 변을 구하거나 불가능을 판정하는 백준 6322번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 6322
  - C#
  - C++
  - 알고리즘
keywords: "백준 6322, 백준 6322번, BOJ 6322, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6322번 - 직각 삼각형의 두 변](https://www.acmicpc.net/problem/6322)

## 설명

여러 개의 테스트 케이스가 주어지는 상황에서, 각 케이스마다 직각삼각형의 세 변 길이 a, b, c (c는 빗변) 중 하나가 -1로 주어질 때, 피타고라스 정리를 이용하여 누락된 변의 길이를 구하는 문제입니다.

세 변의 길이는 양의 정수이며, 누락된 변을 계산했을 때 삼각형이 성립하지 않으면 "Impossible."을 출력합니다. 모든 입력 값이 0이 되면 종료합니다.

<br>

## 접근법

피타고라스 정리 `a² + b² = c²`를 사용하여 누락된 변을 계산합니다.

<br>
누락된 변이 빗변 c인 경우, `c = √(a² + b²)`로 계산합니다.

계산된 c가 삼각형의 변으로 유효하려면 삼각형 부등식을 만족해야 하므로 `c < a + b`를 확인합니다. 제곱근 안의 값이 음수거나 계산 결과가 NaN이면 불가능합니다.

<br>
빗변 c가 주어지고 a 또는 b가 누락된 경우, `변 = √(c² - 다른변²)`로 계산합니다.

예를 들어 b가 누락되었다면 `b = √(c² - a²)`입니다. 계산된 변이 유효하려면 `변 + 다른변 > c`를 만족해야 합니다. c² - 다른변²이 음수거나 계산 결과가 NaN이면 불가능합니다.

<br>
각 테스트 케이스마다 "Triangle #번호"를 출력하고, 누락된 변을 "변 = 값" 형식으로 소수점 셋째 자리까지 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Globalization;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      Console.OutputEncoding = System.Text.Encoding.UTF8;
      var tc = 1;
      
      while (true) {
        var parts = Console.ReadLine()!.Split();
        var a = double.Parse(parts[0], CultureInfo.InvariantCulture);
        var b = double.Parse(parts[1], CultureInfo.InvariantCulture);
        var c = double.Parse(parts[2], CultureInfo.InvariantCulture);
        if (a == 0 && b == 0 && c == 0) break;

        Console.WriteLine($"Triangle #{tc}");
        var ok = true;
        var missing = ' ';
        var ans = 0.0;

        if (c == -1) {
          missing = 'c';
          ans = Math.Sqrt(a * a + b * b);
          if (ans >= a + b || double.IsNaN(ans)) ok = false;
        } else if (b == -1) {
          missing = 'b';
          ans = Math.Sqrt(c * c - a * a);
          if (ans + a <= c || double.IsNaN(ans)) ok = false;
        } else {
          missing = 'a';
          ans = Math.Sqrt(c * c - b * b);
          if (ans + b <= c || double.IsNaN(ans)) ok = false;
        }

        if (ok) Console.WriteLine($"{missing} = {ans:F3}");
        else Console.WriteLine("Impossible.");
        Console.WriteLine();
        tc++;
      }
    }
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

  cout.setf(ios::fixed);
  cout.precision(3);
  
  int tc = 1;
  while (true) {
    double a, b, c;
    cin >> a >> b >> c;
    if (a == 0 && b == 0 && c == 0) break;

    cout << "Triangle #" << tc << "\n";
    bool ok = true;
    char miss;
    double ans = 0;

    if (c == -1) {
      miss = 'c';
      ans = sqrt(a * a + b * b);
      if (ans >= a + b || isnan(ans)) ok = false;
    } else if (b == -1) {
      miss = 'b';
      ans = sqrt(c * c - a * a);
      if (ans + a <= c || isnan(ans)) ok = false;
    } else {
      miss = 'a';
      ans = sqrt(c * c - b * b);
      if (ans + b <= c || isnan(ans)) ok = false;
    }

    if (ok) cout << miss << " = " << ans << "\n";
    else cout << "Impossible.\n";
    cout << "\n";
    tc++;
  }
  
  return 0;
}
```


