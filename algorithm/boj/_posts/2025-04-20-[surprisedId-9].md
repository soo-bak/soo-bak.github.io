---
layout: single
title: "[백준 10926] ??! (C#, C++) - soo:bak"
date: "2025-04-20 01:10:00 +0900"
description: 입력된 사용자 이름 뒤에 ??!를 붙여 출력하는 백준 10926번 ??! 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10926번 - ??!](https://www.acmicpc.net/problem/10926)

## 설명
**입력된 사용자 이름 뒤에 특정 문자열을 붙여 출력하는 단순한 문자열 출력 문제**입니다.
<br>

- 사용자로부터 하나의 문자열이 입력으로 주어집니다.
- 해당 문자열 뒤에 `??!`를 붙여 출력해야 합니다.
<br>

## 접근법

1. 문자열을 그대로 입력받습니다.
2. 해당 문자열 뒤에 `??!`를 덧붙여 출력합니다.

- 공백이 없고, 입력 문자열 길이도 최대 `50`이므로 단순히 구현 가능합니다.
- 출력 형식에 맞게 `??!`를 붙이는 것이 핵심입니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string name = Console.ReadLine();
    Console.WriteLine(name + "??!");
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

  string str; cin >> str;
  cout << str << "??!" << "\n";

  return 0;
}
```
