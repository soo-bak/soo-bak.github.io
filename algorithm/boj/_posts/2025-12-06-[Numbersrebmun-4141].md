---
layout: single
title: "[백준 4141] Numbersrebmun (C#, C++) - soo:bak"
date: "2025-12-06 22:20:00 +0900"
description: 회사 이름을 전화키패드 숫자로 치환한 뒤 팰린드롬인지 확인하는 백준 4141번 Numbersrebmun 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 4141
  - C#
  - C++
  - 알고리즘
keywords: "백준 4141, 백준 4141번, BOJ 4141, Numbersrebmun, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4141번 - Numbersrebmun](https://www.acmicpc.net/problem/4141)

## 설명
회사 이름을 전화 키패드 숫자로 치환합니다. 2는 ABC, 3은 DEF, 4는 GHI, 5는 JKL, 6은 MNO, 7은 PQRS, 8은 TUV, 9는 WXYZ에 대응합니다.

치환한 숫자 문자열이 팰린드롬이면 YES, 아니면 NO를 출력하는 문제입니다.

<br>

## 접근법
먼저, 대소문자를 모두 대문자로 변환합니다.

다음으로, 문자별로 대응 숫자를 미리 배열로 만들어 상수 시간에 치환합니다.

이후, 치환된 숫자 문자열이 앞뒤 대칭인지 확인합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var preset = new[] { "ABC", "DEF", "GHI", "JKL", "MNO", "PQRS", "TUV", "WXYZ" };
      var map = new int[128];
      for (var p = 0; p < 8; p++) {
        foreach (var ch in preset[p])
          map[ch] = p + 2;
      }

      var t = int.Parse(Console.ReadLine()!);
      while (t-- > 0) {
        var s = Console.ReadLine()!.ToUpper();
        var digits = new char[s.Length];
        for (var i = 0; i < s.Length; i++)
          digits[i] = (char)('0' + map[s[i]]);

        var ok = true;
        for (int i = 0, j = digits.Length - 1; i < j; i++, j--) {
          if (digits[i] != digits[j]) {
            ok = false;
            break;
          }
        }
        Console.WriteLine(ok ? "YES" : "NO");
      }
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vs preset = {"ABC", "DEF", "GHI", "JKL", "MNO", "PQRS", "TUV", "WXYZ"};
  int mp[128] = {0};
  for (int p = 0; p < 8; p++) {
    for (char ch : preset[p])
      mp[(int)ch] = p + 2;
  }

  int T; cin >> T;
  while (T--) {
    string s; cin >> s;
    for (char &ch : s)
      ch = toupper(ch);

    string num;
    num.reserve(s.size());
    for (char ch : s)
      num.push_back('0' + mp[(int)ch]);

    bool ok = true;
    for (size_t i = 0, j = num.size() - 1; i < j; i++, j--) {
      if (num[i] != num[j]) {
        ok = false;
        break;
      }
    }
    cout << (ok ? "YES" : "NO") << "\n";
  }

  return 0;
}
```
