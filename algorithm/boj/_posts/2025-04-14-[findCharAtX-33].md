---
layout: single
title: "[백준 30877] X를 찾아서 (C#, C++) - soo:bak"
date: "2025-04-14 06:27:16 +0900"
description: 문자열에서 X의 위치를 찾아 해당 인덱스의 문자를 대문자로 출력하는 백준 30877번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[30877번 - X를 찾아서](https://www.acmicpc.net/problem/30877)

## 설명
각 테스트 케이스마다 두 문자열이 주어졌을 때,  <br>
**첫 번째 문자열에서 'X' 또는 'x'의 위치를 찾고**,  <br>
그 인덱스에 해당하는 **두 번째 문자열의 문자를 대문자로 출력**하는 문제입니다.

---

## 접근법
- 문자열 `s`에서 처음 등장하는 `'x'` 또는 `'X'`의 위치 `i`를 찾습니다.
- 문자열 `t[i]`가 소문자라면 대문자로 바꾸고, 대문자라면 그대로 출력합니다.
- 이를 각 테스트 케이스마다 반복합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Text;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      StringBuilder sb = new ();
      int n = int.Parse(Console.ReadLine());
      while (n-- > 0) {
        string[] input = Console.ReadLine().Split();
        string s = input[0], t = input[1];

        int idx = s.IndexOfAny(new char[] { 'x', 'X' });
        var c = t[idx];
        sb.Append(char.IsLower(c) ? char.ToUpper(c) : c);
      }
      Console.Write(sb.ToString());
    }
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
  cout.tie(nullptr);

  int n; cin >> n;
  while (n--) {
    string s, t; cin >> s >> t;

    int idx = 0;
    while (idx < s.length() && s[idx] != 'x' && s[idx] != 'X') idx++;

    if ('a' <= t[idx] && t[idx] <= 'z')
      cout << (char)(t[idx] - 32);
    else cout << t[idx];
  }

  return 0;
}
```
