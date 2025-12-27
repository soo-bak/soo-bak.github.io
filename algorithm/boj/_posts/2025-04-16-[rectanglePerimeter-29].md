---
layout: single
title: "[백준 32171] 울타리 공사 (C#, C++) - soo:bak"
date: "2025-04-16 02:13:00 +0900"
description: 여러 개의 직사각형을 포함하는 가장 작은 외곽 사각형의 둘레를 계산하는 백준 32171번 울타리 공사 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 32171
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 기하학
  - arithmetic
keywords: "백준 32171, 백준 32171번, BOJ 32171, rectanglePerimeter, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32171번 - 울타리 공사](https://www.acmicpc.net/problem/32171)

## 설명
**여러 개의 직사각형을 모두 포함할 수 있는 가장 작은 직사각형의 둘레를 계산하는 문제**입니다.<br>
<br>

- 입력으로 여러 개의 직사각형 좌표가 주어집니다.<br>
- 각 직사각형은 좌측 하단 꼭짓점과 우측 상단 꼭짓점의 좌표로 표현됩니다.<br>
- 이 모든 직사각형을 완전히 감싸는 가장 작은 직사각형을 만들고,<br>
- 그 둘레를 계산하면 됩니다.<br>

### 접근법
- 입력으로 들어오는 모든 직사각형을 읽으면서<br>
  - 전체 직사각형을 감싸기 위한 최소 x좌표, 최소 y좌표를 갱신하고<br>
  - 최대 x좌표, 최대 y좌표도 계속 갱신합니다.<br>
- 모든 입력이 끝난 후, 감싸는 직사각형의 세로 길이는 `최댓값 y - 최솟값 y`, 가로 길이는 `최댓값 x - 최솟값 x`가 됩니다.<br>
- 둘레는 다음 공식으로 계산합니다:<br>
  $$2 \times (가로 + 세로)$$<br>
- 각 테스트마다 결과를 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var minX = 10;
    var minY = 10;
    var maxX = -10;
    var maxY = -10;

    var n = int.Parse(Console.ReadLine());
    while (n-- > 0) {
      var input = Console.ReadLine().Split();
      var x1 = int.Parse(input[0]);
      var y1 = int.Parse(input[1]);
      var x2 = int.Parse(input[2]);
      var y2 = int.Parse(input[3]);

      minX = Math.Min(minX, x1);
      minY = Math.Min(minY, y1);
      maxX = Math.Max(maxX, x2);
      maxY = Math.Max(maxY, y2);

      var perimeter = 2 * ((maxY - minY) + (maxX - minX));
      Console.WriteLine(perimeter);
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

  int minX = 10, minY = 10, maxX = -10, maxY = -10;

  int n; cin >> n;
  while (n--) {
    int x1, y1, x2, y2; cin >> x1 >> y1 >> x2 >> y2;

    minX = min(x1, minX);
    minY = min(y1, minY);
    maxX = max(x2, maxX);
    maxY = max(y2, maxY);

    cout << 2 * ((maxY - minY) + (maxX - minX)) << "\n";
  }

  return 0;
}
```
