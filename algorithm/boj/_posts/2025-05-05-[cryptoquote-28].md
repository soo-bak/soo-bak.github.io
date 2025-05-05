---
layout: single
title: "[백준 2703] Cryptoquote (C++, C#) - soo:bak"
date: "2025-05-05 18:09:00 +0900"
description: 대문자 알파벳 변환 규칙에 따라 암호화된 문장을 복호화하는 문자열 처리 문제, 백준 2703번 Cryptoquote 문제의 C++ 및 C# 풀이 및 해설
---

## 문제 링크
[2703번 - Cryptoquote](https://www.acmicpc.net/problem/2703)

## 설명

알파벳 치환 규칙에 따라 주어진 암호문을 복호화하는 문자열 치환 문제입니다.

- 각 테스트케이스마다 **암호화된 문자열**과 **알파벳 치환 규칙**이 주어집니다.
- 주어지는 길이가 `26`인 대문자 문자열에서,<br>
  `i`번째 문자는 알파벳 순서상 `i`번째 문자(`A=0`, `B=1`, `...`, `Z=25`)를 치환한 결과를 의미합니다.
- 알파벳이 아닌 문자(공백)는 그대로 유지해야 하며, 알파벳은 규칙에 따라 치환하여 출력해야 합니다.

## 접근법

- 각 테스트케이스마다 두 줄의 입력이 주어집니다:
  1. 암호화된 문장
  2. 변환 테이블 (`26자`)
- 알파벳 `A`부터 `Z`까지의 변환 테이블을 구성해두고, <br>
  암호문 내 문자를 하나씩 확인하면서 변환 테이블에 따라 변경합니다.
- 공백 문자는 변환 대상이 아니므로 그대로 유지해야 하며,<br>
  알파벳만 변환 대상임에 유의합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var encrypted = Console.ReadLine();
      var table = Console.ReadLine();

      var res = new char[encrypted.Length];
      for (int i = 0; i < encrypted.Length; i++) {
        char c = encrypted[i];
        res[i] = char.IsLetter(c) ? table[c - 'A'] : c;
      }

      Console.WriteLine(new string(res));
    }
  }
}
```

<br>

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
    string s, table; getline(cin, s); getline(cin, table);

    char code[26];
    for (int i = 0; i < 26; i++)
      code[i] = table[i];

    for (char& c : s) {
      if (isalpha(c))
        c = code[c - 'A'];
    }

    cout << s << "\n";
  }

  return 0;
}
```
