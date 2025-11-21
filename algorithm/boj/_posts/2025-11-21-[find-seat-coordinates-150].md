---
layout: single
title: "[백준 17388 변형?] 나는 행복합니다~ (C#, C++) - soo:bak"
date: "2025-11-21 23:27:00 +0900"
description: K번째 좌석 번호를 N×M 격자 좌표로 바꾸는 방식으로 잃어버린 좌석을 찾는 \"나는 행복합니다~\" 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[나는 행복합니다~ 문제 링크](https://www.acmicpc.net/problem/17388)

## 설명

관중석이 N행 M열 격자로 배치되어 있으며, 각 좌석은 0번부터 시작하는 번호가 순서대로 매겨져 있습니다.

번호는 첫 번째 행부터 순서대로 왼쪽에서 오른쪽으로 매겨집니다.

좌석 번호 K가 주어질 때, 해당 좌석이 몇 행 몇 열에 위치하는지 구해야 합니다. 행과 열은 모두 0부터 시작합니다.

<br>

## 접근법

K번 좌석은 0부터 시작하는 일련번호이므로, M개씩 묶인 행 단위로 나누어 계산할 수 있습니다.

K를 M으로 나눈 몫이 행 번호가 되고, 나머지가 열 번호가 됩니다.

예를 들어 M이 5이고 K가 12라면, 12를 5로 나눈 몫은 2, 나머지는 2이므로 2행 2열입니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var input = Console.ReadLine()!.Split();
      var n = int.Parse(input[0]);
      var m = int.Parse(input[1]);
      var k = int.Parse(input[2]);

      var row = k / m;
      var col = k % m;

      Console.WriteLine($"{row} {col}");
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

  int N, M, K; cin >> N >> M >> K;

  cout << (K / M) << " " << (K % M) << "\n";

  return 0;
}
```

