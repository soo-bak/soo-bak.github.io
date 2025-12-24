---
layout: single
title: "[백준 32278] 선택 가능성이 가장 높은 자료형 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: 값의 범위를 확인해 가장 작은 정수 자료형을 선택하는 문제
---

## 문제 링크
[32278번 - 선택 가능성이 가장 높은 자료형](https://www.acmicpc.net/problem/32278)

## 설명
정수 N을 정확히 표현할 수 있는 최소 크기의 정수 자료형을 출력하는 문제입니다.

<br>

## 접근법
주어진 정수가 각 자료형의 범위에 들어가는지 작은 자료형부터 순서대로 확인합니다.

먼저 short 범위인지 확인하고, 아니면 int, 그래도 아니면 long long을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = long.Parse(Console.ReadLine()!);
    if (n >= short.MinValue && n <= short.MaxValue) Console.WriteLine("short");
    else if (n >= int.MinValue && n <= int.MaxValue) Console.WriteLine("int");
    else Console.WriteLine("long long");
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

  ll n; cin >> n;
  if (n >= -32768 && n <= 32767) cout << "short\n";
  else if (n >= -2147483648LL && n <= 2147483647LL) cout << "int\n";
  else cout << "long long\n";

  return 0;
}
```
