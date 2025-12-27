---
layout: single
title: "[백준 4592] 중복을 없애자 (C#, C++) - soo:bak"
date: "2025-05-04 18:09:00 +0900"
description: 연속된 수를 제거하여 중복을 없애는 백준 4592번 중복을 없애자 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 4592
  - C#
  - C++
  - 알고리즘
keywords: "백준 4592, 백준 4592번, BOJ 4592, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4592번 - 중복을 없애자](https://www.acmicpc.net/problem/4592)

## 설명

**중복된 제출값을 제거하고, 연속된 값이 반복되지 않도록 필터링한 결과를 출력하는 문제입니다.**

한 줄마다 `수의 개수`와 `제출된 수들`이 주어지며, 각 줄에 대해 **연속해서 중복된 수를 하나만 남기고 출력**해야 합니다.

<br>
각 줄의 끝에는 항상 `'$'` 문자를 붙여야 하며, 입력은 `0`을 입력받을 때까지 계속해서 처리합니다.

<br>

## 접근법

- 한 줄의 시작에 `수의 개수`가 주어지고, 그 뒤를 이어 제출된 수들이 입력됩니다.
- 입력된 수를 차례대로 확인하며, **바로 직전에 추가한 수와 다를 경우에만 추가**합니다.
- 각 줄의 출력 마지막에는 공백 뒤에 `'$'`를 출력합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    while (true) {
      var input = Console.ReadLine();
      if (input == null) break;

      var parts = input.Split(' ', StringSplitOptions.RemoveEmptyEntries);
      int n = int.Parse(parts[0]);
      if (n == 0) break;

      var res = new List<int>();
      res.Add(int.Parse(parts[1]));

      for (int i = 2; i <= n; i++) {
        int cur = int.Parse(parts[i]);
        if (cur != res[^1])
          res.Add(cur);
      }

      Console.WriteLine(string.Join(" ", res) + " $");
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  while (true) {
    int num; cin >> num;
    if (!num) break ;

    int init; cin >> init;
    vi choco;
    choco.push_back(init);
    for (int i = 1; i < num; i++) {
      int submit; cin >> submit;
      if (submit != choco.back())
        choco.push_back(submit);
    }
    for (size_t i = 0; i < choco.size(); i++)
      cout << choco[i] << " ";
    cout << "$\n";
  }

  return 0;
}
```
