---
layout: single
title: "[백준 1213] 팰린드롬 만들기 (C++ 풀이) - soo:bak"
date: "2025-05-18 02:52:43 +0900"
description: 주어진 문자열로 사전순 가장 빠른 팰린드롬을 만들 수 있는지 판단하고 구성하는 백준 1213번 팰린드롬 만들기 문제의 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1213
  - C++
  - 알고리즘
keywords: "백준 1213, 백준 1213번, BOJ 1213, C++ 풀이, 알고리즘"
---

## 문제 링크
[1213번 - 팰린드롬 만들기](https://www.acmicpc.net/problem/1213)

## 설명

**주어진 문자열의 알파벳을 재배열하여 팰린드롬을 만들 수 있는지 판단하고,**

**가능하다면 사전순으로 가장 앞서는 팰린드롬을 출력하는 문제입니다.**

<br>
팰린드롬은 앞에서부터 읽든 뒤에서부터 읽든 동일한 문자열을 의미하며,

이를 만들기 위해서는 다음과 같은 조건을 만족해야 합니다:
- 문자열 길이가 짝수인 경우: **모든 알파벳의 개수가 짝수**여야 합니다.
- 문자열 길이가 홀수인 경우: **한 가지 알파벳만 홀수 개수**를 가질 수 있으며, 나머지는 모두 짝수여야 합니다.

<br>

## 접근법

먼저 입력 문자열의 각 알파벳 개수를 셉니다.

이 때, **홀수 개수의 알파벳이 2개 이상 존재하는 경우**에는 팰린드롬을 만들 수 없습니다.

<br>

그 외의 경우에는 다음과 같이 구성합니다:
1. **왼쪽 절반**: 알파벳 순서대로 절반만큼의 문자를 추가합니다.<br>
   예를 들어 `C`가 `4번` 나온다면 `"CC"`를 추가합니다.
2. **가운데 문자**: 홀수 개수의 알파벳이 존재한다면, 해당 문자를 중앙에 `1개` 추가합니다.
3. **오른쪽 절반**: 왼쪽 절반의 역순을 그대로 이어 붙입니다.

<br>
이렇게 구성하면 팰린드롬 구조를 유지하면서도,

**가장 앞쪽 알파벳부터 선택하여 사전순으로 가장 빠른 문자열**이 됩니다.

<br>

---
## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string input = Console.ReadLine();
    int[] count = new int[26];

    foreach (char c in input)
      count[c - 'A']++;

    int odd = 0;
    foreach (int x in count)
      if (x % 2 != 0) odd++;

    if (odd > 1) {
      Console.WriteLine("I'm Sorry Hansoo");
      return;
    }

    string first = "", mid = "";
    for (int i = 0; i < 26; i++) {
      if (count[i] % 2 != 0)
        mid += (char)(i + 'A');
      first += new string((char)(i + 'A'), count[i] / 2);
    }

    char[] arr = first.ToCharArray();
    Array.Reverse(arr);
    string second = new string(arr);

    Console.WriteLine(first + mid + second);
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

  int count[26] = {};

  string s; cin >> s;
  for (char c : s)
    ++count[c - 'A'];

  int odd = 0;
  for (int i = 0; i < 26; ++i)
    if (count[i] % 2) ++odd;

  if (odd > 1) {
    cout << "I'm Sorry Hansoo\n";
    return 0;
  }

  string ans = "";
  for (int i = 0; i < 26; ++i)
    ans += string(count[i] / 2, 'A' + i);
  for (int i = 0; i < 26; ++i)
    if (count[i] % 2) ans += 'A' + i;
  for (int i = 25; i >= 0; --i)
    ans += string(count[i] / 2, 'A' + i);

  cout << ans << "\n";

  return 0;
}
```
