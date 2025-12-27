---
layout: single
title: "[백준 16032] Income Inequality (C#, C++) - soo:bak"
date: "2025-12-26 00:28:01 +0900"
description: "백준 16032번 C#, C++ 풀이 - 평균 이하 소득자의 수를 계산해 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 16032
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 16032, 백준 16032번, BOJ 16032, IncomeInequality, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16032번 - Income Inequality](https://www.acmicpc.net/problem/16032)

## 설명
여러 데이터셋에서 평균 소득 이하인 사람의 수를 구하는 문제입니다.

<br>

## 접근법
먼저 한 데이터셋의 소득을 모두 읽어 합계를 구하고 평균을 계산합니다.

다음으로 평균 이하인 소득의 개수를 세어 출력합니다.

이후 n이 0이면 입력을 종료합니다.

마지막으로 각 데이터셋을 같은 방식으로 처리합니다.

<br>

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
    var sb = new StringBuilder();

    while (idx < parts.Length) {
      var n = int.Parse(parts[idx++]);
      if (n == 0) break;

      var arr = new int[n];
      long sum = 0;
      for (var i = 0; i < n; i++) {
        var v = int.Parse(parts[idx++]);
        arr[i] = v;
        sum += v;
      }

      var cnt = 0;
      for (var i = 0; i < n; i++) {
        if (arr[i] * n <= sum) cnt++;
      }

      sb.AppendLine(cnt.ToString());
    }

    Console.Write(sb);
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
    if (n == 0) break;

    vector<int> arr(n);
    long long sum = 0;
    for (int i = 0; i < n; i++) {
      cin >> arr[i];
      sum += arr[i];
    }

    int cnt = 0;
    for (int i = 0; i < n; i++) {
      if ((long long)arr[i] * n <= sum) cnt++;
    }

    cout << cnt << "\n";
  }

  return 0;
}
```
