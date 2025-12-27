---
layout: single
title: "[백준 9366] 삼각형 분류 (C#, C++) - soo:bak"
date: "2025-05-05 03:13:00 +0900"
description: 세 변의 길이에 따라 삼각형의 종류를 분류하고, 조건을 만족하지 않으면 invalid를 출력하는 백준 9366번 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9366
  - C#
  - C++
  - 알고리즘
keywords: "백준 9366, 백준 9366번, BOJ 9366, triangleclassify, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9366 - 삼각형 분류](https://www.acmicpc.net/problem/9366)

## 설명

세 개의 길이가 주어졌을 때,

삼각형을 만들 수 있는지, 만들 수 있다면 삼각형의 종류는 무엇인지를 분류하는 문제입니다.

<br>
삼각형을 구성하기 위해서는 가장 긴 변의 길이가 나머지 두 변의 길이 합보다 작아야 하며,

이 조건이 성립하지 않으면 삼각형이 될 수 없습니다.

<br>
삼각형이 되는 경우는 다음 세 가지 중 하나로 분류됩니다:

- **정삼각형** (`equilateral`): 세 변의 길이가 모두 같은 경우
- **이등변삼각형** (`isosceles`): 두 변의 길이만 같은 경우
- **부등변삼각형** (`scalene`): 세 변의 길이가 모두 다른 경우

<br>

## 접근법

- 테스트케이스의 개수를 먼저 입력받습니다.
- 각 테스트마다 세 변의 길이를 입력받습니다.
- 세 변을 비교하기 위해 오름차순으로 정렬합니다.
- 정렬된 순서로 삼각형이 가능한지 판별합니다:
  - 가장 긴 변의 길이보다 앞의 두 변의 합이 작거나 같다면 **삼각형 불가** → `"invalid!"`
- 삼각형이 가능한 경우, 다음 기준에 따라 종류를 분류합니다:
  - 세 변이 모두 같다면 `"equilateral"`
  - 두 변만 같다면 `"isosceles"`
  - 모두 다르다면 `"scalene"`

<br>
각 테스트케이스는 `"Case #x: 결과"` 형식으로 출력해야 하며, 번호는 `1`부터 시작합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    for (int i = 1; i <= t; i++) {
      var s = Console.ReadLine().Split().Select(int.Parse).ToArray();
      Array.Sort(s);

      string result = s[0] + s[1] <= s[2] ? "invalid!" :
                      s[0] == s[1] && s[1] == s[2] ? "equilateral" :
                      s[0] == s[1] || s[1] == s[2] ? "isosceles" : "scalene";

      Console.WriteLine($"Case #{i}: {result}");
    }
  }
}
```
### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

bool isTri(int a, int b, int c) {
  return a + b > c;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  for (int i = 1; i <= t; i++) {
    int s[3]; cin >> s[0] >> s[1] >> s[2];
    sort(s, s + 3);

    string ans = !isTri(s[0], s[1], s[2]) ? "invalid!" :
                 s[0] == s[1] && s[1] == s[2] ? "equilateral" :
                 s[0] == s[1] || s[1] == s[2] ? "isosceles" : "scalene";

    cout << "Case #" << i << ": " << ans << "\n";
  }

  return 0;
}
```
