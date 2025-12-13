---
layout: single
title: "[백준 4589] Gnome Sequencing (C#, C++) - soo:bak"
date: "2025-12-13 13:02:00 +0900"
description: 세 수가 오름차순 또는 내림차순인지 확인해 Ordered/Unordered를 판정하는 백준 4589번 Gnome Sequencing 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[4589번 - Gnome Sequencing](https://www.acmicpc.net/problem/4589)

## 설명
세 수염 길이가 정렬되어 있는지 판단하는 문제입니다.

<br>

## 접근법
세 값이 오름차순이거나 내림차순이면 Ordered, 그렇지 않으면 Unordered입니다.

첫 번째 값과 두 번째 값, 두 번째 값과 세 번째 값의 대소 관계가 일관되면 정렬된 것입니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    Console.WriteLine("Gnomes:");
    for (var i = 0; i < n; i++) {
      var p = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var a = p[0]; var b = p[1]; var c = p[2];
      var ordered = (a <= b && b <= c) || (a >= b && b >= c);
      Console.WriteLine(ordered ? "Ordered" : "Unordered");
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

  int n; cin >> n;
  cout << "Gnomes:\n";
  for (int i = 0; i < n; i++) {
    int a, b, c; cin >> a >> b >> c;
    bool ordered = (a <= b && b <= c) || (a >= b && b >= c);
    cout << (ordered ? "Ordered" : "Unordered") << "\n";
  }

  return 0;
}
```
