---
layout: single
title: "[백준 2774] 아름다운 수 (C#, C++) - soo:bak"
date: "2025-04-20 00:35:00 +0900"
description: 문자열에 등장하는 서로 다른 숫자의 개수를 구하는 백준 2774번 아름다운 수 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2774
  - C#
  - C++
  - 알고리즘
keywords: "백준 2774, 백준 2774번, BOJ 2774, beautifulNumber, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2774번 - 아름다운 수](https://www.acmicpc.net/problem/2774)

## 설명
**수에 포함된 서로 다른 숫자의 개수를 세는 간단한 구현 문제**입니다.
<br>

- 여러 개의 테스트케이스가 주어지며, 각 테스트케이스마다 하나의 수가 입력됩니다.
- 이 수는 **최대 100자리의 자연수**로, 일반적인 정수형 타입으로는 다룰 수 없기 때문에 **문자열로 읽어 처리해야 합니다.**
<br>

- 구해야 할 정답은 해당 수에 등장하는 **서로 다른 숫자의 개수**입니다.<br>
  예를 들어 `"1231"`이라는 수가 주어졌다면, `1`, `2`, `3`의 세 가지 숫자가 등장하므로 정답은 `3`이 됩니다.<br>

## 접근법

1. 입력으로 주어진 수를 문자열로 읽습니다.
2. `0`부터 `9`까지 각 숫자가 **등장했는지 여부를 저장할 수 있는 배열**을 만듭니다.
   - 총 10칸의 불리언 배열을 만들어, 특정 숫자가 처음 등장했을 때만 체크합니다.
3. 문자열을 끝까지 순회하며, **등장한 숫자의 개수만 세어 출력**합니다.
4. 각 테스트케이스마다 배열을 초기화하고, 정답을 계산해 출력합니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var seen = new bool[10];
      string num = Console.ReadLine();
      int cnt = 0;

      foreach (var ch in num) {
        int digit = ch - '0';
        if (!seen[digit]) {
          seen[digit] = true;
          cnt++;
        }
      }
      Console.WriteLine(cnt);
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
    bool sieve[10] = {0};
    string num; cin >> num;
    int ans = 0;
    for (size_t i = 0; i < num.size(); i++) {
      if (sieve[num[i] - 48]) continue;
      sieve[num[i] - 48] = true;
      ans++;
    }
    cout << ans << "\n";
  }

  return 0;
}
```
