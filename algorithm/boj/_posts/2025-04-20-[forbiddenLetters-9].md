---
layout: single
title: "[백준 2789] 유학 금지 (C#, C++) - soo:bak"
date: "2025-04-20 01:08:00 +0900"
description: 특정 문자열에 포함된 알파벳을 제거하고 출력하는 백준 2789번 유학 금지 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[2789번 - 유학 금지](https://www.acmicpc.net/problem/2789)

## 설명
**문자열에서 특정 문자들을 제거하여 출력하는 간단한 구현 문제**입니다.
<br>

- 입력으로 주어진 문자열에서 `CAMBRIDGE`에 포함된 모든 알파벳들을 제거한 결과를 출력해야 합니다.
- `CAMBRIDGE`에 포함된 문자는 다음과 같습니다: `C`, `A`, `M`, `B`, `R`, `I`, `D`, `G`, `E`
- 이 문자들이 포함되어 있으면 제거하고, 나머지 문자만을 순서대로 출력합니다.

## 접근법

1. 입력 문자열을 읽어옵니다.
2. `CAMBRIDGE`라는 문자열에 포함된 문자인지를 판별할 기준으로 사용합니다.
3. 입력 문자열의 각 문자를 순회하며:
   - `CAMBRIDGE`에 포함되지 않은 경우만 출력합니다.
4. 최종적으로 남은 문자들을 공백 없이 그대로 출력합니다.

<br>

## 코드

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var forbidden = "CAMBRIDGE";
    var input = Console.ReadLine();
    var result = new string(input.Where(c => !forbidden.Contains(c)).ToArray());
    Console.WriteLine(result);
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

  string inspect = "CAMBRIDGE";
  string str; cin >> str;
  for (size_t i = 0; i < str.size(); i++) {
    bool isI = false;
    for (auto c: inspect) {
      if (str[i] == c) isI = true;
    }
    if (!isI) cout << str[i];
  }
  cout << "\n";

  return 0;
}
```
