---
layout: single
title: "[백준 9295] 주사위 (C#, C++) - soo:bak"
date: "2025-04-14 21:26:35 +0900"
description: 각 테스트 케이스마다 두 주사위의 합을 구해 출력하는 백준 9295번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 9295
  - C#
  - C++
  - 알고리즘
keywords: "백준 9295, 백준 9295번, BOJ 9295, diceCaseSum, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9295번 - 주사위](https://www.acmicpc.net/problem/9295)

## 설명
각 테스트 케이스에서 두 개의 주사위 값을 입력받고,  <br>
<br>
해당 주사위의 **합을 출력하되**, `"Case i: 결과"` 형식으로 출력하는 문제입니다.

---

## 접근법
- 먼저 전체 테스트 케이스 수를 입력받습니다.
- 각 테스트 케이스마다 두 정수를 입력받고, 그 합을 구한 뒤 출력합니다.
- 출력 형식은 `"Case i: 합"` 형식으로, 테스트 케이스 번호를 포함해야 합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int t = int.Parse(Console.ReadLine()!);
      for (int i = 1; i <= t; i++) {
        var input = Console.ReadLine()!.Split();
        int a = int.Parse(input[0]);
        int b = int.Parse(input[1]);
        Console.WriteLine($"Case {i}: {a + b}");
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

  int t; cin >> t;
  int cnt = 1;
  while (t--) {
    int f, s; cin >> f >> s;
    cout << "Case " << cnt << ": " << f + s << "\n";
    cnt++;
  }

  return 0;
}
```
