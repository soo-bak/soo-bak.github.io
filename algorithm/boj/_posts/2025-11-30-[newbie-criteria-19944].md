---
layout: single
title: "[백준 19944] 뉴비의 기준은 뭘까? (C#, C++) - soo:bak"
date: "2025-11-30 01:48:00 +0900"
description: 학년 N과 M이 주어질 때 M학년을 NEWBIE, OLDBIE, TLE로 분류하는 백준 19944번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 19944
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 19944, 백준 19944번, BOJ 19944, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[19944번 - 뉴비의 기준은 뭘까?](https://www.acmicpc.net/problem/19944)

## 설명

동아리 학년 분류 규칙이 주어지는 상황에서, 전체 학년 수 N (3 ≤ N ≤ 1,000)과 특정 학생의 학년 M (1 ≤ M ≤ 1,000)이 주어질 때, 해당 학생의 분류를 출력하는 문제입니다.

분류 규칙은 다음과 같습니다:
- M이 1 또는 2이면: NEWBIE!
- M이 3 이상이고 N 이하이면: OLDBIE!
- 그 외의 경우: TLE!

<br>

## 접근법

주어진 M의 값에 따라 조건을 순서대로 확인합니다.

먼저 M이 1 또는 2인지 확인하여 NEWBIE!를 출력하고, 그렇지 않으면 M이 N 이하인지 확인하여 OLDBIE!를 출력하며, 둘 다 아니면 TLE!를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var input = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var n = input[0];
      var m = input[1];

      if (m <= 2) Console.WriteLine("NEWBIE!");
      else if (m <= n) Console.WriteLine("OLDBIE!");
      else Console.WriteLine("TLE!");
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

  int n, m; cin >> n >> m;
  
  if (m <= 2) cout << "NEWBIE!\n";
  else if (m <= n) cout << "OLDBIE!\n";
  else cout << "TLE!\n";

  return 0;
}
```


