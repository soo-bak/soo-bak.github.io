---
layout: single
title: "[백준 30658] Os últimos serão os primeiros (C#, C++) - soo:bak"
date: "2025-12-20 12:12:00 +0900"
description: "백준 30658번 C#, C++ 풀이 - 1차 성적 순서를 뒤집어 2차 예상 순서를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 30658
  - C#
  - C++
  - 알고리즘
keywords: "백준 30658, 백준 30658번, BOJ 30658, ReverseRanking, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30658번 - Os últimos serão os primeiros](https://www.acmicpc.net/problem/30658)

## 설명
1차 성적 순서가 주어질 때, 이를 뒤집어 2차 예상 순서를 출력하는 문제입니다. 각 테스트케이스 출력 뒤에는 구분용 0을 추가합니다.

<br>

## 접근법
먼저 n을 읽어 0이면 종료합니다.

다음으로 n개의 정수를 읽어 배열에 저장한 뒤 역순으로 출력하고, 마지막에 0을 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    while (true) {
      var line = Console.ReadLine();
      if (line == null)
        break;

      var n = int.Parse(line);
      if (n == 0)
        break;

      var arr = new int[n];
      for (var i = 0; i < n; i++)
        arr[i] = int.Parse(Console.ReadLine()!);

      var sb = new StringBuilder();
      for (var i = n - 1; i >= 0; i--)
        sb.AppendLine(arr[i].ToString());
      sb.AppendLine("0");
      Console.Write(sb.ToString());
    }
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

  int n;
  while (cin >> n && n != 0) {
    vi v(n);
    for (int i = 0; i < n; i++)
      cin >> v[i];

    for (int i = n - 1; i >= 0; i--)
      cout << v[i] << "\n";
    cout << 0 << "\n";
  }

  return 0;
}
```
