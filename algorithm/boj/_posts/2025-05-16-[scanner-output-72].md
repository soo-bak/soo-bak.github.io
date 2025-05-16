---
layout: single
title: "[백준 3035] 스캐너 (C#, C++) - soo:bak"
date: "2025-05-16 19:53:00 +0900"
description: 각 문자를 지정된 배율만큼 확대하여 전체 행렬을 출력하는 백준 3035번 스캐너 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[3035번 - 스캐너](https://www.acmicpc.net/problem/3035)

## 설명

**신문 기사의 각 문자를 행과 열 방향으로 확대 출력하는 문제입니다.**

주어진 문서는 `R × C` 크기의 문자 행렬로 표현되며,

스캐너는 각 문자를 `ZR × ZC` 배율로 확대하여 새로 출력합니다.

<br>
즉, 원래 문서의 각 문자가:

- 행 방향으로 `ZR`배
- 열 방향으로 `ZC`배

확대되어 전체 크기가 `R × ZR` 행과 `C × ZC` 열의 행렬로 바뀌는 결과를 출력해야 합니다.

<br>

## 접근법

입력으로 주어지는 원본 문서의 각 문자는 그대로 유지되며,

단지 **행과 열을 각각 배율만큼 복제하여 확대 출력**하는 시뮬레이션 문제입니다.

<br>
이를 구현하기 위해서 다음과 같이 처리합니다:

- 먼저 원본 문서의 각 줄을 문자열로 저장합니다.
- 이후 전체 확대된 출력 행에 대해:
  - 인덱스를 `ZR`로 나눈 몫을 통해 원본 문서의 어떤 행인지 확인하고,
  - 각 열 문자 역시 `ZC`로 나눈 몫을 통해 원본에서 어떤 열 문자인지를 구합니다.
- 이때, `i / ZR`, `j / ZC`를 통해 원래 문서의 좌표를 역참조합니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine().Split();
    int r = int.Parse(parts[0]);
    int c = int.Parse(parts[1]);
    int zr = int.Parse(parts[2]);
    int zc = int.Parse(parts[3]);

    var original = new string[r];
    for (int i = 0; i < r; i++)
      original[i] = Console.ReadLine();

    for (int i = 0; i < r * zr; i++) {
      for (int j = 0; j < c * zc; j++)
        Console.Write(original[i / zr][j / zc]);
      Console.WriteLine();
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int r, c, zr, zc; cin >> r >> c >> zr >> zc;
  vs paper(r);
  for (auto& s : paper) cin >> s;

  for (int i = 0; i < r * zr; ++i) {
    for (int j = 0; j < c * zc; ++j)
      cout << paper[i / zr][j / zc];
    cout << "\n";
  }

  return 0;
}
```
