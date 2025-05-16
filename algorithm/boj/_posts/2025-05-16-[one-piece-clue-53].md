---
layout: single
title: "[백준 12780] 원피스 (C#, C++) - soo:bak"
date: "2025-05-16 21:12:00 +0900"
description: 주어진 문자열에서 부분 문자열이 몇 번 등장하는지를 세는 백준 12780번 원피스 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[12780번 - 원피스](https://www.acmicpc.net/problem/12780)

## 설명

**긴 문자열 안에 주어진 특정 문자열이 얼마나 자주 등장하는지를 세는 간단한 문자열 탐색 문제입니다.**

문자열 `H`와 문자열 `N`이 주어졌을 때,

`H` 안에 `N`이 **겹쳐서 포함될 수 있도록** 몇 번 등장하는지를 구해야 합니다.

<br>
예를 들어 `ABABABA`와 `ABA`가 주어진 경우:
- `ABA`는 인덱스 `0`부터 한 번, 인덱스 `2`부터 한 번 → 총 `2`번 등장합니다.

<br>

## 접근법

문자열 전체를 왼쪽부터 차례대로 탐색하면서, 부분 문자열 `N`이 시작되는 위치를 찾아갑니다.

하나를 찾을 때마다 `해당 위치 바로 다음 칸`부터 다시 탐색을 이어가며,

이 과정을 문자열 끝까지 반복합니다.

이때 `N`이 겹쳐서 등장할 수도 있기 때문에, 중복을 허용하며 탐색을 계속해야 올바른 개수를 셀 수 있습니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string h = Console.ReadLine();
    string n = Console.ReadLine();

    int count = 0;
    int pos = 0;
    while ((pos = h.IndexOf(n, pos)) != -1) {
      count++;
      pos++;
    }

    Console.WriteLine(count);
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

  string s, t; cin >> s >> t;

  int count = 0;
  size_t pos = 0;
  while ((pos = s.find(t, pos)) != string::npos) {
    ++count;
    ++pos;
  }
  cout << count << "\n";

  return 0;
}
```
