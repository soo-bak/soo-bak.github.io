---
layout: single
title: "[백준 10384] 팬그램 (C++, C#) - soo:bak"
date: "2025-05-02 19:42:00 +0900"
description: 문자열에 등장하는 알파벳 빈도를 세어 팬그램, 더블 팬그램, 트리플 팬그램을 구분하는 백준 10384번 팬그램 문제의 C++ 및 C# 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10384
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 10384, 백준 10384번, BOJ 10384, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10384번 - 팬그램](https://www.acmicpc.net/problem/10384)

## 설명
입력으로 주어진 문자열이 **팬그램(Pangram)**인지, 또는 **더블 팬그램(Double pangram)**, **트리플 팬그램(Triple pangram)**인지 판별하는 문제입니다.

<br>
각 알파벳이 등장하는 횟수에 따라 아래와 같이 분류합니다:

- 모든 알파벳이 한 번 이상 등장 → `"Pangram!"`
- 모든 알파벳이 두 번 이상 등장 → `"Double pangram!!"`
- 모든 알파벳이 세 번 이상 등장 → `"Triple pangram!!!"`
- 이 외의 경우는 `"Not a pangram"`

<br>

## 접근법

- 각 테스트케이스마다 알파벳의 등장 횟수를 세기 위해 `크기 26`의 배열을 선언합니다.
- 대소문자 구분 없이 알파벳만 필터링하여 소문자로 변환한 뒤, 등장 횟수를 누적합니다.
- 누적된 횟수 중 **가장 적게 등장한 알파벳의 개수를 기준으로** 판별합니다.
- 결과는 `"Case i: "` 형식으로 출력하며, 테스트케이스 번호를 함께 표시합니다.

<br>

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());

    for (int i = 1; i <= t; i++) {
      var line = Console.ReadLine();
      var freq = new int[26];

      foreach (char c in line) {
        if (char.IsLetter(c))
          freq[char.ToLower(c) - 'a']++;
      }

      int minCount = freq.Min();

      string result = minCount switch {
        0 => "Not a pangram",
        1 => "Pangram!",
        2 => "Double pangram!!",
        _ => "Triple pangram!!!"
      };

      Console.WriteLine($"Case {i}: {result}");
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

  string s; getline(cin, s);
  int t = stoi(s);

  for (int i = 1; i <= t; i++) {
    getline(cin, s);
    int cnt[26] = {0, };

    for (char c : s)
      if (isalpha(c)) cnt[tolower(c) - 'a']++;

    int minCnt = 4;
    for (int x : cnt)
      minCnt = min(minCnt, x);

    string ans;
    if (minCnt == 0) ans = "Not a pangram";
    else if (minCnt == 1) ans = "Pangram!";
    else if (minCnt == 2) ans = "Double pangram!!";
    else ans = "Triple pangram!!!";

    cout << "Case " << i << ": " << ans << "\n";
  }

  return 0;
}
```
