---
layout: single
title: "[백준 16103] Drawn and Quartered (C#, C++) - soo:bak"
date: "2026-04-21 21:33:00 +0900"
description: "백준 16103번 C#, C++ 풀이 - 문자열을 4등분한 뒤 블록 순서를 바꾸는 연산의 주기를 이용하는 문제"
tags:
  - 백준
  - BOJ
  - 16103
  - C#
  - C++
  - 알고리즘
  - 문자열
  - 구현
keywords: "백준 16103, 백준 16103번, BOJ 16103, Drawn and Quartered, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16103번 - Drawn and Quartered](https://www.acmicpc.net/problem/16103)

## 설명
문자열을 정확히 4등분한 뒤, 가운데 두 구간을 뒤로 보내는 연산을 여러 번 적용했을 때의 최종 문자열을 구하는 문제입니다.

<br>

## 접근법
문자열을 네 구간 `A B C D`로 나누면, 한 번의 연산 뒤에는 `A D B C`가 됩니다.

이 연산을 다시 적용해 보면 `A C D B`, 그다음에는 다시 원래 문자열 `A B C D`로 돌아옵니다. 즉 이 연산의 주기는 `3`입니다.

따라서 `K`가 매우 커도 `K % 3`만 확인하면 됩니다. 나머지가 `0`이면 원래 문자열, `1`이면 `A D B C`, `2`이면 `A C D B`를 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string[] first = Console.ReadLine()!.Split();
    int n = int.Parse(first[0]);
    long k = long.Parse(first[1]);
    string s = Console.ReadLine()!;

    int q = n / 4;
    string a = s.Substring(0, q);
    string b = s.Substring(q, q);
    string c = s.Substring(2 * q, q);
    string d = s.Substring(3 * q, q);

    long mod = k % 3;

    if (mod == 0)
      Console.WriteLine(a + b + c + d);
    else if (mod == 1)
      Console.WriteLine(a + d + b + c);
    else
      Console.WriteLine(a + c + d + b);
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
  long long k;
  cin >> n >> k;

  string s;
  cin >> s;

  int q = n / 4;
  string a = s.substr(0, q);
  string b = s.substr(q, q);
  string c = s.substr(2 * q, q);
  string d = s.substr(3 * q, q);

  long long mod = k % 3;

  if (mod == 0)
    cout << a + b + c + d << "\n";
  else if (mod == 1)
    cout << a + d + b + c << "\n";
  else
    cout << a + c + d + b << "\n";

  return 0;
}
```
