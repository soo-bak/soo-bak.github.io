---
layout: single
title: "[백준 11109] 괴짜 교수 (C#, C++) - soo:bak"
date: "2025-05-04 17:41:00 +0900"
description: 병렬 처리 개발 시간과 실행 횟수를 비교하여 병렬화 여부를 판단하는 백준 11109번 괴짜 교수 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[11109번 - 괴짜 교수](https://www.acmicpc.net/problem/11109)

## 설명
병렬 처리 개발 시간과 실행 횟수를 비교하여 병렬 프로그램의 개발 여부를 판단하는 조건 비교 문제입니다.

<br>

## 접근법

각 경우에 다음과 같은 총 시간이 소요됩니다:
- 직렬 버전 총 시간: `n * s`
- 병렬 버전 총 시간: `d + n * p`

<br>
이 두 값을 비교하여,
- 병렬 버전이 빠르면 `"parallelize"`
- 직렬 버전이 빠르면 `"do not parallelize"`
- 동일하면 `"does not matter"`

을 출력합니다.

<br>

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var input = Console.ReadLine().Split().Select(int.Parse).ToArray();
      int d = input[0], n = input[1], s = input[2], p = input[3];

      int par = d + n * p, seq = n * s;
      if (par < seq)
        Console.WriteLine("parallelize");
      else if (par > seq)
        Console.WriteLine("do not parallelize");
      else
        Console.WriteLine("does not matter");
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

  int t; cin >> t;
  while (t--) {
    int d, n, s, p; cin >> d >> n >> s >> p;
    int par = d + n * p, seq = n * s;
    cout << (par < seq ?
              "parallelize" : par > seq ?
              "do not parallelize" : "does not matter") << "\n";
  }

  return 0;
}
```
