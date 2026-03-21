---
layout: single
title: "[백준 6627] The Easiest Problem is This One (C#, C++) - soo:bak"
date: "2026-03-21 21:43:00 +0900"
description: "백준 6627번 C#, C++ 풀이 - N에 10보다 큰 수를 곱해 자리수 합이 다시 같아지는 가장 작은 값을 찾는 문제"
tags:
  - 백준
  - BOJ
  - 6627
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 6627, 백준 6627번, BOJ 6627, The Easiest Problem is This One, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6627번 - The Easiest Problem is This One](https://www.acmicpc.net/problem/6627)

## 설명
양의 정수 `N`이 주어질 때, `p > 10`인 수 중에서 `S(N) = S(N x p)`를 만족하는 가장 작은 `p`를 찾는 문제입니다. 여기서 `S(x)`는 각 자리 숫자의 합입니다.

<br>

## 접근법
먼저 `N`의 자리수 합을 구해 둡니다.

그 다음 `p = 11`부터 하나씩 증가시키면서 `N x p`의 자리수 합을 계산합니다. 처음으로 원래 자리수 합과 같아지는 `p`가 정답입니다.

입력 범위가 크지 않고, 문제 자체도 이 과정을 그대로 구현하면 되는 형태이므로 단순 반복으로 충분합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static int DigitSum(long x) {
    int sum = 0;
    while (x > 0) {
      sum += (int)(x % 10);
      x /= 10;
    }
    return sum;
  }

  static void Main() {
    var sb = new StringBuilder();

    while (true) {
      long n = long.Parse(Console.ReadLine()!);
      if (n == 0)
        break;

      int target = DigitSum(n);
      int p = 11;

      while (true) {
        if (DigitSum(n * p) == target) {
          sb.AppendLine(p.ToString());
          break;
        }
        p++;
      }
    }

    Console.Write(sb.ToString());
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int digitSum(long long x) {
  int sum = 0;
  while (x > 0) {
    sum += (int)(x % 10);
    x /= 10;
  }
  return sum;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  long long n;
  while (cin >> n && n != 0) {
    int target = digitSum(n);
    int p = 11;

    while (true) {
      if (digitSum(n * p) == target) {
        cout << p << "\n";
        break;
      }
      p++;
    }
  }

  return 0;
}
```
