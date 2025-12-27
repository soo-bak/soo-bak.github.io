---
layout: single
title: "[백준 5597] 과제 안 내신 분..? (C#, C++) - soo:bak"
date: "2025-04-19 20:07:01 +0900"
description: 1번부터 30번까지의 학생 중 과제를 제출하지 않은 2명의 번호를 찾는 백준 5597번 과제 안 내신 분..? 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5597
  - C#
  - C++
  - 알고리즘
keywords: "백준 5597, 백준 5597번, BOJ 5597, missingStudent, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5597번 - 과제 안 내신 분..?](https://www.acmicpc.net/problem/5597)

## 설명
**1번부터 30번까지 출석번호를 가진 학생 중, 제출하지 않은 2명의 출석번호를 찾는 문제**입니다.<br>
<br>

- 총 `30`명의 학생들 중 `28`명이 과제를 제출했습니다.<br>
- 제출한 학생들의 번호가 입력으로 주어지며, 오름차순이나 중복은 없습니다.<br>
- 제출하지 않은 `2`명의 번호를 오름차순으로 출력해야 합니다.<br>

### 접근법
- 총 30명의 학생 번호를 표시할 수 있도록 크기가 `30`인 불리언 배열을 선언합니다.<br>
- 처음에는 모든 값을 `false`로 두고, 입력된 번호에 해당하는 위치만 `true`로 바꿉니다.<br>
- 배열을 처음부터 끝까지 순회하면서 여전히 `false`인 위치의 번호(출석번호 + 1)를 출력하면 됩니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    bool[] submitted = new bool[30];
    for (int i = 0; i < 28; i++) {
      int num = int.Parse(Console.ReadLine());
      submitted[num - 1] = true;
    }

    for (int i = 0; i < 30; i++) {
      if (!submitted[i])
        Console.WriteLine(i + 1);
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

  bool sieve[30] = {0, };
  for (int i = 0; i < 28; i++) {
    int stud; cin >> stud;
    sieve[stud - 1] = true;
  }

  for (int i = 0; i < 30; i++) {
    if (!sieve[i])
      cout << i + 1 << "\n";
  }

  return 0;
}
```
