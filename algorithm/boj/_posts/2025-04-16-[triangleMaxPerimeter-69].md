---
layout: single
title: "[백준 14215] 세 막대 (C#, C++) - soo:bak"
date: "2025-04-16 02:04:00 +0900"
description: 삼각형을 만들 수 없는 경우 가장 긴 변을 줄여 최대 둘레를 만드는 문제인 백준 14215번 세 막대 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 14215
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 기하학
keywords: "백준 14215, 백준 14215번, BOJ 14215, triangleMaxPerimeter, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14215번 - 세 막대](https://www.acmicpc.net/problem/14215)

## 설명
삼각형의 성립조건(삼각부등식) 과 관련하여, **세 막대를 이용해 삼각형을 만들 수 있는 최대 둘레를 구하는 문제**입니다.<br>
<br>

- 막대 세 개의 길이가 주어집니다.<br>
- 이 막대로 삼각형을 만들기 위해서는 **가장 긴 막대의 길이가 나머지 두 막대 길이의 합보다 작아야 합니다.**<br>
- 조건을 만족하지 않으면 삼각형이 만들어지지 않습니다.<br>
- 이때 **가장 긴 막대의 길이를 줄여서 삼각형 조건을 만족시키는 최대 둘레**를 구해야 합니다.<br>

### 접근법
- 세 막대의 길이를 입력받아 오름차순 정렬합니다.<br>
- 가장 긴 막대의 길이가 나머지 둘의 합보다 크거나 같다면, 삼각형이 되지 않으므로<br>
  - 가장 긴 막대를 `나머지 두 개의 합 - 1`까지 줄여야 합니다.<br>
- 최종적으로 세 막대 길이의 합을 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var side = Console.ReadLine().Split().Select(int.Parse).ToArray();
    Array.Sort(side);
    while (side[2] >= side[0] + side[1]) side[2]--;
    Console.WriteLine(side.Sum());
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

  int side[3];
  for (int i = 0; i < 3; i++)
    cin >> side[i];

  sort(side, side + 3);

  while (side[2] >= side[0] + side[1])
    side[2]--;

  cout << side[0] + side[1] + side[2] << "\n";

  return 0;
}
```
