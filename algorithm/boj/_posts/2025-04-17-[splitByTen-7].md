---
layout: single
title: "[백준 11721] 열 개씩 끊어 출력하기 (C#, C++) - soo:bak"
date: "2025-04-17 01:10:35 +0900"
description: 입력된 문자열을 열 글자 단위로 나누어 출력하는 구현 문제인 백준 11721번 열 개씩 끊어 출력하기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11721
  - C#
  - C++
  - 알고리즘
keywords: "백준 11721, 백준 11721번, BOJ 11721, splitByTen, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11721번 - 열 개씩 끊어 출력하기](https://www.acmicpc.net/problem/11721)

## 설명
**입력된 문자열을 열 글자 단위로 끊어서 출력하는 간단한 문자열 출력 문제**입니다.<br>
<br>

- 공백 없이 연속된 문자열이 주어지고, 이를 `10`**글자씩 끊어서 줄바꿈**하며 출력해야 합니다.<br>
- 마지막 줄은 `10`글자가 되지 않아도 입력된 그대로 출력합니다.<br>

### 접근법
- 문자열을 입력받고, 인덱스를 기준으로 반복문을 수행하며 `10글자마다 줄바꿈` 처리합니다.<br>
- 또는 문자열 자르기 방식으로 `Substring()` 또는 `substr()`을 이용할 수도 있습니다.<br>

`C#` 코드는 문자열 자르기 방식으로, `C++` 코드는 인덱스를 활용하여 문자열의 길이를 판별하는 방식으로 풀이하였습니다. <br>
---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    string input = Console.ReadLine();

    for (int i = 0; i < input.Length; i += 10) {
      int len = Math.Min(10, input.Length - i);
      Console.WriteLine(input.Substring(i, len));
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string str; cin >> str;
  for (size_t i = 0; i < str.size(); i++) {
    cout << str[i];
    if ((i + 1) % 10 == 0) cout << "\n";
  }
  cout << "\n";

  return 0;
}
```
