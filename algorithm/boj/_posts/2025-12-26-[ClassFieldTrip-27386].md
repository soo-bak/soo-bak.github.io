---
layout: single
title: "[백준 27386] Class Field Trip (C#, C++) - soo:bak"
date: "2025-12-26 02:38:00 +0900"
description: "백준 27386번 C#, C++ 풀이 - 두 정렬된 문자열을 합쳐 정렬된 결과를 만드는 문제"
tags:
  - 백준
  - BOJ
  - 27386
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
  - 정렬
keywords: "백준 27386, 백준 27386번, BOJ 27386, ClassFieldTrip, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[27386번 - Class Field Trip](https://www.acmicpc.net/problem/27386)

## 설명
정렬된 두 문자열이 주어질 때, 알파벳 순서를 유지하며 합친 문자열을 출력하는 문제입니다.

<br>

## 접근법
먼저 두 문자열의 포인터를 앞에서부터 움직이며 작은 문자를 선택합니다.

다음으로 한쪽이 끝나면 남은 문자를 그대로 이어 붙입니다.

마지막으로 완성된 문자열을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var a = Console.ReadLine()!;
    var b = Console.ReadLine()!;

    var i = 0;
    var j = 0;
    var sb = new StringBuilder();

    while (i < a.Length && j < b.Length) {
      if (a[i] <= b[j]) {
        sb.Append(a[i]);
        i++;
      } else {
        sb.Append(b[j]);
        j++;
      }
    }

    while (i < a.Length) {
      sb.Append(a[i]);
      i++;
    }
    while (j < b.Length) {
      sb.Append(b[j]);
      j++;
    }

    Console.WriteLine(sb.ToString());
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

  string a, b; cin >> a >> b;

  int i = 0;
  int j = 0;
  string out;
  while (i < (int)a.size() && j < (int)b.size()) {
    if (a[i] <= b[j]) {
      out.push_back(a[i]);
      i++;
    } else {
      out.push_back(b[j]);
      j++;
    }
  }

  while (i < (int)a.size()) {
    out.push_back(a[i]);
    i++;
  }
  while (j < (int)b.size()) {
    out.push_back(b[j]);
    j++;
  }

  cout << out << "\n";
  return 0;
}
```
