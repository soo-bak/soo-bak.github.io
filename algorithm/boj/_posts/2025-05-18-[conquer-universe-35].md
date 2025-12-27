---
layout: single
title: "[백준 1237] 정ㅋ벅ㅋ (C#, C++) - soo:bak"
date: "2025-05-18 21:14:00 +0900"
description: 출력 조건에 맞게 고정된 문자열만을 출력하는 백준 1237번 정ㅋ벅ㅋ 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1237
  - C#
  - C++
  - 알고리즘
keywords: "백준 1237, 백준 1237번, BOJ 1237, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1237번 - 정ㅋ벅ㅋ](https://www.acmicpc.net/problem/1237)

## 설명

이 문제는 **고정된 문자열을 출력하는 것만으로 정답이 되는 단순 출력 문제**입니다.

<br>
문제에서는 ‘입력 따위 필요 없다’고 명시되어 있으며,  
출력으로는 **"문제의 정답"**이라는 문자열을 한 줄로 출력해야 합니다.

입력이나 조건 분기 없이, 주어진 문장을 그대로 출력하는 것이 요구됩니다.

<br>

## 접근법

입력은 주어지지 않기 때문에, `입력 처리` 코드는 필요 없습니다.

<br>
출력은 단 한 줄로 `"문제의 정답"`이라는 문장을 그대로 출력하면 됩니다.

- 줄 끝에 공백 없이
- 띄어쓰기 포함하여 정확히 `"문제의 정답"` 형태로 출력

이 문제는 단순 출력 구조로, 문자열 하나만 정확히 출력하면 정답이 되므로  
별도의 연산이나 조건 처리 없이 `Console.WriteLine` 또는 `cout`을 이용해 문자열을 출력하면 됩니다.

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine("문제의 정답");
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

  cout << "문제의 정답";

  return 0;
}
```
