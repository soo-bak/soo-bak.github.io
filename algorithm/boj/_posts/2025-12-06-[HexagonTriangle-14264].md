---
layout: single
title: "[백준 14264] 정육각형과 삼각형 (C#, C++) - soo:bak"
date: "2025-12-06 23:30:00 +0900"
description: 정육각형을 대각선으로 나눌 때 가장 작은 삼각형 넓이의 최댓값을 구하는 백준 14264번 정육각형과 삼각형 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[14264번 - 정육각형과 삼각형](https://www.acmicpc.net/problem/14264)

## 설명
한 변의 길이가 L인 정육각형을 서로 겹치지 않는 대각선 3개로 4개의 삼각형으로 나눕니다.

이때 가장 작은 삼각형의 넓이를 최대화하는 문제입니다.

<br>

## 접근법
정육각형의 대각선을 적절히 이으면 4개의 삼각형을 모두 한 변이 L인 정삼각형으로 만들 수 있습니다. 이것이 가장 작은 삼각형의 넓이를 최대화하는 최적의 구성입니다.

따라서 정답은 한 변이 L인 정삼각형의 넓이인 루트3 나누기 4 곱하기 L 제곱입니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var L = double.Parse(Console.ReadLine()!);
      var area = L * L * Math.Sqrt(3) / 4.0;
      Console.WriteLine(area.ToString("0.000000000"));
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

  double L; cin >> L;
  double area = L * L * sqrt(3.0) / 4.0;

  cout << fixed << setprecision(9) << area << "\n";

  return 0;
}
```
