---
layout: single
title: "[백준 20216] Ducky Debugging (C#, C++) - soo:bak"
date: "2025-12-30 12:33:00 +0900"
description: "백준 20216번 C#, C++ 풀이 - 문장 끝 문장부호에 따라 대답하며 종료 문장을 만나면 끝내는 인터랙티브 문제"
tags:
  - 백준
  - BOJ
  - 20216
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 20216, 백준 20216번, BOJ 20216, Ducky Debugging, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[20216번 - Ducky Debugging](https://www.acmicpc.net/problem/20216)

## 설명
입력으로 문장이 주어질 때, 문장 끝이 ?이면 Quack!, .이면 *Nod*를 출력하는 문제입니다. I quacked the code!가 입력되면 프로그램을 종료합니다.

<br>

## 접근법
먼저 한 줄씩 입력을 받고, 종료 문장인지 확인합니다.

다음으로 마지막 문자를 확인하여 ?이면 Quack!, .이면 *Nod*를 출력합니다. 인터랙티브 문제이므로 매 출력마다 버퍼를 플러시해야 합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.IO;

class Program {
  static void Main() {
    var sr = new StreamReader(Console.OpenStandardInput());
    var sw = new StreamWriter(Console.OpenStandardOutput());

    while (true) {
      var line = sr.ReadLine();
      if (line == null)
        break;
      if (line == "I quacked the code!")
        break;

      var last = line[^1];
      if (last == '?')
        sw.WriteLine("Quack!");
      else
        sw.WriteLine("*Nod*");
      sw.Flush();
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

  string line;
  while (getline(cin, line)) {
    if (line == "I quacked the code!")
      break;
    char last = line.back();
    if (last == '?')
      cout << "Quack!" << endl;
    else
      cout << "*Nod*" << endl;
  }

  return 0;
}
```
