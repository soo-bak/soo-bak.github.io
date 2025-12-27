---
layout: single
title: "[백준 3059] 등장하지 않는 문자의 합 (C#, C++) - soo:bak"
date: "2025-04-20 02:01:00 +0900"
description: 문자열에 등장하지 않은 알파벳의 아스키 코드 합을 구하는 백준 3059번 등장하지 않는 문자의 합 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 3059
  - C#
  - C++
  - 알고리즘
keywords: "백준 3059, 백준 3059번, BOJ 3059, missingAlphabetSum, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3059번 - 등장하지 않는 문자의 합](https://www.acmicpc.net/problem/3059)

## 설명
**주어진 문자열에 등장하지 않은 알파벳 대문자들의 아스키 코드값의 총합을 구하는 문제**입니다.
<br>

- 먼저 테스트케이스의 개수가 주어지고, 이어서 각 테스트케이스마다 하나의 문자열이 입력됩니다.
- 각 문자열은 모두 대문자로만 구성되어 있습니다.
- 문자열에 포함되지 않은 알파벳(A~Z)에 대해, 해당 알파벳의 아스키 코드값을 모두 더한 값을 출력합니다.

## 접근법

1. 테스트케이스 수를 입력받습니다.
2. 각 문자열에 대해, 알파벳 등장 여부를 저장할 배열(크기 26)을 초기화합니다.
3. 문자열의 각 문자를 순회하며 해당 알파벳의 등장 여부를 기록합니다.
4. 등장하지 않은 알파벳에 대해, `i + 65`를 이용하여 아스키 코드값을 더합니다.
5. 총합을 출력합니다.

- `A`의 아스키 코드값은 `65`이고, `Z`는 `90`입니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());

    while (t-- > 0) {
      string str = Console.ReadLine();
      var seen = new bool[26];
      foreach (var c in str)
        seen[c - 'A'] = true;

      int sum = 0;
      for (int i = 0; i < 26; i++)
        if (!seen[i]) sum += (char)('A' + i);

      Console.WriteLine(sum);
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

  int t; cin >> t;
  while (t--) {
    int cntAlpha[26] = {0, }, ans = 0;
    string str; cin >> str;
    for (auto i : str)
      cntAlpha[i - 65]++;

    for (int i = 0; i < 26; i++) {
      if (!cntAlpha[i]) ans += i + 65;
    }

    cout << ans << "\n";
  }

  return 0;
}
```
