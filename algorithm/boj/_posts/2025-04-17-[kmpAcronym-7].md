---
layout: single
title: "[백준 2902] KMP는 왜 KMP일까? (C#, C++) - soo:bak"
date: "2025-04-17 01:06:35 +0900"
description: 하이픈으로 구분된 단어의 약어를 추출하여 출력하는 간단한 문자열 처리 문제인 백준 2902번 KMP는 왜 KMP일까? 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2902
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 2902, 백준 2902번, BOJ 2902, kmpAcronym, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2902번 - KMP는 왜 KMP일까?](https://www.acmicpc.net/problem/2902)

## 설명
**대문자와 하이픈으로 구성된 문자열에서 각 단어의 첫 글자만 추출하여 약어 형태로 출력하는 간단한 문자열 문제**입니다.<br>
<br>

- 입력 문자열은 여러 단어가 `-`로 구분된 형태입니다.<br>
- 각 단어의 **첫 글자만 추출**하여 연결한 문자열을 출력하면 됩니다.<br>
- 모든 단어는 대문자로 시작하므로, 하이픈 이후 등장하는 문자가 첫 글자가 됩니다.<br>

### 접근법
- 첫 글자는 무조건 포함되므로 따로 처리합니다.<br>
- 문자열을 순회하면서 `'-'` 문자를 만나면, 그 다음 글자를 약어에 포함시킵니다.<br>
- 누적한 결과를 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    string input = Console.ReadLine();
    Console.Write(input[0]);
    for (int i = 1; i < input.Length - 1; i++) {
      if (input[i] == '-')
        Console.Write(input[i + 1]);
    }
    Console.WriteLine();
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

  cout << str[0];
  for (size_t i = 1; i < str.size() - 1; i++) {
    if (str[i] == '-')
      cout << str[i + 1];
  }
  cout << "\n";

  return 0;
}
```
