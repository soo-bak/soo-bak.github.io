---
layout: single
title: "[백준 4766] 일반 화학 실험 (C#, C++) - soo:bak"
date: "2025-04-20 22:43:00 +0900"
description: 연속된 온도 측정값들의 차이를 소수점 둘째 자리까지 출력하는 백준 4766번 일반 화학 실험 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 4766
  - C#
  - C++
  - 알고리즘
keywords: "백준 4766, 백준 4766번, BOJ 4766, temperatureDiff, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4766번 - 일반 화학 실험](https://www.acmicpc.net/problem/4766)

## 설명
**일정 시간 간격으로 측정한 온도 데이터들을을 입력받아,**<br>
**이전 온도와의 차이를 소수점 둘째 자리까지 출력하는 문제입니다.**
<br>

- 첫 번째 온도는 기준값으로 저장되며 출력하지 않습니다.
- 두 번째 값부터는 이전 값과의 차이를 구해 출력합니다.
- 입력은 `999`가 나올 때까지 계속되며, `999`는 종료 신호이므로 출력하지 않습니다.
- 출력은 소수점 둘째 자리까지 고정 형식으로 표시해야 합니다.


## 접근법

1. 첫 번째 실수형 값을 입력받아 이전 온도로 저장합니다.
2. 이후 반복문을 통해 현재 온도를 하나씩 입력받습니다.
3. 입력값이 `999`라면 종료하고, 아니라면 이전 온도와의 차이를 계산하여 출력합니다.
5. 현재 온도를 이전 온도로 갱신하며 다음 반복을 준비합니다.


## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    double prev = double.Parse(Console.ReadLine());

    while (true) {
      double now = double.Parse(Console.ReadLine());
      if (now == 999) break;

      Console.WriteLine((now - prev).ToString("F2"));
      prev = now;
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

  double prev; cin >> prev;
  while (true) {
    double now; cin >> now;
    if (now == 999) break;

    cout.setf(ios::fixed); cout.precision(2);
    cout << now - prev << "\n";
    prev = now;
  }

  return 0;
}
```
