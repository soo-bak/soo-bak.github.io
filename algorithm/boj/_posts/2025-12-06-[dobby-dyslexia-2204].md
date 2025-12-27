---
layout: single
title: "[백준 2204] 도비의 난독증 테스트 (C#, C++) - soo:bak"
date: "2025-12-06 17:52:00 +0900"
description: 대소문자를 무시하고 사전순으로 가장 앞서는 단어를 찾는 백준 2204번 도비의 난독증 테스트 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2204
  - C#
  - C++
  - 알고리즘
  - 문자열
  - 정렬
keywords: "백준 2204, 백준 2204번, BOJ 2204, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2204번 - 도비의 난독증 테스트](https://www.acmicpc.net/problem/2204)

## 설명
여러 단어가 주어질 때, 대소문자를 구분하지 않고 사전순으로 가장 앞서는 단어를 출력하는 문제입니다.

출력할 때는 원본 단어 그대로 출력합니다. 테스트케이스는 N이 0일 때 종료됩니다.

<br>

## 접근법
먼저, 각 단어를 소문자로 변환한 값을 비교 기준으로 사용합니다. 원본 단어는 따로 저장해두어 나중에 출력합니다.

다음으로, 모든 단어를 순회하며 현재까지의 최솟값과 비교합니다. 소문자 변환 값이 더 작으면 최솟값을 갱신합니다.

<br>

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      while (true) {
        var line = Console.ReadLine();
        if (line == null)
          break;
        var n = int.Parse(line);
        if (n == 0)
          break;

        var bestOrig = "";
        var bestKey = "";
        for (var i = 0; i < n; i++) {
          var w = Console.ReadLine()!;
          var key = w.ToLower();
          if (i == 0 || string.CompareOrdinal(key, bestKey) < 0) {
            bestKey = key;
            bestOrig = w;
          }
        }
        Console.WriteLine(bestOrig);
      }
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

  int n;
  while (cin >> n) {
    if (n == 0)
      break;
    string bestOrig, bestKey;
    for (int i = 0; i < n; i++) {
      string w; cin >> w;
      string key = w;
      for (char &ch : key)
        ch = tolower(ch);
      if (i == 0 || key < bestKey) {
        bestKey = key;
        bestOrig = w;
      }
    }
    cout << bestOrig << "\n";
  }

  return 0;
}
```
