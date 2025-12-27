---
layout: single
title: "[백준 15680] 연세대학교 (C#, C++) - soo:bak"
date: "2025-04-14 04:51:24 +0900"
description: 입력값에 따라 조건 분기하여 출력하는 간단한 구현 문제인 백준 15680번 연세대학교 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 15680
  - C#
  - C++
  - 알고리즘
keywords: "백준 15680, 백준 15680번, BOJ 15680, yonseiOutput, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15680번 - 연세대학교](https://www.acmicpc.net/problem/15680)

## 설명
이 문제는 `0` 또는 `1` 중 하나의 숫자가 주어졌을 때,  <br>
해당 값에 따라 **특정 문구를 출력하는 조건 분기 구현 문제**입니다.

- 입력이 `0`이면 `"YONSEI"`를 출력
- 입력이 `1`이면 `"Leading the Way to the Future"`를 출력

---

## 접근법
- 조건문을 통해 입력이 `1`인 경우와 아닌 경우를 구분하여 출력만 잘 해주면 되는 간단한 구현 문제입니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int num = int.Parse(Console.ReadLine()!);
      Console.WriteLine(num == 1 ? "Leading the Way to the Future" : "YONSEI");
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <iostream>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int num; cin >> num;
  if (num) cout << "Leading the Way to the Future\n";
  else cout << "YONSEI\n";

  return 0;
}
```
