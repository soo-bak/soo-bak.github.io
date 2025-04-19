---
layout: single
title: "[백준 10926] ??! (C#, C++) - soo:bak"
date: "2025-04-20 01:08:00 +0900"
description: 입력된 사용자 이름 뒤에 ??!를 붙여 출력하는 백준 10926번 ??! 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10926번 - ??!](https://www.acmicpc.net/problem/10926)

## 설명
**입력된 사용자 이름 뒤에 특정 문자열을 붙여 출력하는 단순한 문자열 출력 문제**입니다.  
<br>

- 사용자로부터 하나의 문자열(아이디)이 입력으로 주어집니다.
- 해당 아이디 뒤에 `??!`를 붙여 출력해야 합니다.
<br>

예를 들어 입력이 `joonas`라면, 출력은 `joonas??!`가 되어야 합니다.

## 접근법

이 문제는 매우 단순한 문자열 덧붙이기 문제로, 다음과 같이 해결할 수 있습니다:

1. 문자열을 그대로 입력받습니다.
2. 해당 문자열 뒤에 `??!`를 덧붙여 출력합니다.

- 공백이 없고, 입력 문자열 길이도 최대 50이므로 별다른 예외 처리 없이 바로 구현 가능합니다.
- 출력 형식에 맞게 `??!`를 붙이는 것이 핵심입니다.

## Code

### C# 코드
```csharp
using System;

class Program {
  static void Main() {
    string name = Console.ReadLine();
    Console.WriteLine(name + "??!");
  }
}
```

### C++ 코드
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
