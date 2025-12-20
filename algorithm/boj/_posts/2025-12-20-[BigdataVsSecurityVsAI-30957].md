---
layout: single
title: "[백준 30957] 빅데이터 vs 정보보호 vs 인공지능 (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: B, S, A 응답을 집계해 최다 관심 분야를 출력하는 문제
---

## 문제 링크
[30957번 - 빅데이터 vs 정보보호 vs 인공지능](https://www.acmicpc.net/problem/30957)

## 설명
B, S, A로 표기된 학생들의 관심 분야 응답이 주어질 때, 가장 많은 응답을 받은 분야를 출력하는 문제입니다. 최다 분야가 여러 개면 B, S, A 순서로 이어서 출력하고, 세 분야가 모두 같으면 SCU를 출력합니다.

<br>

## 접근법
문자열을 순회하면서 각 분야별 응답 수를 집계합니다. 세 분야의 응답 수가 모두 같으면 SCU를 출력합니다.

그렇지 않으면 최댓값을 구하고, 해당 값과 같은 분야를 B, S, A 순서로 결과 문자열에 추가합니다. 이 순서를 지켜야 동점일 때 올바른 출력이 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    Console.ReadLine();
    var s = Console.ReadLine()!;

    var b = 0;
    var ss = 0;
    var a = 0;
    foreach (var ch in s) {
      if (ch == 'B') b++;
      else if (ch == 'S') ss++;
      else if (ch == 'A') a++;
    }

    if (b == ss && ss == a) {
      Console.WriteLine("SCU");
      return;
    }

    var mx = Math.Max(b, Math.Max(ss, a));
    var res = "";
    if (b == mx) res += "B";
    if (ss == mx) res += "S";
    if (a == mx) res += "A";

    Console.WriteLine(res);
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

  int b = 0, ss = 0, a = 0;
  for (char c : s) {
    if (c == 'B') b++;
    else if (c == 'S') ss++;
    else if (c == 'A') a++;
  }

  if (b == ss && ss == a) {
    cout << "SCU\n";
    return 0;
  }

  int mx = max(b, max(ss, a));
  string res;
  if (b == mx) res.push_back('B');
  if (ss == mx) res.push_back('S');
  if (a == mx) res.push_back('A');

  cout << res << "\n";

  return 0;
}
```
