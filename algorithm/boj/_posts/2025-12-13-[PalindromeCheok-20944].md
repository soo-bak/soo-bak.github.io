---
layout: single
title: "[백준 20944] 팰린드롬 척화비 (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 같은 문자로 채워 길이 N을 맞추면 수미상관이면서 팰린드롬이 되는 점을 이용하는 백준 20944번 팰린드롬 척화비 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[20944번 - 팰린드롬 척화비](https://www.acmicpc.net/problem/20944)

## 설명
수미상관이면서 동시에 팰린드롬인 문자열을 구하는 문제입니다.

<br>

## 접근법
한 문자만 반복한 문자열은 팰린드롬이면서 수미상관 조건도 만족합니다.

따라서 임의의 소문자 하나를 n번 반복한 문자열을 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder(n);
    sb.Append('a', n);
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

  int n;
  if (!(cin >> n)) return 0;
  cout << string(n, 'a') << "\n";

  return 0;
}
```
