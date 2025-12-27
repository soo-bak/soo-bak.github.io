---
layout: single
title: "[백준 2506] 점수계산 (C#, C++) - soo:bak"
date: "2025-04-14 07:27:30 +0900"
description: 연속된 정답 보너스 점수를 계산하는 백준 2506번 점수계산 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2506
  - C#
  - C++
  - 알고리즘
keywords: "백준 2506, 백준 2506번, BOJ 2506, scoreAccumulation, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2506번 - 점수계산](https://www.acmicpc.net/problem/2506)

## 설명
이 문제는 OX 퀴즈 채점 결과가 주어졌을 때,  <br>
**연속된 정답에 대해 점수를 누적해서 계산하는 문제**입니다.

---

## 접근법
- 각 정답에 대해:
  - 정답이면 누적 보너스 점수를 증가시키고 점수에 더합니다.
  - 오답이면 누적 보너스 점수를 다시 `1`로 초기화합니다.
- 최종 누적 점수를 출력하면 됩니다.

<br>
> 참고 : [누적합(Prefix Sum)의 원리와 구간 합 계산 - soo:bak](https://soo-bak.github.io/algorithm/theory/prefix-sum/)

<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int num = int.Parse(Console.ReadLine()!);
      var input = Console.ReadLine()!.Split().Select(int.Parse);

      int sum = 0, seq = 1;
      foreach (var res in input) {
        if (res == 1) {
          sum += seq;
          seq++;
        } else seq = 1;
      }

      Console.WriteLine(sum);
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int numQ; cin >> numQ;
  int sum = 0, seq = 1;
  for (int i = 0; i < numQ; i++) {
    bool isRight; cin >> isRight;
    if (isRight) {
      sum += seq;
      seq++;
    } else seq = 1;
  }

  cout << sum << "\n";

  return 0;
}
```
