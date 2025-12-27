---
layout: single
title: "[백준 12518] Centauri Prime (Small2) (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 12518번 C#, C++ 풀이 - 나라 이름의 마지막 글자로 통치자를 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 12518
  - C#
  - C++
  - 알고리즘
keywords: "백준 12518, 백준 12518번, BOJ 12518, CentauriPrimeSmall2, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12518번 - Centauri Prime (Small2)](https://www.acmicpc.net/problem/12518)

## 설명
나라 이름의 마지막 글자를 기준으로 통치자를 결정해 출력하는 문제입니다.

<br>

## 접근법
마지막 글자가 y면 nobody, 모음(a, e, i, o, u)이면 queen, 그 외는 king입니다.  
형식에 맞게 `Case #x: ...`로 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();

    for (var caseNo = 1; caseNo <= t; caseNo++) {
      var name = Console.ReadLine()!;
      var last = char.ToLower(name[name.Length - 1]);
      string who;
      if (last == 'y') who = "nobody";
      else if (last == 'a' || last == 'e' || last == 'i' || last == 'o' || last == 'u')
        who = "a queen";
      else who = "a king";

      sb.AppendLine($"Case #{caseNo}: {name} is ruled by {who}.");
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

  int t; cin >> t;
  for (int caseNo = 1; caseNo <= t; caseNo++) {
    string name; cin >> name;
    char last = name.back();
    if ('A' <= last && last <= 'Z') last = last - 'A' + 'a';

    string who;
    if (last == 'y') who = "nobody";
    else if (last == 'a' || last == 'e' || last == 'i' || last == 'o' || last == 'u')
      who = "a queen";
    else who = "a king";

    cout << "Case #" << caseNo << ": " << name << " is ruled by " << who << ".\n";
  }

  return 0;
}
```
