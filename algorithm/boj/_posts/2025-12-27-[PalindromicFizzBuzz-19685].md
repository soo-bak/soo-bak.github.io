---
layout: single
title: "[백준 19685] Palindromic FizzBuzz (C#, C++) - soo:bak"
date: "2025-12-27 12:25:00 +0900"
description: 구간 [S,E] 숫자를 출력하되 회문이면 Palindrome!을 출력하는 문제
---

## 문제 링크
[19685번 - Palindromic FizzBuzz](https://www.acmicpc.net/problem/19685)

## 설명
주어진 구간의 각 정수를 한 줄씩 출력하되, 회문수라면 숫자 대신 Palindrome!을 출력하는 문제입니다.

<br>

## 접근법
각 숫자를 문자열로 변환해 앞뒤가 대칭인지 검사합니다.

회문이면 지정된 문자열을, 아니면 숫자를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static bool IsPal(long x) {
    var s = x.ToString();
    var l = 0;
    var r = s.Length - 1;
    while (l < r) {
      if (s[l++] != s[r--]) return false;
    }
    return true;
  }

  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var s = long.Parse(parts[0]);
    var e = long.Parse(parts[1]);
    var sb = new StringBuilder();
    for (var x = s; x <= e; x++) {
      if (IsPal(x)) sb.AppendLine("Palindrome!");
      else sb.AppendLine(x.ToString());
    }
    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

bool isPal(ll x) {
  string str = to_string(x);
  int l = 0;
  int r = (int)str.size() - 1;
  while (l < r) {
    if (str[l++] != str[r--]) return false;
  }
  return true;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll s, e; cin >> s >> e;

  for (ll x = s; x <= e; x++) {
    if (isPal(x)) cout << "Palindrome!\n";
    else cout << x << "\n";
  }

  return 0;
}
```
