---
layout: single
title: "[백준 1076] 저항 (C#, C++) - soo:bak"
date: "2025-04-20 03:26:00 +0900"
description: 저항 색 코드 3개를 입력받아 이를 숫자로 변환하고 최종 저항값을 계산하는 백준 1076번 저항 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1076번 - 저항](https://www.acmicpc.net/problem/1076)

## 설명
`3`**개의 색깔이 주어졌을 때, 저항의 값을 계산하는 문제입니다.**
<br>

- 전자 저항은 세 가지 색으로 표현됩니다:
  - 첫 번째 색: 저항의 값
  - 두 번째 색: 저항의 값
  - 세 번째 색: 곱해지는 배수 (10의 거듭제곱)

예시:
- 입력: `yellow`(4) `violet`(7) `red`(2)
  → 계산: $$(4 \times 10 + 7) \times 10^2 = 4700$$

## 접근법

1. 색상과 숫자 값을 대응시키는 자료구조를 생성합니다.
2. `3`개의 색을 순서대로 입력받고, 각각의 저항값으로 변환하여 다음과 같이 계산합니다.
3. 계산식:
   - 앞 두 자리: $$A \times 10 + B$$
   - 전체 값: $$(A \times 10 + B) \times 10^C$$
4. 계산 결과를 출력합니다.


## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var map = new Dictionary<string, int> {
      ["black"] = 0, ["brown"] = 1, ["red"] = 2, ["orange"] = 3, ["yellow"] = 4,
      ["green"] = 5, ["blue"] = 6, ["violet"] = 7, ["grey"] = 8, ["white"] = 9
    };

    string s1 = Console.ReadLine();
    string s2 = Console.ReadLine();
    string s3 = Console.ReadLine();

    long value = (map[s1] * 10L + map[s2]) * (long)Math.Pow(10, map[s3]);
    Console.WriteLine(value);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;
typedef long long ll;
typedef map<string, int> msi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  msi table = {
    {"black", 0}, {"brown", 1}, {"red", 2}, {"orange", 3}, {"yellow", 4},
    {"green", 5}, {"blue", 6}, {"violet", 7}, {"grey", 8}, {"white", 9}
  };

  string s1, s2, s3; cin >> s1 >> s2 >> s3;
  ll value = (table[s1] * 10LL + table[s2]) * pow(10, table[s3]);

  cout << value << "\n";

  return 0;
}
```
