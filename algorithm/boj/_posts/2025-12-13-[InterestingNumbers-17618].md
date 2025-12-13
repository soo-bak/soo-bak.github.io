---
layout: single
title: "[백준 17618] 신기한 수 (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 1부터 N까지 자릿수 합으로 나누어떨어지는 수를 세는 백준 17618번 신기한 수 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[17618번 - 신기한 수](https://www.acmicpc.net/problem/17618)

## 설명
자릿수 합으로 나누어떨어지는 수의 개수를 구하는 문제입니다.

<br>

## 접근법
1부터 n까지 순회하며 각 수의 자릿수 합을 구합니다.

해당 수가 자릿수 합으로 나누어떨어지면 '신기한 수'입니다.

조건을 만족하는 수의 개수를 세어 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var cnt = 0;
    for (var x = 1; x <= n; x++) {
      var y = x; var sum = 0;
      while (y > 0) {
        sum += y % 10;
        y /= 10;
      }
      if (x % sum == 0) cnt++;
    }
    Console.WriteLine(cnt);
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

  int n;
  if (!(cin >> n)) return 0;
  int cnt = 0;
  for (int x = 1; x <= n; x++) {
    int y = x, sum = 0;
    while (y > 0) {
      sum += y % 10;
      y /= 10;
    }
    if (x % sum == 0) cnt++;
  }
  cout << cnt << "\n";

  return 0;
}
```
