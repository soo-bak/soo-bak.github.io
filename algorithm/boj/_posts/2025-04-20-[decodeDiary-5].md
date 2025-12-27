---
layout: single
title: "[백준 2954] 창영이의 일기장 (C#, C++) - soo:bak"
date: "2025-04-20 04:06:00 +0900"
description: 창영이가 암호화한 모음 + p + 모음 패턴을 해독하여 원래 문장을 복원하는 백준 2954번 창영이의 일기장 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2954
  - C#
  - C++
  - 알고리즘
keywords: "백준 2954, 백준 2954번, BOJ 2954, decodeDiary, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2954번 - 창영이의 일기장](https://www.acmicpc.net/problem/2954)

## 설명
**문제에 주어지는 암호화 방식에 따라 주어진 문자열을 해독하여 원래 문장을 복호화하여 출력하는 문제입니다.**
<br>

- 암호화 방식은 다음과 같습니다:
  - 모음 (a, e, i, o, u) → `모음 + 'p' + 같은 모음` 으로 변환.
  - 자음은 그대로 사용.

예시:
- 암호: `apa` → 원문: `a`
- 암호: `bapa` → 원문: `ba`

## 접근법

1. 문자열을 한 줄 입력받습니다.
2. 문자열을 왼쪽부터 한 글자씩 순회합니다.
3. `현재 문자가 모음`이고, `다음 문자가 'p'`, `그 다음이 현재 문자와 같다면` → 한 글자로 복원하고 `3칸` 건너뜁니다.
4. 그렇지 않다면 그대로 출력하고 한 글자만 이동합니다.


## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string s = Console.ReadLine();
    for (int i = 0; i < s.Length;) {
      if ("aeiou".Contains(s[i]) && i + 2 < s.Length && s[i + 1] == 'p' && s[i + 2] == s[i]) {
        Console.Write(s[i]);
        i += 3;
      } else {
        Console.Write(s[i]);
        i++;
      }
    }
    Console.WriteLine();
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

  string s;
  getline(cin, s);
  for (size_t i = 0; i < s.size();)
    if (string("aeiou").find(s[i]) != string::npos && i + 2 < s.size() && s[i + 1] == 'p' && s[i + 2] == s[i])
      cout << s[i], i += 3;
    else cout << s[i], i++;
  cout << "\n";

  return 0;
}
```
