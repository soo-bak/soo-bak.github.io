---
layout: single
title: "[백준 10987] 모음의 개수 (C#, C++) - soo:bak"
date: "2025-04-17 01:07:35 +0900"
description: 주어진 소문자 문자열에서 모음의 개수를 세는 간단한 문자열 문제인 백준 10987번 모음의 개수 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10987
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 10987, 백준 10987번, BOJ 10987, countVowels, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10987번 - 모음의 개수](https://www.acmicpc.net/problem/10987)

## 설명
**입력으로 주어지는 알파벳 소문자 문자열에서** `a`, `e`, `i`, `o`, `u`**모음이 몇 개 포함되어 있는지를 세는 문제**입니다.<br>
<br>

- 입력은 알파벳 소문자로 이루어진 단어이며, 공백이나 대문자는 포함되지 않습니다.<br>
- 문제에서 요구하는 모음은 `a`, `e`, `i`, `o`, `u`입니다.<br>
- 각 문자를 순회하며 모음인지 확인하고 개수를 세면 됩니다.<br>

### 접근법
- 모음을 판별하는 보조 함수를 만들어 `a`, `e`, `i`, `o`, `u`인지 비교합니다.<br>
- 전체 문자열을 한 글자씩 검사하며, 모음일 경우 카운트를 증가시킵니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static bool IsVowel(char c) =>
    c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';

  static void Main() {
    string word = Console.ReadLine();
    int count = 0;

    foreach (char c in word)
      if (IsVowel(c)) count++;

    Console.WriteLine(count);
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

bool isVowel(const char& c) {
  if (c == 'a' || c == 'e' || c == 'i' ||
      c == 'o' || c == 'u') return true;
  else return false;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string word; cin >> word;
  int cnt = 0;
  for (size_t i = 0; i < word.size(); i++) {
    if (isVowel(word[i])) cnt++;
  }
  cout << cnt << "\n";

  return 0;
}
```
