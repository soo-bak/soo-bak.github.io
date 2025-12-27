---
layout: single
title: "[백준 13462] Battle Simulation (C#, C++) - soo:bak"
date: "2025-12-27 08:35:00 +0900"
description: 몬스터의 공격 문자열을 보고 대응 문자열을 생성하는 시뮬레이션 문제
---

## 문제 링크
[13462번 - Battle Simulation](https://www.acmicpc.net/problem/13462)

## 설명
몬스터의 공격 문자열이 주어질 때, 각 공격에 대응하는 방어 문자열을 만드는 문제입니다.

연속한 세 글자가 R, B, L을 모두 포함하면 C 하나로 대응합니다. 그 외에는 각 글자마다 R은 S, B는 K, L은 H로 대응합니다.

<br>

## 접근법
문자열을 왼쪽부터 순회하며 현재 위치에서 세 글자가 모두 다른 종류인지 확인합니다.

세 종류가 모두 있으면 C를 추가하고 세 칸 건너뜁니다. 아니면 해당 글자에 맞는 방어 문자를 추가하고 한 칸 이동합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var n = s.Length;
    var sb = new StringBuilder(n);
    var i = 0;
    while (i < n) {
      if (i + 2 < n) {
        char a = s[i], b = s[i + 1], c = s[i + 2];
        int mask = 0;
        if (a == 'R') mask |= 1;
        if (a == 'B') mask |= 2;
        if (a == 'L') mask |= 4;
        if (b == 'R') mask |= 1;
        if (b == 'B') mask |= 2;
        if (b == 'L') mask |= 4;
        if (c == 'R') mask |= 1;
        if (c == 'B') mask |= 2;
        if (c == 'L') mask |= 4;

        if (mask == 7) {
          sb.Append('C');
          i += 3;
          continue;
        }
      }

      char ch = s[i];
      sb.Append(ch == 'R' ? 'S' : ch == 'B' ? 'K' : 'H');
      i++;
    }

    Console.WriteLine(sb.ToString());
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
  int n = s.size();
  string res;
  res.reserve(n);

  int i = 0;
  while (i < n) {
    if (i + 2 < n) {
      int mask = 0;
      char a = s[i], b = s[i + 1], c = s[i + 2];
      if (a == 'R' || b == 'R' || c == 'R') mask |= 1;
      if (a == 'B' || b == 'B' || c == 'B') mask |= 2;
      if (a == 'L' || b == 'L' || c == 'L') mask |= 4;
      if (mask == 7) {
        res += 'C';
        i += 3;
        continue;
      }
    }
    char ch = s[i];
    if (ch == 'R') res += 'S';
    else if (ch == 'B') res += 'K';
    else res += 'H';
    i++;
  }

  cout << res << "\n";

  return 0;
}
```
