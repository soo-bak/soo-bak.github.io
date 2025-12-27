---
layout: single
title: "[백준 9713] Sum of Odd Sequence (C#, C++) - soo:bak"
date: "2025-11-15 01:50:00 +0900"
description: 1부터 N까지 홀수를 더하는 합을 테스트 케이스마다 계산하는 백준 9713번 Sum of Odd Sequence 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 9713
  - C#
  - C++
  - 알고리즘
keywords: "백준 9713, 백준 9713번, BOJ 9713, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9713번 - Sum of Odd Sequence](https://www.acmicpc.net/problem/9713)

## 설명

홀수 `N`이 주어질 때, `1`부터 `N`까지의 모든 홀수의 합을 구하는 문제입니다.<br>

예를 들어 `N = 9`이면 `1 + 3 + 5 + 7 + 9 = 25`를 출력합니다.<br>

<br>

## 접근법

수학 공식을 사용하여 해결합니다.

`1`부터 `N`까지 홀수의 개수는 `(N + 1) / 2`입니다. 홀수가 `k`개 있을 때 첫 `k`개 홀수의 합은 `k²`입니다.

<br>
따라서 홀수의 개수를 구한 뒤 제곱하면 답을 바로 계산할 수 있습니다.

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
      var outputs = new int[t];

      for (var i = 0; i < t; i++) {
        var n = int.Parse(Console.ReadLine()!);
        var count = (n + 1) / 2;
        outputs[i] = count * count;
      }

      Console.WriteLine(string.Join("\n", outputs));
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
  while (t--) {
    int n; cin >> n;
    int count = (n + 1) / 2;
    cout << count * count << "\n";
  }

  return 0;
}
```

