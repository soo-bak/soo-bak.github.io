---
layout: single
title: "[백준 1342] 행운의 문자열 (C#, C++) - soo:bak"
date: "2025-05-18 00:01:00 +0900"
description: 서로 다른 문자 배치를 통해 인접한 문자가 중복되지 않는 행운의 문자열의 개수를 구하는 백준 1342번 행운의 문자열 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1342
  - C#
  - C++
  - 알고리즘
  - 브루트포스
  - set
  - 백트래킹
keywords: "백준 1342, 백준 1342번, BOJ 1342, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1342번 - 행운의 문자열](https://www.acmicpc.net/problem/1342)

## 설명

**문자열 S를 재배치하여 인접한 문자가 모두 다르게 되는 경우의 수를 구하는 문제입니다.**

<br>
문자열에 포함된 문자를 이용해 만들 수 있는 가능한 모든 순열 중에서,

**같은 문자가 연속으로 등장하지 않는 경우만 유효한 조합으로 인정**됩니다.

즉, 각 문자 간의 위치를 바꿔 구성할 수 있는 모든 문자열 중에서 **연속된 문자가 하나도 없는 경우의 수**를 계산하는 것이 목적입니다.

<br>
원래 주어진 문자열이 이 조건을 만족한다면, 그 경우도 정답에 포함됩니다.

<br>

## 접근법

문자열의 길이가 10 이하로 매우 짧기 때문에,

모든 가능한 문자의 배치를 직접 생성하며 조건을 만족하는 경우만 세어도 충분합니다.

<br>
하지만 주의할 점은 다음과 같습니다:
- 문자열에 **같은 문자가 여러 번 등장할 수 있으므로**,<br>
  단순한 순열 생성 방식은 **중복된 경우**를 포함하게 됩니다.
- 또한, **인접한 문자가 같아지는 배치는 허용되지 않기 때문에**<br>
  탐색 도중 이 조건을 반드시 확인해야 합니다.

<br>
이러한 조건을 만족하기 위해, 다음과 같은 방식으로 모든 배치를 탐색합니다:
1. 알파벳 빈도 배열을 만들어 각 문자가 몇 번 등장하는지를 기록합니다.
2. 백트래킹 방식의 완전탐색을 수행하며 한 글자씩 채워갑니다.
  - 이때 직전에 사용한 문자와 같은 문자는 건너뛰어, 인접 문자가 같아지는 경우를 방지합니다.
3. 문자열의 길이만큼 문자를 모두 선택했다면, 조건을 만족한 하나의 경우로 판단하고 정답 개수를 증가시킵니다.
4. 탐색을 마친 후에는, **사용한 문자를 다시 복구**하여 다른 경우의 수를 탐색할 수 있도록 합니다.

<br>
문자열의 길이가 작기 때문에 이러한 방식으로도 충분히 모든 가능한 배치를 검사할 수 있습니다.

<br>

> 참고 : [백트래킹(Backtracking)의 개념과 구조적 사고 - soo:bak](https://soo-bak.github.io/algorithm/theory/backTracking/)

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static int ans = 0;
  static int[] count = new int[26];

  static void Backtrack(int idx, int len, char last) {
    if (idx == len) {
      ans++;
      return;
    }

    for (int i = 0; i < 26; i++) {
      if (count[i] > 0 && last != (char)(i + 'a')) {
        count[i]--;
        Backtrack(idx + 1, len, (char)(i + 'a'));
        count[i]++;
      }
    }
  }

  static void Main() {
    string s = Console.ReadLine();
    foreach (char c in s)
      count[c - 'a']++;

    Backtrack(0, s.Length, (char)0);
    Console.WriteLine(ans);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int ans = 0;

void backtrack(size_t idx, size_t len, char last, int* count) {
  if (idx == len) {
    ++ans;
    return;
  }

  for (int i = 0; i < 26; ++i) {
    if (count[i] && last != 'a' + i) {
      --count[i];
      backtrack(idx + 1, len, 'a' + i, count);
      ++count[i];
    }
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int count[26] = {};

  string s; cin >> s;
  for (char c : s)
    ++count[c - 'a'];

  backtrack(0, s.size(), 0, count);

  cout << ans << "\n";

  return 0;
}
```
