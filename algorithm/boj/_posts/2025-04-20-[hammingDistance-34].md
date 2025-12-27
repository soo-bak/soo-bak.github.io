---
layout: single
title: "[백준 3449] 해밍 거리 (C#, C++) - soo:bak"
date: "2025-04-20 22:13:00 +0900"
description: 두 이진 문자열 간의 해밍 거리를 계산하는 로직을 구현한 백준 3449번 해밍 거리 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 3449
  - C#
  - C++
  - 알고리즘
keywords: "백준 3449, 백준 3449번, BOJ 3449, hammingDistance, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3449번 - 해밍 거리](https://www.acmicpc.net/problem/3449)

## 설명
두 숫자의 서로 다른 자리수의 개수를 나타내는 **해밍 거리(Hamming distance)**를 구하는 문제입니다.<br>

- 두 개의 이진수가 주어졌을 때, 서로 다른 자릿수의 개수를 세어 해밍 거리를 계산합니다.
- 각 테스트케이스마다 두 개의 이진 문자열이 주어지며, 길이는 항상 동일합니다.


## 접근법
- 각각의 케이스에서 이진수를 문자열로 입력받아, 각 자릿수를 순차적으로 비교합니다.
- 비교를 진행하며 각 자리의 수가 서로 다른 경우를 카운트합니다.
- 문자열의 길이가 같다는 조건이 보장되므로, 인덱스의 범위 초과는 고려하지 않아도 괜찮습니다.
- 문자열의 길이만큼 단순히 반복 순회하면 되므로, 시간 복잡도는 `O(n)` 입니다.


## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var input = Console.ReadLine().Split();
      string s1 = input[0], s2 = input[1];

      int dist = 0;
      for (int i = 0; i < s1.Length; i++) {
        if (s1[i] != s2[i]) dist++;
      }
      Console.WriteLine($"Hamming distance is {dist}.");
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
    string binary1, binary2; cin >> binary1 >> binary2;
    int dist = 0;
    for (size_t i = 0; i < binary1.size(); i++) {
      if (binary1[i] != binary2[i]) dist++;
    }
    cout << "Hamming distance is " << dist << ".\n";
  }

  return 0;
}
```
