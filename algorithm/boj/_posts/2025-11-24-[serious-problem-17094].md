---
layout: single
title: "[백준 17094] Serious Problem (C#, C++) - soo:bak"
date: "2025-11-24 23:25:00 +0900"
description: 문자열에서 문자 2와 e의 빈도를 비교해 더 많은 쪽을 출력하고, 같으면 yee를 출력하는 백준 17094번 Serious Problem 문제의 C# 및 C++ 풀이
---

## 문제 링크
[17094번 - Serious Problem](https://www.acmicpc.net/problem/17094)

## 설명

문자 2와 e로만 이루어진 문자열이 주어집니다.

문자열의 길이와 문자열이 주어질 때, 두 문자 중 더 많이 등장한 문자를 출력하는 문제입니다.

두 문자의 등장 횟수가 같으면 yee를 출력합니다.

<br>

## 접근법

문자열을 한 번 순회하며 문자 2와 e의 등장 횟수를 각각 셉니다.

예를 들어, 문자열이 "2ee2e"라면 2가 2번, e가 3번 등장합니다.

<br>
두 문자의 등장 횟수를 비교하여 결과를 출력합니다.

2의 횟수가 더 많으면 2를 출력하고, e의 횟수가 더 많으면 e를 출력하며, 같으면 yee를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var s = Console.ReadLine()!;

      var cnt2 = 0;
      var cntE = 0;

      foreach (var ch in s) {
        if (ch == '2') cnt2++;
        else cntE++;
      }

      if (cnt2 > cntE) Console.WriteLine("2");
      else if (cnt2 < cntE) Console.WriteLine("e");
      else Console.WriteLine("yee");
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

  int n; cin >> n;
  string s; cin >> s;

  int cnt2 = 0, cntE = 0;

  for (char ch : s) {
    if (ch == '2') cnt2++;
    else cntE++;
  }

  if (cnt2 > cntE) cout << "2\n";
  else if (cnt2 < cntE) cout << "e\n";
  else cout << "yee\n";

  return 0;
}
```

