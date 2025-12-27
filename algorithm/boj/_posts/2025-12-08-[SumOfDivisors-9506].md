---
layout: single
title: "[백준 9506] 약수들의 합 (C#, C++) - soo:bak"
date: "2025-12-08 04:20:00 +0900"
description: 완전수 여부를 판별하고 약수 합 표현을 출력하는 백준 9506번 약수들의 합 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 9506
  - C#
  - C++
  - 알고리즘
keywords: "백준 9506, 백준 9506번, BOJ 9506, SumOfDivisors, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9506번 - 약수들의 합](https://www.acmicpc.net/problem/9506)

## 설명
자연수가 주어질 때, 그 수가 완전수인지 판별하는 문제입니다. 완전수란 자기 자신을 제외한 약수들의 합이 자기 자신과 같은 수입니다. 예를 들어 6은 1 + 2 + 3 = 6이므로 완전수입니다.

<br>

## 접근법
1부터 n의 절반까지 확인하면서 약수를 모두 찾고 합을 구합니다. 합이 n과 같으면 완전수이므로 약수들을 더하기 형태로 출력하고, 다르면 완전수가 아니라고 출력합니다. -1이 입력될 때까지 반복합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    while (true) {
      var n = int.Parse(Console.ReadLine()!);
      if (n == -1) break;
      var v = new List<int>();
      var ans = 0;
      for (var i = 1; i < n; i++) {
        if (n % i == 0) { v.Add(i); ans += i; }
      }
      if (ans != n) {
        Console.WriteLine($"{n} is NOT perfect.");
      } else {
        Console.Write($"{n} = ");
        for (var i = 0; i < v.Count; i++) {
          Console.Write(v[i]);
          if (i == v.Count - 1) Console.WriteLine();
          else Console.Write(" + ");
        }
      }
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  while (true) {
    int n; cin >> n;
    if (n == -1) break;
    vi v;
    int ans = 0;
    for (int i = 1; i < n; i++) {
      if (!(n % i)) { v.push_back(i); ans += i; }
    }
    if (ans != n) {
      cout << n << " is NOT perfect.\n";
    } else {
      cout << n << " = ";
      for (auto i : v) {
        cout << i;
        if (i == *(v.end() - 1)) cout << "\n";
        else cout << " + ";
      }
    }
  }

  return 0;
}
```
