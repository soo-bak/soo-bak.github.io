---
layout: single
title: "[백준 16394] 홍익대학교 (C#, C++) - soo:bak"
date: "2025-11-21 23:27:00 +0900"
description: 입력 연도에서 1946을 빼 홍익대학교 개교 주년을 구하는 백준 16394번 홍익대학교 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[16394번 - 홍익대학교](https://www.acmicpc.net/problem/16394)

## 설명

주어진 연도가 홍익대학교 개교 몇 주년인지 구하는 문제입니다.<br>

홍익대학교는 `1946`년에 개교했으므로, 연도 `N`이 주어지면 `N - 1946`이 개교 주년입니다.<br>

<br>

## 접근법

입력받은 연도에서 `1946`을 빼서 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      Console.WriteLine(n - 1946);
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

  int n; cin >> n;

  cout << n - 1946 << "\n";

  return 0;
}
```

