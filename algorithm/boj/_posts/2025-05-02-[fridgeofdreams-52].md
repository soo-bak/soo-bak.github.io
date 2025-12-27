---
layout: single
title: "[백준 11104] Fridge of Your Dreams (C#, C++) - soo:bak"
date: "2025-05-02 19:19:00 +0900"
description: 24비트 이진수 문자열을 입력받아 10진수로 변환하는 문제인 백준 11104번 Fridge of Your Dreams 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11104
  - C#
  - C++
  - 알고리즘
  - 구현
  - 수학
keywords: "백준 11104, 백준 11104번, BOJ 11104, fridgeofdreams, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11104번 - Fridge of Your Dreams](https://www.acmicpc.net/problem/11104)

## 설명
`24자리`의 이진수 문자열이 주어졌을 때, 이를 `10진수`로 변환하여 출력하는 문제입니다.<br>

<br>

## 접근법

- 먼저 테스트케이스의 수를 입력받습니다.
- 이후 각 테스트케이스마다 `24자리` 이진 문자열을 입력받아 처리합니다.
- 문자열의 왼쪽부터 오른쪽까지 차례로 순회하면서, <br>
  해당 자릿수가 `1`일 경우, `해당 위치의 2의 거듭제곱 값`을 더해줍니다.
- 최종적으로 계산한 `10진수`값을 출력합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    for (int i = 0; i < t; i++) {
      string binary = Console.ReadLine();
      int dec = 0;
      for (int j = 0; j < 24; j++) {
        if (binary[j] == '1')
          dec += 1 << (23 - j);
      }
      Console.WriteLine(dec);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int decBinary[24] = {1, };
  for (int i = 1; i < 24; i++)
    decBinary[i] = 2 * decBinary[i - 1];

  int t; cin >> t;
  while (t--) {
    string binary; cin >> binary;
    int dec = 0;
    for (int i = 0; i < 24; i++)
      dec += ((binary[i] - 48) * decBinary[24 - i - 1]);
    cout << dec << "\n";
  }

  return 0;
}
```
