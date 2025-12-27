---
layout: single
title: "[백준 11283] 한글 2 (C#, C++) - soo:bak"
date: "2025-11-21 23:53:00 +0900"
description: 입력된 한글 음절이 '가'로부터 몇 번째인지 계산하는 백준 11283번 한글 2 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11283
  - C#
  - C++
  - 알고리즘
keywords: "백준 11283, 백준 11283번, BOJ 11283, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11283번 - 한글 2](https://www.acmicpc.net/problem/11283)

## 설명

한글 음절 하나가 입력으로 주어질 때, 해당 음절이 '가'로부터 몇 번째인지 순서를 출력하는 문제입니다.

<br>

## 접근법

컴퓨터는 각 문자를 고유한 숫자로 표현하며, 유니코드에서 한글 음절은 '가'부터 '힣'까지 총 11,172개가 연속된 숫자로 배치되어 있습니다.

예를 들어 '가'는 44032번, '각'은 44033번, '힣'은 55203번입니다.

따라서 입력 음절의 숫자 값에서 '가'의 숫자 값을 빼면 0부터 시작하는 인덱스를 얻을 수 있고, 여기에 1을 더하면 1부터 시작하는 순서가 됩니다.

C#의 경우 `char.ConvertToUtf32`를 사용하여 문자를 숫자로 변환하며, C++의 경우 UTF-8 문자열을 UTF-32로 변환하여 숫자 값을 얻습니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var input = Console.ReadLine()!;
      var charValue = char.ConvertToUtf32(input, 0);
      var baseValue = char.ConvertToUtf32("가", 0);

      Console.WriteLine(charValue - baseValue + 1);
    }
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

  string s; cin >> s;

  wstring_convert<codecvt_utf8<char32_t>, char32_t> conv;
  char32_t ch = conv.from_bytes(s)[0];
  char32_t base = U'가';

  cout << (int)(ch - base + 1) << "\n";

  return 0;
}
```

