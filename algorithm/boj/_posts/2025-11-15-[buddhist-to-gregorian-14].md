---
layout: single
title: "[백준 18108] 1998년생인 내가 태국에서는 2541년생?! (C#, C++) - soo:bak"
date: "2025-11-15 02:00:00 +0900"
description: 태국 불기 연도를 서기로 변환하기 위해 543을 빼는 백준 18108번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[18108번 - 1998년생인 내가 태국에서는 2541년생?!](https://www.acmicpc.net/problem/18108)

## 설명

불기 연도가 주어지면 서기 연도로 바꾸기 위해 `543`을 뺍니다.<br>

<br>

## 접근법

입력된 연도에서 `543`을 빼 바로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var year = int.Parse(Console.ReadLine()!);
    Console.WriteLine(year - 543);
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

  int year; cin >> year;
  cout << year - 543 << "\n";

  return 0;
}
```

