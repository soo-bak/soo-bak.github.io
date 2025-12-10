---
layout: single
title: "[백준 13301] 타일 장식물 (C#, C++) - soo:bak"
date: "2025-12-09 12:50:00 +0900"
description: 피보나치 형태로 커지는 정사각형들을 둘러싼 직사각형 둘레를 이전 둘레 두 개의 합으로 구하는 백준 13301번 타일 장식물 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[13301번 - 타일 장식물](https://www.acmicpc.net/problem/13301)

## 설명
정사각형 한 변 길이가 피보나치 수열로 커지는 타일을 나선처럼 붙일 때, N개 타일이 만드는 전체 직사각형의 둘레를 구합니다. 둘레 값은 64비트 범위가 필요합니다.

<br>

## 접근법
타일 한 개일 때 둘레는 4이고, 두 개일 때는 6입니다. 세 개 이상부터는 직전 둘레와 그 전 둘레를 더한 값이 됩니다.

피보나치 수열처럼 이전 두 값을 더해 다음 값을 구하는 방식으로 N번째까지 계산합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var p = new long[81];
    p[1] = 4;
    p[2] = 6;
    for (var i = 3; i <= n; i++)
      p[i] = p[i - 1] + p[i - 2];
    Console.WriteLine(p[n]);
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

  int n; cin >> n;
  ll p[81] = {0};
  p[1] = 4; p[2] = 6;
  for (int i = 3; i <= n; i++)
    p[i] = p[i - 1] + p[i - 2];
  cout << p[n] << "\n";

  return 0;
}
```
