---
layout: single
title: "[백준 8892] 팰린드롬 (C#, C++) - soo:bak"
date: "2025-05-18 03:12:00 +0900"
description: 두 단어를 이어 붙여 팰린드롬을 만들 수 있는지를 확인하는 백준 8892번 팰린드롬 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[8892번 - 팰린드롬](https://www.acmicpc.net/problem/8892)

## 설명

**단어 목록에서 두 단어를 이어 붙여 만들 수 있는 팰린드롬 문자열을 찾는 문제입니다.**

<br>
각 테스트케이스는 `k`개의 단어로 구성되어 있으며,

이 중 서로 다른 두 단어를 이어 붙여 팰린드롬을 만들 수 있는지를 확인합니다.

- 단어의 순서는 임의이며,
- 단어 `A`와 `B`가 있을 때 `A + B` 혹은 `B + A` 형태 모두 고려할 수 있습니다.

<br>
가능한 팰린드롬이 있다면 그 중 하나를 출력하고,

없다면 `0`을 출력해야 합니다.

<br>

## 접근법

가장 단순하면서도 효과적인 방식은 **두 단어를 이어 붙여 직접 확인하는 완전 탐색**입니다.

- 주어진 단어들을 두 개씩 골라 이어 붙인 뒤,
- 해당 문자열이 팰린드롬인지 직접 확인합니다.

<br>
이를 위해 다음 절차를 따릅니다:

1. 주어진 단어 리스트를 순회하며, 가능한 모든 순서쌍을 고려합니다.
2. 두 단어를 이어 붙여 새 문자열을 만든 후,<br>
   이를 앞뒤에서 비교하며 팰린드롬 여부를 판별합니다.
3. 팰린드롬을 찾으면 즉시 출력하고, 더 이상의 탐색을 중단합니다.
4. 끝까지 탐색해도 찾을 수 없다면 `"0"`을 출력합니다.

<br>

---

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static bool IsPalindrome(string s) {
    int left = 0, right = s.Length - 1;
    while (left < right) {
      if (s[left++] != s[right--]) return false;
    }
    return true;
  }

  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      int n = int.Parse(Console.ReadLine());
      var words = new List<string>();
      for (int i = 0; i < n; i++)
        words.Add(Console.ReadLine());

      bool found = false;
      for (int i = 0; i < n && !found; i++) {
        for (int j = 0; j < n && !found; j++) {
          if (i == j) continue;
          string combined = words[i] + words[j];
          if (IsPalindrome(combined)) {
            Console.WriteLine(combined);
            found = true;
          }
        }
      }
      if (!found) Console.WriteLine("0");
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<string> vs;

bool isPalin(const string& s) {
  int left = 0, right = s.size() - 1;
  while (left < right) {
    if (s[left++] != s[right--])
      return false;
  }
  return true;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    vs words(n);
    for (string& w : words) cin >> w;

    bool found = false;
    for (int i = 0; i < n && !found; ++i) {
      for (int j = 0; j < n && !found; ++j) {
        if (i != j) {
          string s = words[i] + words[j];
          if (isPalin(s)) {
            cout << s << "\n";
            found = true;
          }
        }
      }
    }
    if (!found) cout << "0\n";
  }

  return 0;
}
```
