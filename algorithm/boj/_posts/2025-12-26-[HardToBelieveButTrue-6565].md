---
layout: single
title: "[백준 6565] Hard to Believe, but True! (C#, C++) - soo:bak"
date: "2025-12-26 04:20:00 +0900"
description: "백준 6565번 C#, C++ 풀이 - 숫자를 뒤집어 식의 참거짓을 판단하는 문제"
tags:
  - 백준
  - BOJ
  - 6565
  - C#
  - C++
  - 알고리즘
keywords: "백준 6565, 백준 6565번, BOJ 6565, HardToBelieveButTrue, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6565번 - Hard to Believe, but True!](https://www.acmicpc.net/problem/6565)

## 설명
식의 각 숫자를 거꾸로 읽었을 때 덧셈이 성립하는지 판단하는 문제입니다.

<br>

## 접근법
먼저 입력 줄을 세 숫자로 분리합니다.

다음으로 각 숫자 문자열을 뒤집어 정수로 바꿔 더한 뒤 비교합니다.

마지막으로 결과에 따라 True 또는 False를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int Rev(string s) {
    var arr = s.ToCharArray();
    Array.Reverse(arr);
    return int.Parse(new string(arr));
  }

  static void Main() {
    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;

      var plus = line.IndexOf('+');
      var eq = line.IndexOf('=');

      var a = line.Substring(0, plus);
      var b = line.Substring(plus + 1, eq - plus - 1);
      var c = line.Substring(eq + 1);

      var ra = Rev(a);
      var rb = Rev(b);
      var rc = Rev(c);

      if (ra + rb == rc) Console.WriteLine("True");
      else Console.WriteLine("False");

      if (line == "0+0=0") break;
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int revStr(const string &s) {
  string t = s;
  reverse(t.begin(), t.end());
  return stoi(t);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string line;
  while (cin >> line) {
    int plus = line.find('+');
    int eq = line.find('=');

    string a = line.substr(0, plus);
    string b = line.substr(plus + 1, eq - plus - 1);
    string c = line.substr(eq + 1);

    int ra = revStr(a);
    int rb = revStr(b);
    int rc = revStr(c);

    if (ra + rb == rc) cout << "True\n";
    else cout << "False\n";

    if (line == "0+0=0") break;
  }

  return 0;
}
```
