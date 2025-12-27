---
layout: single
title: "[백준 16486] 운동장 한 바퀴 (C#, C++) - soo:bak"
date: "2025-04-16 02:06:00 +0900"
description: 반원과 직선 구간으로 이루어진 운동장의 둘레를 계산하는 백준 16486번 운동장 한 바퀴 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 16486
  - C#
  - C++
  - 알고리즘
  - 수학
  - 기하학
keywords: "백준 16486, 백준 16486번, BOJ 16486, runningTrack, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16486번 - 운동장 한 바퀴](https://www.acmicpc.net/problem/16486)

## 설명
**운동장의 구조를 고려해 총 둘레를 계산하는 문제**입니다.<br>
<br>

- 운동장은 두 개의 직선 구간과 두 개의 반원으로 구성된 타원형 형태입니다.<br>
- 입력으로는 `직선 구간의 길이`와 `반지름`이 주어집니다.<br>
- 전체 둘레는 다음과 같이 계산할 수 있습니다:<br>
  - 직선 구간: `2 * 직선 구간의 길이`<br>
  - 반원 2개를 합치면 전체 원이 되므로 `2 * π * 반지름`<br>
  - 총합: `2 * 직선 구간의 길이 + 2 * π * 반지름`<br>

### 접근법
- `직선 구간의 길이`와 `반지름`을 입력받고, 위 수식대로 계산하면 됩니다.<br>
- 소수점 아래 `6`자리까지 출력해야 하므로, 출력 형식에 유의합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var w = int.Parse(Console.ReadLine());
    var r = int.Parse(Console.ReadLine());

    const double PI = 3.141592;
    var ans = 2 * w + 2 * PI * r;
    Console.WriteLine($"{ans:F6}");
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>
#define PI 3.141592

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int w, r; cin >> w >> r;
  double ans = 2 * w + 2 * PI * r;
  cout.setf(ios::fixed); cout.precision(6);
  cout << ans << "\n";

  return 0;
}
```
