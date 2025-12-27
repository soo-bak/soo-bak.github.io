---
layout: single
title: "[백준 11121] Communication Channels (C#, C++) - soo:bak"
date: "2025-12-13 13:02:00 +0900"
description: 전송 전후 비트 문자열이 동일한지 비교해 OK/ERROR를 출력하는 백준 11121번 Communication Channels 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11121
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 11121, 백준 11121번, BOJ 11121, CommunicationChannels, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11121번 - Communication Channels](https://www.acmicpc.net/problem/11121)

## 설명
원본 비트열과 수신 비트열이 같은지 판단하는 문제입니다.

<br>

## 접근법
두 문자열을 비교하여 완전히 같으면 OK, 하나라도 다르면 ERROR를 출력합니다.

단순 문자열 비교만으로 해결할 수 있습니다.

<br>

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < t; i++) {
      var line = Console.ReadLine()!.Split();
      Console.WriteLine(line[0] == line[1] ? "OK" : "ERROR");
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

  int t; cin >> t;
  while (t--) {
    string a, b; cin >> a >> b;
    cout << (a == b ? "OK" : "ERROR") << "\n";
  }

  return 0;
}
```
