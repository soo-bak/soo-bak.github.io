---
layout: single
title: "[백준 28295] 팀명 정하기 2 (C#, C++) - soo:bak"
date: "2025-04-29 05:12:00 +0900"
description: 여러 후보 중 소문자가 많고 글자 수가 적으며 숫자가 아닌 글자가 포함된 팀명을 고르는 백준 28295번 팀명 정하기 2 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[28295번 - 팀명 정하기 2](https://www.acmicpc.net/problem/28295)

## 설명
여러 개의 팀명 후보가 주어졌을 때, 정해진 조건을 모두 만족하는 팀명을 찾는 문제입니다.

팀명은 다음 세 가지 조건을 모두 만족해야 합니다:

- 알파벳 대문자보다 소문자가 더 많이 등장해야 합니다.
- 팀명의 길이는 `10`글자 이하여야 합니다.
- 숫자가 아닌 문자가 하나 이상 포함되어 있어야 합니다.

입력으로 주어진 후보들 중 조건을 모두 만족하는 팀명을 하나 출력합니다.

문제에서 항상 정답은 유일하게 존재한다고 보장합니다.

<br>

## 접근법

각 팀명 후보를 하나씩 확인하면서 다음 과정을 거칩니다.

- 팀명의 길이가 `10`글자 이하여야 하므로, 이를 초과하는 경우 제외합니다.
- 알파벳 소문자의 개수와 대문자의 개수를 각각 센 뒤, 대문자의 수가 소문자의 수보다 많으면 제외합니다.
- 팀명을 구성하는 문자들 중 숫자가 아닌 글자가 하나 이상 존재해야 하며, 숫자와 하이픈(`'-'`)만 있을 경우 제외합니다.

모든 조건을 만족하는 팀명을 탐색하여 출력합니다.


## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());

    for (int i = 0; i < n; i++) {
      string s = Console.ReadLine();

      if (s.Length > 10) continue;

      int lower = 0, upper = 0, hyphen = 0;
      foreach (char c in s) {
        if ('a' <= c && c <= 'z') lower++;
        else if ('A' <= c && c <= 'Z') upper++;
        else if (c == '-') hyphen++;
      }

      if (lower < upper) continue;
      if (lower + upper + hyphen == 0) continue;

      Console.WriteLine(s);
      return;
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
  cin.ignore();

  while (n--) {
    string s; getline(cin, s);

    if (s.length() > 10) continue;

    int lower = 0, upper = 0, hyphen = 0;
    for (char c : s) {
      if ('a' <= c && c <= 'z') lower++;
      else if ('A' <= c && c <= 'Z') upper++;
      else if (c == '-') hyphen++;
    }

    if (lower < upper) continue;
    if (lower + upper + hyphen == 0) continue;

    cout << s << "\n";
    return 0;
  }

  return 0;
}
```
