---
layout: single
title: "[백준 23795] 사장님 도박은 재미로 하셔야 합니다 (C#, C++) - soo:bak"
date: "2025-11-21 23:27:00 +0900"
description: -1이 나올 때까지 입력된 금액을 더해 총 손실을 구하는 백준 23795번 사장님 도박은 재미로 하셔야 합니다 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[23795번 - 사장님 도박은 재미로 하셔야 합니다](https://www.acmicpc.net/problem/23795)

## 설명

도박으로 잃은 금액이 한 줄에 하나씩 입력됩니다. 입력은 `-1`이 나올 때까지 계속됩니다.<br>

총 손실 금액을 계산하여 출력하는 문제입니다.<br>

<br>

## 접근법

입력된 금액을 순서대로 읽으며 누적합니다. `-1`이 입력되면 반복을 종료하고 누적한 합을 출력합니다.

예를 들어 `100`, `200`, `50`, `-1`이 차례로 입력되면 `350`을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {

      var sum = 0;
      while (true) {
        var line = Console.ReadLine();
        if (line == null) break;

        var value = int.Parse(line);
        if (value == -1) break;

        sum += value;
      }

      Console.WriteLine(sum);
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

  int sum = 0;
  while (true) {
    int value; cin >> value;

    if (value == -1) break;

    sum += value;
  }

  cout << sum << "\n";

  return 0;
}
```

