---
layout: single
title: "[백준 24606] Double Password (C#, C++) - soo:bak"
date: "2025-12-06 22:10:00 +0900"
description: 두 4자리 비밀번호에서 자리별로 선택 가능한 숫자 수를 곱해 로그인 가능한 경우의 수를 구하는 백준 24606번 Double Password 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[24606번 - Double Password](https://www.acmicpc.net/problem/24606)

## 설명
두 개의 4자리 비밀번호가 있고, 입력한 4자리 수가 각 자리에서 두 비밀번호 중 하나와 일치하면 로그인됩니다.

자리별로 가능한 숫자 수를 곱해 전체 경우의 수를 구하는 문제입니다. 두 비밀번호의 해당 자리가 같다면 선택지는 1개, 다르면 선택지는 2개입니다.

<br>

## 접근법
먼저, 두 비밀번호를 문자열로 읽습니다.

다음으로, 자리마다 두 비밀번호의 해당 자리가 동일하면 1을 곱하고, 다르면 2를 곱합니다.

이후, 곱셈 결과를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var a = Console.ReadLine()!;
      var b = Console.ReadLine()!;

      var ways = 1;
      for (var i = 0; i < 4; i++)
        ways *= (a[i] == b[i]) ? 1 : 2;

      Console.WriteLine(ways);
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

  string s1, s2; cin >> s1 >> s2;
  int ways = 1;
  for (int i = 0; i < 4; i++)
    ways *= (s1[i] == s2[i]) ? 1 : 2;

  cout << ways << "\n";

  return 0;
}
```
