---
layout: single
title: "[백준 10039] 평균 점수 (C#, C++) - soo:bak"
date: "2025-04-14 02:57:39 +0900"
description: 최소 점수 기준을 적용해 평균을 구하는 백준 10039번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10039
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 10039, 백준 10039번, BOJ 10039, averageScore, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10039번 - 평균 점수](https://www.acmicpc.net/problem/10039)

## 설명
이 문제는 5개의 시험 점수가 주어졌을 때, 각 점수가 `40점` 미만이면 `40점`으로 처리하고, <br>
그 후 평균 점수를 구하는 간단한 구현 문제입니다.

---

## 접근법
- 총 5개의 점수를 반복문으로 입력받습니다.
- 각 점수가 `40`보다 작으면 `40`으로 대체하여 합계에 누적합니다.
- 마지막에 누적된 총합을 `5`로 나누어 평균을 구합니다.

출력은 정수로 처리하며, 소수점은 버립니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var sum = 0;
      for (int i = 0; i < 5; i++) {
        var scr = int.Parse(Console.ReadLine()!);
        sum += scr < 40 ? 40 : scr;
      }
      Console.WriteLine(sum / 5);
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <iostream>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int sum = 0;
  for (int i = 0; i < 5; i++) {
    int scr; cin >> scr;
    if (scr < 40) sum += 40;
    else sum += scr;
  }
  cout << sum / 5 << "\n";

  return 0;
}
```
