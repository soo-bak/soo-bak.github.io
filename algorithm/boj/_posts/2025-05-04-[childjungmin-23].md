---
layout: single
title: "[백준 11382] 꼬마 정민 (C#, C++) - soo:bak"
date: "2025-05-04 08:15:00 +0900"
description: 세 수를 입력받아 모두 더한 값을 출력하는 백준 11382번 꼬마 정민 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11382
  - C#
  - C++
  - 알고리즘
keywords: "백준 11382, 백준 11382번, BOJ 11382, childjungmin, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11382번 - 꼬마 정민](https://www.acmicpc.net/problem/11382)

## 설명
세 수를 입력받아 **모두 더한 값을 출력하는 문제**입니다.

입력되는 세 수는 각각 최대 $$10^{12}$$까지 가능하므로, **정수 오버플로우에 유의해야 합니다.**

<br>

## 접근법
- 공백을 기준으로 나뉜 세 수를 입력받습니다.
- 입력받은 값을 모두 더하여 출력합니다.
- 자료형은 **64비트 정수형**을 사용해야 안전하게 처리할 수 있습니다.

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var sum = Console.ReadLine()
      .Split()
      .Select(long.Parse)
      .Sum();

    Console.WriteLine(sum);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll num1, num2, num3; cin >> num1 >> num2 >> num3;
  cout << num1 + num2 + num3 << "\n";

  return 0;
}
```
