---
layout: single
title: "[백준 3034] 앵그리 창영이 (C#, C++) - soo:bak"
date: "2025-04-20 22:12:00 +0900"
description: 직각삼각형의 대각선을 이용해 성냥개비가 박스 안에 들어갈 수 있는지를 판별하는 백준 3034번 앵그리 창영이 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 3034
  - C#
  - C++
  - 알고리즘
  - 수학
  - 기하학
  - pythagoras
keywords: "백준 3034, 백준 3034번, BOJ 3034, angryChangYoung, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3034번 - 앵그리 창영이](https://www.acmicpc.net/problem/3034)

## 설명
**성냥개비가 직사각형 박스 안에 들어갈 수 있는지를 판단하는 문제입니다.**
<br>

- 박스는 너비와 높이를 가지는 직사각형입니다.
- 성냥개비는 회전이 가능하며, 박스에 대각선 방향으로 들어갈 수 있다면 적절한 방향으로 넣을 수 있습니다.
- 따라서 성냥개비의 길이가 박스의 **대각선 길이 이하**이면 박스 안에 들어갈 수 있습니다.
- 각 성냥개비에 대해 결과를 판별하고, 가능하면 `DA`를, 불가능하면 `NE`를 출력합니다.

## 접근법

1. 입력으로 다음 정보를 차례로 입력받습니다:
   - 성냥개비 개수
   - 박스의 너비
   - 박스의 높이

2. 먼저 박스의 대각선 길이를 구합니다.
   이는 피타고라스의 정리에 의해 다음과 같이 계산됩니다:

  $$
  \text{대각선 길이} = \sqrt{(\text{너비})^2 + (\text{높이})^2}
  $$

3. 각 성냥개비의 길이를 입력받아, 박스의 대각선보다 짧거나 같다면 `DA`, 그렇지 않으면 `NE`를 출력합니다.

- `sqrt`를 사용하는 대신, 제곱값으로 비교하면 오차 없이 처리할 수도 있습니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    int count = int.Parse(input[0]);
    int width = int.Parse(input[1]);
    int height = int.Parse(input[2]);

    double maxLen = Math.Sqrt(width * width + height * height);

    for (int i = 0; i < count; i++) {
      int match = int.Parse(Console.ReadLine());
      Console.WriteLine(match <= maxLen ? "DA" : "NE");
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

  int cntMatch, widthBox, lengthBox;
  cin >> cntMatch >> widthBox >> lengthBox;

  int availSize = sqrt(widthBox * widthBox + lengthBox * lengthBox);
  for (int i = 0; i < cntMatch; i++) {
    int sizeMatch; cin >> sizeMatch;
    if (sizeMatch > availSize) cout << "NE\n";
    else cout << "DA\n";
  }

  return 0;
}
```
