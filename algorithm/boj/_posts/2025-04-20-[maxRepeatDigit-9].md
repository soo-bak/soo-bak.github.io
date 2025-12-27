---
layout: single
title: "[백준 2495] 연속구간 (C#, C++) - soo:bak"
date: "2025-04-20 01:12:00 +0900"
description: 세 줄의 숫자 문자열에서 가장 많이 연속해서 등장하는 숫자의 개수를 구하는 백준 2495번 연속구간 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2495
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 2495, 백준 2495번, BOJ 2495, maxRepeatDigit, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2495번 - 연속구간](https://www.acmicpc.net/problem/2495)

## 설명
**세 줄의 숫자 문자열이 주어졌을 때, 같은 숫자가 연속해서 등장하는 가장 긴 길이를 구하는 문자열 처리 문제**입니다.
<br>

- 총 `3`개의 줄이 주어지며, 각 줄은 숫자로만 이루어진 문자열입니다.
- 각 줄마다 **연속해서 등장하는 동일한 숫자의 최대 길이**를 구하여 출력해야 합니다.
- 예를 들어 `12224445` 라는 문자열이 있다면 `4`가 연속으로 3번 등장하므로 결과는 `3`입니다.

## 접근법

1. 총 `3`개의 문자열을 반복문을 통해 한 줄씩 입력받습니다.
2. 각 문자열마다:
   - 현재 문자가 이전 문자와 같다면 연속 길이를 증가시킵니다.
   - 다르면 연속 길이를 `1`로 초기화합니다.
   - 최대 연속 길이를 저장하여 갱신합니다.
3. 각 줄마다 최대 길이를 출력합니다.

- `i`번째 문자와 `i - 1`번째 문자를 비교하는 방식으로 처리합니다.
- 각 문자열에 대해 한 번만 순차적으로 순회하면서 인접한 문자를 비교하므로, 문자열 하나에 대해 수행되는 연산은 **O(N)**입니다.<br>
  총 `3`개의 줄이 주어지므로 전체 연산은 `3 × O(N) = O(N)` 수준이며,<br>
  여기서 `N`의 최대값은 `100`이므로, 전체 연산량은 약 `300`번 이내로 매우 적은 수준입니다.<br>

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    for (int t = 0; t < 3; t++) {
      string line = Console.ReadLine();
      int count = 1, max = 1;

      for (int i = 1; i < line.Length; i++) {
        if (line[i] == line[i - 1]) {
          count++;
          if (count > max) max = count;
        } else count = 1;
      }

      Console.WriteLine(max);
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

  for (int t = 0; t < 3; t++) {
    string num; cin >> num;
    size_t size = 1, maxSize = 1;
    for (size_t i = 1; i < num.size(); i++) {
      if (num[i] == num[i - 1]) {
        size++;
        maxSize = max(maxSize, size);
      } else size = 1;
    }
    cout << maxSize << "\n";
  }

  return 0;
}
```
