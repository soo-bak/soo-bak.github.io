---
layout: single
title: "[백준 1550] 16진수 (C#, C++) - soo:bak"
date: "2025-04-19 00:14:10 +0900"
description: 입력된 16진수 문자열을 10진수로 변환하여 출력하는 간단한 진법 변환 문제인 백준 1550번 16진수 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1550번 - 16진수](https://www.acmicpc.net/problem/1550)

## 설명
**16진수 형태로 입력된 문자열을 10진수 정수로 변환하는 단순한 진법 변환 문제**입니다.<br>
<br>

- 입력으로 하나의 16진수 문자열이 주어집니다.<br>
- 이 값을 10진수로 변환하여 출력하면 됩니다.<br>
- 숫자와 알파벳 대문자(`A`~`F`)가 혼합될 수 있으며, 입력 값은 항상 유효합니다.<br>

### 접근법
- 문자열을 16진수로 해석하여 10진수로 변환합니다.<br>
<br>

`C#`에서는 `Convert.ToInt32(문자열, 16)`을 사용하여 동일하게 처리할 수 있습니다.<br>
<br>
`C++`에서는 `stoi(문자열, nullptr, 16)`을 사용하면 16진수 해석이 가능합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    string hex = Console.ReadLine();
    int num = Convert.ToInt32(hex, 16);
    Console.WriteLine(num);
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string str; cin >> str;
  cout << stoi(str, nullptr, 16) << "\n";

  return 0;
}
```
