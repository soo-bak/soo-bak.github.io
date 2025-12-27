---
layout: single
title: "[백준 9313] Integer Flipping (C#, C++) - soo:bak"
date: "2025-12-27 05:55:00 +0900"
description: 32비트 부호 없는 정수를 비트 반전(역순)한 값을 출력하는 문제
---

## 문제 링크
[9313번 - Integer Flipping](https://www.acmicpc.net/problem/9313)

## 설명
지구 기준 32비트 부호 없는 정수의 비트를 역순으로 뒤집어(0번째↔31번째) 다시 부호 없는 정수로 읽어 출력하는 문제입니다. 입력은 -1이 나오면 종료합니다.

<br>

## 접근법
입력값의 최하위 비트를 하나씩 꺼내 결과의 최하위에 넣고 시프트하는 과정을 32번 반복합니다. 이렇게 하면 비트 순서가 뒤집힌 값을 얻을 수 있습니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string? line;
    while ((line = Console.ReadLine()) != null) {
      if (line.StartsWith("-1")) break;
      
      var x = uint.Parse(line);
      var res = 0u;
      for (var i = 0; i < 32; i++) {
        res <<= 1;
        res |= (x & 1);
        x >>= 1;
      }
      Console.WriteLine(res);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef unsigned int ui;
typedef unsigned long long ull;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  long long in;
  while (cin >> in) {
    if (in == -1) break;

    ui x = static_cast<ui>(in);
    ui res = 0;
    for (int i = 0; i < 32; i++) {
      res <<= 1;
      res |= (x & 1U);
      x >>= 1;
    }
    cout << static_cast<ull>(res) << "\n";
  }

  return 0;
}
```
