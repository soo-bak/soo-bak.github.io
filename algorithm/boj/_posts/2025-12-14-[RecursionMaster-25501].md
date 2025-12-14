---
layout: single
title: "[백준 25501] 재귀의 귀재 (C#, C++) - soo:bak"
date: "2025-12-14 09:03:00 +0900"
description: 재귀로 팰린드롬을 판정하며 호출 횟수를 함께 출력하는 백준 25501번 재귀의 귀재 문제의 C#/C++ 풀이
---

## 문제 링크
[25501번 - 재귀의 귀재](https://www.acmicpc.net/problem/25501)

## 설명
재귀로 팰린드롬을 검사하면서 함수 호출 횟수를 함께 출력하는 문제입니다.

팰린드롬 여부(1 또는 0)와 호출 횟수를 공백으로 구분해 출력합니다.

<br>

## 접근법
재귀 함수가 호출될 때마다 카운터를 증가시킵니다.

좌우 문자가 다르면 0을 반환하고, 인덱스가 겹치거나 지나치면 1을 반환합니다.

각 테스트케이스마다 카운터를 초기화한 뒤 재귀 함수를 호출하고, 결과와 호출 횟수를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int cnt;

  static int Rec(string s, int l, int r) {
    cnt++;
    if (l >= r) return 1;
    if (s[l] != s[r]) return 0;
    return Rec(s, l + 1, r - 1);
  }

  static int IsPalindrome(string s) => Rec(s, 0, s.Length - 1);

  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < t; i++) {
      var s = Console.ReadLine()!;
      cnt = 0;
      var res = IsPalindrome(s);
      Console.WriteLine($"{res} {cnt}");
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int cnt;

int recursion(const string& s, int l, int r) {
  cnt++;
  if (l >= r) return 1;
  if (s[l] != s[r]) return 0;
  return recursion(s, l + 1, r - 1);
}

int isPalindrome(const string& s) {
  return recursion(s, 0, (int)s.size() - 1);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    string s; cin >> s;
    cnt = 0;
    int res = isPalindrome(s);
    cout << res << " " << cnt << "\n";
  }

  return 0;
}
```
