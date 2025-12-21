---
layout: single
title: "[백준 31833] 온데간데없을뿐더러 (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 배열을 이어붙여 만든 두 수 중 더 작은 값을 출력하는 문제
---

## 문제 링크
[31833번 - 온데간데없을뿐더러](https://www.acmicpc.net/problem/31833)

## 설명
배열 A, B를 각각 순서대로 이어 만든 수 X, Y 중 더 작은 값을 출력하는 문제입니다.

<br>

## 접근법
각 배열의 원소들을 문자열로 이어 붙여 두 수를 만듭니다.

이후 길이가 더 짧은 쪽이 더 작은 수이고, 길이가 같으면 문자열 비교로 더 작은 값을 선택해 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var a = Console.ReadLine()!.Split();
    var b = Console.ReadLine()!.Split();

    var x = "";
    var y = "";
    for (var i = 0; i < n; i++) {
      x += a[i];
      y += b[i];
    }

    if (x.Length < y.Length) Console.WriteLine(x);
    else if (x.Length > y.Length) Console.WriteLine(y);
    else Console.WriteLine(string.CompareOrdinal(x, y) <= 0 ? x : y);
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

  int n; cin >> n;
  string x, y;
  for (int i = 0; i < n; i++) {
    string s; cin >> s;
    x += s;
  }
  for (int i = 0; i < n; i++) {
    string s; cin >> s;
    y += s;
  }

  if (x.size() < y.size()) cout << x << "\n";
  else if (x.size() > y.size()) cout << y << "\n";
  else cout << (x <= y ? x : y) << "\n";

  return 0;
}
```
