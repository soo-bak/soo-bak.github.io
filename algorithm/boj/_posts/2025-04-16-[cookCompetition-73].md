---
layout: single
title: "[백준 2953] 나는 요리사다 (C#, C++) - soo:bak"
date: "2025-04-16 02:18:00 +0900"
description: 다섯 명의 참가자 중 점수 합이 가장 높은 사람을 구하는 백준 2953번 나는 요리사다 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2953
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 2953, 백준 2953번, BOJ 2953, cookCompetition, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2953번 - 나는 요리사다](https://www.acmicpc.net/problem/2953)

## 설명
**다섯 명의 참가자 중 네 개의 점수 합이 가장 높은 참가자를 찾아 출력하는 문제**입니다.<br>
<br>

- 각 참가자는 네 개의 점수를 입력받습니다.<br>
- 총 다섯 명의 참가자가 있으며, 각 참가자마다 총점을 계산한 후 가장 큰 총점을 가진 사람을 찾아야 합니다.<br>
- 참가자의 번호는 `1`번부터 `5`번까지입니다.<br>

### 접근법
- 총 `5`번 반복하면서 각 참가자의 점수를 누적합산합니다.<br>
- 현재까지의 최고 점수보다 높은 경우, 최고 점수와 해당 참가자 번호를 갱신합니다.<br>
- 최종적으로 최고 점수를 받은 참가자의 번호와 점수를 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int max = 0, winner = 0;
    for (int i = 0; i < 5; i++) {
      var input = Console.ReadLine().Split();
      int sum = 0;
      foreach (var str in input)
        sum += int.Parse(str);

      if (sum > max) {
        max = sum;
        winner = i + 1;
      }
    }
    Console.WriteLine($"{winner} {max}");
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

  int max = 0, idx = 0;
  for (int i = 0; i < 5; i++) {
    int sum = 0;
    for (int j = 0; j < 4; j++) {
      int input; cin >> input;
      sum += input;
    }
    if (sum > max) {
      max = sum;
      idx = i;
    }
  }

  cout << idx + 1 << " " << max << "\n";

  return 0;
}
```
