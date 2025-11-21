---
layout: single
title: "[백준 1526] 가장 큰 금민수 (C#, C++) - soo:bak"
date: "2025-05-16 20:12:00 +0900"
description: 4와 7로만 이루어진 수 중 N 이하인 가장 큰 수를 탐색하는 백준 1526번 가장 큰 금민수 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1526번 - 가장 큰 금민수](https://www.acmicpc.net/problem/1526)

## 설명

**정수** `N` **이하에서** `4`**와** `7`**로만 이루어진 가장 큰 수를 찾는 문제입니다.**

문제의 설명에 따라, 금민수란 숫자를 이루는 모든 자릿수가 **오직 4 또는 7**로만 구성된 수를 의미합니다.

예를 들어, `474`, `77`, `444`는 금민수이고, `78`, `123`, `470`은 금민수가 아닙니다.

주어진 정수 `N`이 있을 때, `N` **이하이면서 가장 큰 금민수**를 출력해야 합니다.

<br>

## 접근법

가장 간단하고도 효율적인 방법은 `N`**부터** `4`**까지 거꾸로 내려가며 조건을 만족하는지 검사**하는 것입니다.

- 숫자 `i`를 문자열로 변환하여 각 자리수를 확인합니다.
- 각 자리의 문자가 `4` 또는 `7`이 아닌 경우는 제외하고,
- 모든 자릿수가 `4` 또는 `7`인 경우에 해당 수를 출력합니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static bool IsAns(string s) {
    foreach (char c in s)
      if (c != '4' && c != '7') return false;
    return true;
  }

  static void Main() {
    int n = int.Parse(Console.ReadLine());
    for (int i = n; i >= 4; i--) {
      if (IsAns(i.ToString())) {
        Console.WriteLine(i);
        break;
      }
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

bool isAns(int n) {
  string s = to_string(n);
  for (char c : s)
    if (c != '4' && c != '7') return false;
  return true;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  for (int i = n; i >= 4; --i)
    if (isAns(i)) {
      cout << i << "\n";
      break;
    }

  return 0;
}
```
