---
layout: single
title: "[백준 29534] Буквы и весы (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 29534번 C#, C++ 풀이 - 글자 수가 n 이하인지 확인하고 필요한 큐브 최소 합을 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 29534
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 29534, 백준 29534번, BOJ 29534, LettersAndScales, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[29534번 - Буквы и весы](https://www.acmicpc.net/problem/29534)

## 설명
저울 개수와 단어가 주어질 때, 단어를 표시할 수 있는지 확인하고 가능하면 필요한 큐브 최소 합을 출력하는 문제입니다.

<br>

## 접근법
먼저 단어 길이가 저울 개수를 넘으면 Impossible을 출력합니다.

그렇지 않으면 각 문자에 대응하는 값을 합산합니다. 알파벳 순서대로 1부터 26까지의 값을 가지며, 모든 문자의 값을 더해 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;

    if (s.Length > n) {
      Console.WriteLine("Impossible");
      return;
    }

    var sum = 0;
    foreach (var ch in s)
      sum += ch - 'a' + 1;

    Console.WriteLine(sum);
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
  string s; cin >> s;

  if ((int)s.size() > n) {
    cout << "Impossible\n";
    return 0;
  }

  int sum = 0;
  for (char ch : s)
    sum += ch - 'a' + 1;

  cout << sum << "\n";

  return 0;
}
```
