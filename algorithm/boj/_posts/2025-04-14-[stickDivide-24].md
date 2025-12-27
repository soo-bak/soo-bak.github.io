---
layout: single
title: "[백준 1094] 막대기 (C#, C++) - soo:bak"
date: "2025-04-14 04:20:37 +0900"
description: 자른 막대 조각의 합으로 목표 길이를 만드는 최소 개수를 구하는 백준 1094번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1094
  - C#
  - C++
  - 알고리즘
keywords: "백준 1094, 백준 1094번, BOJ 1094, stickDivide, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1094번 - 막대기](https://www.acmicpc.net/problem/1094)

## 설명
이 문제는 길이 `64`인 막대를 절반으로 자르면서, **목표 길이 `X`를 만드는 최소한의 막대 조각 수**를 구하는 문제입니다.

---

## 접근법
이 문제는 본질적으로 **목표값 `X`를 만들기 위해 어떤 2의 거듭제곱을 조합할 수 있는지**를 찾는 문제입니다.
즉, `X`를 **이진수로 표현했을 때 `1`의 개수**가 정답입니다.

구체적인 과정은 다음과 같습니다:
- 초기 상태에서 길이 `64`인 막대 하나만 있습니다.
- 현재 막대 조각들의 합이 `X`보다 크다면, 가장 짧은 막대를 절반으로 자릅니다.
- 절반으로 자른 막대 2개 중 하나를 버릴지, 유지할지를 결정합니다:
  - 자른 후 하나만 남기면 총합이 `X`보다 작아지는 경우, 둘 다 유지해야 합니다.
  - 그렇지 않으면 하나는 버립니다.
- 이 과정을 반복하면서 막대 조각들의 총합이 정확히 `X`가 되는 시점을 찾습니다.
- 이때 남아있는 막대 조각의 개수가 정답입니다.

직접 위 과정에 따라서 직접 구현을 진행해도 괜찮지만, 답을 가장 빠르게 구현하는 방법 중 하나는 **이진수의 비트 단위 처리** 입니다.

풀이 과정은 결국 `X`를 2의 제곱수들의 합으로 분해하는 과정과 같으며, <br>
목표값을 만드는 데 필요한 최소 막대 수는 결국 `X`를 이진수로 나타냈을 때 1의 개수와 같기 때문입니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var target = int.Parse(Console.ReadLine()!);
      var sticks = new List<int> { 64 };

      while (true) {
        var sum = sticks.Sum();
        if (sum == target) {
          Console.WriteLine(sticks.Count);
          break;
        }

        var min = sticks.Min();
        sticks.Remove(min);
        min /= 2;
        if (sum - min < target)
          sticks.Add(min);
        sticks.Add(min);
      }
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

  int tar; cin >> tar;

  int cnt = 0;
  while (tar) {
    cnt += tar & 1;
    tar >>= 1;
  }

  cout << cnt << "\n";

  return 0;
}
```
