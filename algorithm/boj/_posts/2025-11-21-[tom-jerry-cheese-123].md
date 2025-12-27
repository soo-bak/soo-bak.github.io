---
layout: single
title: "[백준 16430] 제리와 톰 (C#, C++) - soo:bak"
date: "2025-11-21 23:38:00 +0900"
description: 전체 1kg 중 A/B kg를 뺀 나머지를 기약분수로 출력하는 백준 16430번 제리와 톰 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 16430
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 16430, 백준 16430번, BOJ 16430, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16430번 - 제리와 톰](https://www.acmicpc.net/problem/16430)

## 설명

제리가 치즈 `1kg` 중 일부를 먹었습니다. 먹은 양은 `A/B kg`이며, `A`와 `B`는 서로소입니다.<br>

남은 치즈의 양을 기약분수로 출력하는 문제입니다.<br>

<br>

## 접근법

전체 `1kg`에서 `A/B kg`를 뺀 남은 양은 `1 - A/B = (B - A) / B`입니다. 즉, 분자는 `B - A`, 분모는 `B`가 됩니다.<br>

입력으로 주어진 `A`와 `B`가 이미 서로소(최대공약수가 `1`)이므로, `B - A`와 `B`도 서로소입니다.

예를 들어 `A = 1, B = 4`이면 `B - A = 3`이고 `3`과 `4`는 서로소입니다.

또한 `A = 3, B = 7`이면 `B - A = 4`이고 `4`와 `7`은 서로소입니다.

따라서 별도의 약분 없이 `B - A`와 `B`를 그대로 출력하면 기약분수가 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var a = int.Parse(tokens[0]);
      var b = int.Parse(tokens[1]);

      Console.WriteLine($"{b - a} {b}");
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

  int a, b; cin >> a >> b;

  cout << (b - a) << " " << b << "\n";

  return 0;
}
```

