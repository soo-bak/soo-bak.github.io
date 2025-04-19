---
layout: single
title: "[백준 3049] 다각형의 대각선 (C#, C++) - soo:bak"
date: "2025-04-20 02:06:00 +0900"
description: 다각형의 꼭짓점 개수가 주어졌을 때 가능한 대각선의 개수를 조합을 통해 계산하는 백준 3049번 다각형의 대각선 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[3049번 - 다각형의 대각선](https://www.acmicpc.net/problem/3049)

## 설명
**정다각형의 꼭짓점 개수가 주어졌을 때, 이 중 네 개의 꼭짓점을 골라 만들 수 있는 사각형의 개수를 구하는 문제입니다.**
<br>

- 정다각형의 각 꼭짓점은 다른 꼭짓점들과 대각선을 이룰 수 있습니다.
- 문제에서 요구하는 **4개의 꼭짓점을 연결하여 만들 수 있는 모든 사각형의 개수**는 :<br>
  결국 **n개의 꼭짓점 중 4개를 선택하는 조합의 개수**, 즉

  $$
  \binom{n}{4} = \frac{n \times (n - 1) \times (n - 2) \times (n - 3)}{24}
  $$

  를 계산하는 문제입니다.

## 접근법

1. 꼭짓점의 개수를 입력받습니다.
2. $$n \geq 4$$일 때, 가능한 사각형의 수는 위 조합식을 그대로 계산하면 됩니다.
3. 계산 결과를 출력합니다.

- 시간 복잡도는 `O(1)`이며, 단순한 수학 계산만으로 해결됩니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    long res = (long)n * (n - 1) * (n - 2) * (n - 3) / 24;
    Console.WriteLine(res);
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

  int num; cin >> num;
  cout << num * (num - 1) * (num - 2) * (num - 3) / 24 << "\n";

  return 0;
}
```
