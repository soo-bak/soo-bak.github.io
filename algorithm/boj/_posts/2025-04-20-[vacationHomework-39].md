---
layout: single
title: "[백준 5532] 방학 숙제 (C#, C++) - soo:bak"
date: "2025-04-20 18:21:00 +0900"
description: 국어와 수학 숙제를 하루 제한량씩 나누어 푼다고 할 때 방학 중 실제로 놀 수 있는 날짜를 계산하는 백준 5532번 방학 숙제 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5532
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 5532, 백준 5532번, BOJ 5532, vacationHomework, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5532번 - 방학 숙제](https://www.acmicpc.net/problem/5532)

## 설명
**방학 동안 해야 할 국어와 수학 숙제를 매일 일정량씩 푼다고 할 때,**<br>
**모든 숙제를 완료하고 남은 일수만큼 놀 수 있는 날짜를 구하는 문제입니다.**
<br>

- 총 방학 일수가 주어지고, 국어와 수학 각각의 숙제량, 하루에 풀 수 있는 양이 주어집니다.
- 숙제를 모두 끝낼 때까지는 매일 공부해야 하며,
- 국어와 수학 중 **더 오래 걸리는 과목을 기준으로** 숙제를 마치는 날이 정해집니다.
- 방학 총일수에서 숙제를 푸는 데 걸린 일수를 빼면 실제로 놀 수 있는 날이 됩니다.

## 접근법

1. 입력으로 다음의 값들을 차례로 입력받습니다:
   - 방학 전체 일수
   - 국어 총 숙제량
   - 수학 총 숙제량
   - 하루에 풀 수 있는 국어 양
   - 하루에 풀 수 있는 수학 양

2. 각 과목별로 숙제를 마치는 데 걸리는 날짜는 다음과 같이 계산합니다:<br>
   $$\left\lceil \frac{\text{총 숙제량}}{\text{하루 제한량}} \right\rceil$$<br>

   이 연산을 정수 연산으로 구현하면 다음과 같이 처리할 수 있습니다:<br>
   $$\left\lfloor \frac{\text{총 숙제량} + \text{하루 제한량} - 1}{\text{하루 제한량}} \right\rfloor$$<br>

3. 국어와 수학 중 더 오래 걸리는 쪽을 기준으로 숙제 기간을 정한 후,
4. 전체 방학 일수에서 숙제 일수를 빼면 남은 놀 수 있는 날짜가 됩니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int vacation = int.Parse(Console.ReadLine());
    int korean = int.Parse(Console.ReadLine());
    int math = int.Parse(Console.ReadLine());
    int perDayKorean = int.Parse(Console.ReadLine());
    int perDayMath = int.Parse(Console.ReadLine());

    int daysKorean = (korean + perDayKorean - 1) / perDayKorean;
    int daysMath = (math + perDayMath - 1) / perDayMath;
    int homeworkDays = Math.Max(daysKorean, daysMath);

    Console.WriteLine(vacation - homeworkDays);
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

  int v, l, m, pL, pM;
  cin >> v >> l >> m >> pL >> pM;

  int dL = (l + pL - 1) / pL;
  int dM = (m + pM - 1) / pM;
  cout << v - max(dL, dM) << "\n";

  return 0;
}
```
