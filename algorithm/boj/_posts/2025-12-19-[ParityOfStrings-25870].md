---
layout: single
title: "[백준 25870] Parity of Strings (C#, C++) - soo:bak"
date: "2025-12-19 22:47:00 +0900"
description: 모든 문자의 등장 횟수가 짝수면 0, 모두 홀수면 1, 그렇지 않으면 2를 출력하는 단순 카운팅 문제
---

## 문제 링크
[25870번 - Parity of Strings](https://www.acmicpc.net/problem/25870)

## 설명
문자열이 주어질 때, 각 문자의 등장 횟수가 모두 짝수면 0, 모두 홀수면 1, 그 외에는 2를 출력하는 문제입니다.

<br>

## 접근법
알파벳 26칸 빈도 배열로 각 문자의 등장 횟수를 셉니다.

이후 등장한 문자들 중 짝수인 개수와 홀수인 개수를 세어 조건에 맞게 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;

    var freq = new int[26];
    foreach (var c in s)
      freq[c - 'a']++;

    var letters = 0;
    var even = 0;
    var odd = 0;
    for (var i = 0; i < 26; i++) {
      if (freq[i] == 0) continue;
      letters++;
      if ((freq[i] & 1) == 0) even++;
      else odd++;
    }

    if (even == letters) Console.WriteLine(0);
    else if (odd == letters) Console.WriteLine(1);
    else Console.WriteLine(2);
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

  int freq[26] = {0};
  for (char c : s)
    freq[c - 'a']++;

  int letters = 0, even = 0, odd = 0;
  for (int i = 0; i < 26; i++) {
    if (freq[i] == 0) continue;
    letters++;
    if (freq[i] % 2 == 0) even++;
    else odd++;
  }

  if (even == letters) cout << 0 << "\n";
  else if (odd == letters) cout << 1 << "\n";
  else cout << 2 << "\n";

  return 0;
}
```
