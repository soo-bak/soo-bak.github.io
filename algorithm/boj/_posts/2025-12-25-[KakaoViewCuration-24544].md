---
layout: single
title: "[백준 24544] 카카오뷰 큐레이팅 효용성 분석 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 24544번 C#, C++ 풀이 - 전체 흥미도 합과 미등록 콘텐츠 흥미도 합을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 24544
  - C#
  - C++
  - 알고리즘
keywords: "백준 24544, 백준 24544번, BOJ 24544, KakaoViewCuration, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24544번 - 카카오뷰 큐레이팅 효용성 분석](https://www.acmicpc.net/problem/24544)

## 설명
콘텐츠 흥미도와 My뷰 등록 여부가 주어질 때, 전체 흥미도 합과 미등록 콘텐츠의 흥미도 합을 출력하는 문제입니다.

<br>

## 접근법
흥미도 배열을 모두 합해 전체 합을 구합니다.  
등록 여부가 0인 콘텐츠만 따로 더해 두 번째 값을 계산합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);

    var a = new int[n];
    for (var i = 0; i < n; i++)
      a[i] = int.Parse(parts[idx++]);

    var sumAll = 0;
    for (var i = 0; i < n; i++)
      sumAll += a[i];

    var sumNot = 0;
    for (var i = 0; i < n; i++) {
      var b = int.Parse(parts[idx++]);
      if (b == 0) sumNot += a[i];
    }

    var sb = new StringBuilder();
    sb.AppendLine(sumAll.ToString());
    sb.AppendLine(sumNot.ToString());
    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  int sumAll = 0;
  for (int i = 0; i < n; i++)
    sumAll += a[i];

  int sumNot = 0;
  for (int i = 0; i < n; i++) {
    int b; cin >> b;
    if (b == 0) sumNot += a[i];
  }

  cout << sumAll << "\n" << sumNot << "\n";

  return 0;
}
```
