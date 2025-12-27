---
layout: single
title: "[백준 1297] TV 크기 (C#, C++) - soo:bak"
date: "2025-04-19 04:20:32 +0900"
description: 대각선 길이와 종횡비를 바탕으로 TV의 실제 세로 및 가로 크기를 계산하는 기하학 문제인 백준 1297번 TV 크기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1297
  - C#
  - C++
  - 알고리즘
  - pythagoras
  - 기하학
keywords: "백준 1297, 백준 1297번, BOJ 1297, tvResolution, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1297번 - TV 크기](https://www.acmicpc.net/problem/1297)

## 설명
**TV의 대각선 길이와 비율(종횡비)을 바탕으로 실제 세로 및 가로 길이를 계산하는 문제**입니다.<br>
<br>

- TV의 대각선 길이 `D`와 종횡비 `H:W`가 주어집니다.<br>
- 실제 화면 크기는 세로 `H'`, 가로 `W'`로 주어져야 하며, <br>
  주어진 비율을 유지하면서도 $$H'^2 + W'^2 = D^2$$ 를 만족해야 합니다.<br>

### 접근법
- 입력으로 주어지는 종횡비 `H:W`는 **비례값**일 뿐, 실제 길이는 아니므로<br>
  피타고라스 정리를 통해 **비례 상수**를 곱해 실제 길이를 계산해야 합니다.<br>
- 삼각형에서 대각선 `D`, 종횡비 `h:w`를 생각하면 다음이 성립합니다:<br>

  $$\text{scale} = \frac{D}{\sqrt{h^2 + w^2}}$$

- 이 비례 상수를 곱해서 실제 세로, 가로 길이를 구합니다:<br>

  $$
  H' = \left\lfloor h \times \text{scale} \right\rfloor,\quad
  W' = \left\lfloor w \times \text{scale} \right\rfloor
  $$

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    double d = double.Parse(input[0]);
    double h = double.Parse(input[1]);
    double w = double.Parse(input[2]);

    double scale = d / Math.Sqrt(h * h + w * w);
    int ansH = (int)(h * scale);
    int ansW = (int)(w * scale);

    Console.WriteLine($"{ansH} {ansW}");
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

  double d, h, w; cin >> d >> h >> w;
  double ratio = sqrt(h * h + w * w);

  int ansH = h * d / ratio, ansW = w * d / ratio;
  cout << ansH << " " << ansW << "\n";

  return 0;
}
```
