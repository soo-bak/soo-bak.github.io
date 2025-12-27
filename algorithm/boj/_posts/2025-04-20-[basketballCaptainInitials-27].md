---
layout: single
title: "[백준 1159] 농구 경기 (C#, C++) - soo:bak"
date: "2025-04-20 03:58:00 +0900"
description: 농구 선수들의 이름 중 첫 글자를 기준으로 5명 이상이 있는 알파벳을 찾아 출력하는 백준 1159번 농구 경기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1159
  - C#
  - C++
  - 알고리즘
keywords: "백준 1159, 백준 1159번, BOJ 1159, basketballCaptainInitials, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1159번 - 농구 경기](https://www.acmicpc.net/problem/1159)

## 설명
**농구 선수들의 이름을 확인하여, 동일한 알파벳으로 시작하는 이름이** `5`**명 이상 있는 알파벳들을 출력하는 문제입니다.**
<br>

- 첫 줄에 입력되는 이름의 수가 주어집니다.
- 이어지는 각 줄마다 선수 이름이 하나씩 주어집니다.
- 이름의 첫 글자를 기준으로 같은 글자가 `5`명 이상 존재한다면, 해당 글자를 결과에 포함시킵니다.
- 조건을 만족하는 알파벳이 없다면 `PREDAJA`를 출력합니다.


## 접근법

1. 이름의 개수를 입력받습니다.
2. 각 이름에 대해 `첫 글자의 등장 횟수`를 저장합니다.
3. 알파벳별 등장 횟수를 순회하며 `5`회 이상 등장한 알파벳을 정답 문자열에 추가합니다.
4. 정답 문자열이 비어 있다면 `PREDAJA`를 출력하고, 그렇지 않으면 정렬된 문자열을 출력합니다.


## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var count = new int[26];
    for (int i = 0; i < n; i++) {
      string name = Console.ReadLine();
      count[name[0] - 'a']++;
    }

    string result = string.Concat(
      Enumerable.Range(0, 26)
        .Where(i => count[i] >= 5)
        .Select(i => (char)(i + 'a'))
    );

    Console.WriteLine(string.IsNullOrEmpty(result) ? "PREDAJA" : result);
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
  int cnt[26] = {};
  while (n--) {
    string s; cin >> s;
    cnt[s[0] - 'a']++;
  }

  string ans;
  for (int i = 0; i < 26; i++)
    if (cnt[i] >= 5) ans += 'a' + i;

  cout << (ans.empty() ? "PREDAJA" : ans) << "\n";

  return 0;
}
```
