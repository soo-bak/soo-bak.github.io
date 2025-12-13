---
layout: single
title: "[백준 18409] 母音を数える (Counting Vowels) (C#, C++) - soo:bak"
date: "2025-12-13 13:02:00 +0900"
description: 문자열에서 모음 a,i,u,e,o의 개수를 세어 출력하는 백준 18409번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[18409번 - 母音を数える (Counting Vowels)](https://www.acmicpc.net/problem/18409)

## 설명
소문자 문자열에서 모음의 개수를 구하는 문제입니다.

<br>

## 접근법
문자열을 한 글자씩 확인하며 a, i, u, e, o 중 하나이면 개수를 증가시킵니다.

단순 조건문만으로 충분히 해결할 수 있습니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;
    var cnt = 0;
    foreach (char c in s)
      if (c == 'a' || c == 'i' || c == 'u' || c == 'e' || c == 'o') cnt++;
    Console.WriteLine(cnt);
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

  int n; cin >> n;
  string s; cin >> s;
  int cnt = 0;
  for (char c : s) {
    if (c == 'a' || c == 'i' || c == 'u' || c == 'e' || c == 'o') cnt++;
  }
  cout << cnt << "\n";

  return 0;
}
```
