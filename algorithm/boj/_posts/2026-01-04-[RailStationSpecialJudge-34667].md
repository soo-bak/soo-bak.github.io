---
layout: single
title: "[백준 34667] 가희와 철도역 (스페셜 저지) (C#, C++) - soo:bak"
date: "2026-01-04 17:40:00 +0900"
description: "백준 34667번 C#, C++ 풀이 - 문자열 T가 주어질 때 최소 길이의 역명 V를 구성해 두 가지 이상 다른 삭제 방법으로 T를 만들 수 있도록 하는 문제"
tags:
  - 백준
  - BOJ
  - 34667
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 34667, 백준 34667번, BOJ 34667, 가희와 철도역, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[34667번 - 가희와 철도역 (스페셜 저지)](https://www.acmicpc.net/problem/34667)

## 설명
문자열 S와 T가 주어지며 두 문자열은 항상 동일합니다. 역명 V는 T를 부분 문자열로 포함하고, V에서 문자를 하나 이상 제거해 T를 만드는 방법이 두 가지 이상 존재해야 하며, 가능한 V 중 길이가 최소여야 합니다.

<br>

## 접근법
먼저 V의 길이는 T의 길이보다 1 이상 커야 합니다. 길이가 같으면 한 글자도 삭제할 수 없기 때문입니다.

다음으로 길이 T+1인 경우, T의 첫 글자를 앞에 한 번 더 붙인 형태로 두 가지 다른 삭제 방법을 만들 수 있습니다.


첫 글자를 앞에 붙인 T[0] + T 형태에서,

방법 1은 앞에 붙인 글자를 사용하고 원래 첫 글자를 삭제하는 것이고,

방법 2는 앞 글자를 삭제하고 원래 T 부분을 그대로 사용하는 것입니다.


따라서 항상 길이 T+1인 위 문자열이 최소 해답이 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var t = Console.ReadLine()!;

    var v = t[0] + t;
    Console.WriteLine(v);
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

  string s, t;
  cin >> s >> t;

  string v;
  v.reserve(t.size() + 1);
  v.push_back(t[0]);
  v += t;

  cout << v << "\n";

  return 0;
}
```
