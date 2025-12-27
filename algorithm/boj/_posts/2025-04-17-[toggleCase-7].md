---
layout: single
title: "[백준 2744] 대소문자 바꾸기 (C#, C++) - soo:bak"
date: "2025-04-17 01:11:35 +0900"
description: 주어진 문자열의 각 문자의 대소문자를 반전시켜 출력하는 간단한 구현 문제인 백준 2744번 대소문자 바꾸기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2744
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 2744, 백준 2744번, BOJ 2744, toggleCase, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2744번 - 대소문자 바꾸기](https://www.acmicpc.net/problem/2744)

## 설명
**문자열에 포함된 모든 알파벳의 대소문자를 반전시켜 출력하는 간단한 구현 문제**입니다.<br>
<br>

- 소문자는 대문자로, 대문자는 소문자로 바꾸어 출력하면 됩니다.<br>
- 공백이나 숫자 없이 오직 영문자만 주어지므로, 조건 분기 처리가 간단합니다.<br>

### 접근법
- 문자열의 각 문자에 대해 대문자인지 소문자인지를 판별한 후,<br>
  해당 문자를 반대 케이스로 변환하여 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    string input = Console.ReadLine();
    char[] result = new char[input.Length];

    for (int i = 0; i < input.Length; i++) {
      if (char.IsUpper(input[i]))
        result[i] = char.ToLower(input[i]);
      else
        result[i] = char.ToUpper(input[i]);
    }

    Console.WriteLine(new string(result));
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
  for (size_t i = 0; i < str.size(); i++) {
    if (isupper(str[i])) str[i] += 32;
    else str[i] -= 32;
  }
  cout << str << "\n";

  return 0;
}
```
