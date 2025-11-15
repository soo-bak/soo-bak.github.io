---
layout: single
title: "[백준 15000] CAPS (C#, C++) - soo:bak"
date: "2025-11-15 01:55:00 +0900"
description: 입력 문자열을 모두 대문자로 변환해 출력하는 백준 15000번 CAPS 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[15000번 - CAPS](https://www.acmicpc.net/problem/15000)

## 설명

소문자로만 이루어진 문자열이 주어질 때, 모든 문자를 대문자로 변환하여 출력하는 문제입니다.<br>

<br>

## 접근법

ASCII 코드 변환을 사용하여 해결합니다.

소문자 'a'의 ASCII 코드는 `97`, 대문자 'A'는 `65`이므로 둘의 차이는 `32`입니다. 모든 알파벳 소문자와 대문자는 이 관계가 동일합니다.

<br>
각 문자에서 `32`를 빼거나 `'A' - 'a'`를 더하면 소문자를 대문자로 변환할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var input = Console.ReadLine()!;
      var result = new StringBuilder();

      foreach (var ch in input)
        result.Append((char)(ch - 32));

      Console.WriteLine(result);
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
  for (char& ch : s)
    ch -= 32;

  cout << s << "\n";

  return 0;
}
```

