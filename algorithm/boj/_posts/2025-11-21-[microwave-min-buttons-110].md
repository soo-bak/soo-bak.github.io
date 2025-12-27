---
layout: single
title: "[백준 10162] 전자레인지 (C#, C++) - soo:bak"
date: "2025-11-21 23:33:00 +0900"
description: 300초, 60초, 10초 버튼을 큰 단위부터 사용해 최소 버튼 횟수를 구하는 백준 10162번 전자레인지 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10162
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 그리디
keywords: "백준 10162, 백준 10162번, BOJ 10162, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10162번 - 전자레인지](https://www.acmicpc.net/problem/10162)

## 설명

전자레인지에는 세 개의 시간 설정 버튼이 있습니다.<br>

`A` 버튼은 `300`초, `B` 버튼은 `60`초, `C` 버튼은 `10`초를 추가합니다.<br>

주어진 시간 `T`초를 정확히 맞추면서 버튼을 누르는 최소 횟수를 구해야 합니다.<br>

가장 작은 단위가 `10`초이므로 `T`가 `10`의 배수가 아니면 정확히 맞출 수 없습니다. 이 경우 `-1`을 출력합니다.<br>

<br>

## 접근법

큰 단위 버튼부터 사용하면 버튼을 누르는 총 횟수가 줄어들기 때문에, 그리디 방식을 적용하여 문제를 해결합니다.

예를들어 `100`초를 만드는 경우, `10`초 버튼 `10`번보다 `60`초 버튼 `1`번과 `10`초 버튼 `4`번(`5`번)이 더 효율적입니다.<br>

<br>
먼저 `T`가 `10`의 배수인지 확인합니다.

`10`의 배수가 아니면 정확히 맞출 수 없으므로 `-1`을 출력합니다.<br>

`T`를 `300`으로 나눈 몫이 `A` 버튼 횟수이고, 나머지를 `60`으로 나눈 몫이 `B` 버튼 횟수입니다.

마지막 남은 시간을 `10`으로 나눈 몫이 `C` 버튼 횟수입니다.<br>

세 버튼의 사용 횟수를 순서대로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var t = int.Parse(Console.ReadLine()!);

      if (t % 10 != 0) {
        Console.WriteLine(-1);
        return;
      }

      var countA = t / 300;
      t %= 300;
      var countB = t / 60;
      t %= 60;
      var countC = t / 10;

      Console.WriteLine($"{countA} {countB} {countC}");
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

  int t; cin >> t;

  if (t % 10 != 0) {
    cout << -1 << "\n";
    return 0;
  }

  int countA = t / 300;
  t %= 300;
  int countB = t / 60;
  t %= 60;
  int countC = t / 10;

  cout << countA << " " << countB << " " << countC << "\n";

  return 0;
}
```

