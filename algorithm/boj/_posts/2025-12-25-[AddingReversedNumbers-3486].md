---
layout: single
title: "[백준 3486] Adding Reversed Numbers (C#, C++) - soo:bak"
date: "2025-12-25 14:56:00 +0900"
description: 두 수를 뒤집어 더한 뒤 다시 뒤집는 구현 문제
---

## 문제 링크
[3486번 - Adding Reversed Numbers](https://www.acmicpc.net/problem/3486)

## 설명
주어진 두 수를 뒤집어 더한 다음, 합을 다시 뒤집어 출력하는 문제입니다.

<br>

## 접근법
각 숫자를 뒤집는 함수를 만들어 처리합니다.  
`rev(a) + rev(b)`를 계산한 뒤, 결과를 다시 뒤집어 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int Rev(int x) {
    var r = 0;
    while (x > 0) {
      r = r * 10 + x % 10;
      x /= 10;
    }
    return r;
  }

  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < t; i++) {
      var parts = Console.ReadLine()!.Split();
      var a = int.Parse(parts[0]);
      var b = int.Parse(parts[1]);

      var sum = Rev(a) + Rev(b);
      Console.WriteLine(Rev(sum));
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int rev(int x) {
  int r = 0;
  while (x > 0) {
    r = r * 10 + x % 10;
    x /= 10;
  }
  return r;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int a, b; cin >> a >> b;
    int sum = rev(a) + rev(b);
    cout << rev(sum) << "\n";
  }

  return 0;
}
```
