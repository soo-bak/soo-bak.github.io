---
layout: single
title: "[백준 11145] Is it a Number? (C++, C#) - soo:bak"
date: "2025-05-18 17:31:00 +0900"
description: 입력 문자열이 정수인지 판별하는 백준 11145번 Is it a Number? 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11145
  - C#
  - C++
  - 알고리즘
keywords: "백준 11145, 백준 11145번, BOJ 11145, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11145번 - Is it a Number?](https://www.acmicpc.net/problem/11145)

## 설명

**공백이 포함된 입력 문자열이 주어졌을 때, 이 문자열이 올바른 정수인지 판별하는 문제입니다.**

입력값은 앞뒤에 공백이 있을 수 있으며, 내부는 오직 숫자로만 구성되어야 합니다.

양의 정수만 허용되며, 부호나 소수점 등의 기호가 포함되어 있으면 안 됩니다.

<br>
올바른 입력일 경우 숫자만 출력하며, 그 외에는 `"invalid input"`을 출력합니다.

<br>

## 접근법

입력 문자열을 읽은 뒤, 다음 순서로 처리합니다:

- 문자열 양 끝의 공백을 제거합니다.
- 제거한 문자열이 모두 숫자로만 구성되어 있는지 확인합니다.
  - 하나라도 숫자가 아닌 문자가 포함되어 있다면 `"invalid input"`입니다.
- 앞쪽에 붙은 `0`이 여러 개 있는 경우에는 제거한 뒤 출력합니다.
  - 단, `0`만 있는 경우는 그대로 `"0"`을 출력합니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      string s = Console.ReadLine().Trim();

      if (s.Length == 0 || !IsAllDigits(s)) {
        Console.WriteLine("invalid input");
        continue;
      }

      s = s.TrimStart('0');
      Console.WriteLine(s.Length == 0 ? "0" : s);
    }
  }

  static bool IsAllDigits(string s) {
    foreach (char c in s)
      if (!char.IsDigit(c)) return false;
    return true;
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
  cin.ignore();

  while (t--) {
    string s; getline(cin, s);

    size_t start = s.find_first_not_of(" ");
    if (start == string::npos) {
      cout << "invalid input\n";
      continue;
    }

    size_t end = s.find_last_not_of(" ");
    s = s.substr(start, end - start + 1);

    bool valid = true;
    for (char c : s)
      if (!isdigit(c)) {
        valid = false;
        break;
      }

    if (!valid) {
      cout << "invalid input\n";
      continue;
    }

    size_t non_zero = s.find_first_not_of('0');
    cout << (non_zero == string::npos ? "0" : s.substr(non_zero)) << "\n";
  }

  return 0;
}
```
