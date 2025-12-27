---
layout: single
title: "[백준 5586] JOI와 IOI (C#, C++) - soo:bak"
date: "2025-04-20 00:55:00 +0900"
description: 문자열 내에서 JOI와 IOI의 등장 횟수를 각각 세는 백준 5586번 JOI와 IOI 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5586
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 5586, 백준 5586번, BOJ 5586, joiIoiCount, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5586번 - JOI와 IOI](https://www.acmicpc.net/problem/5586)

## 설명
**문자열에서 JOI와 IOI라는 두 패턴이 몇 번 등장하는지를 세는 간단한 문자열 탐색 문제**입니다.
<br>

- 하나의 문자열이 입력으로 주어집니다.
- 이 문자열 안에서 `"JOI"`라는 연속된 세 문자의 패턴이 몇 번 등장하는지 셉니다.
- 동시에 `"IOI"`라는 패턴이 몇 번 등장하는지도 세야 합니다.
<br>

- 두 패턴은 서로 겹쳐서 등장할 수 있습니다.
  예를 들어 `"JOIOI"`라는 문자열에서는 `"JOI"`는 한 번, `"IOI"`도 한 번 등장합니다.<br>
<br>

- 각 패턴의 등장 횟수를 **각각 별도로 계산**해서 출력해야 하며,
  첫 줄에는 `"JOI"`의 개수, 둘째 줄에는 `"IOI"`의 개수를 출력합니다.

## 접근법

1. 문자열을 입력받습니다.
2. 각 인덱스에서 시작하여 **연속된 세 글자**를 확인하며 `"JOI"` 또는 `"IOI"`인지 비교합니다.
3. 전체 문자열을 끝까지 순회하며 조건에 맞는 경우 각각 카운트를 증가시킵니다.
4. 모든 탐색이 끝난 후, `"JOI"`와 `"IOI"`의 개수를 차례로 출력합니다.

- 문자열 길이가 최대 100글자이므로 시간 복잡도는 `O(N)`으로 충분합니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string str = Console.ReadLine();
    int cntJOI = 0, cntIOI = 0;

    for (int i = 0; i <= str.Length - 3; i++) {
      if (str[i] == 'J' && str[i + 1] == 'O' && str[i + 2] == 'I')
        cntJOI++;
      if (str[i] == 'I' && str[i + 1] == 'O' && str[i + 2] == 'I')
        cntIOI++;
    }

    Console.WriteLine(cntJOI);
    Console.WriteLine(cntIOI);
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

  string str; cin >> str;
  int cntJOI = 0, cntIOI = 0;
  for (size_t i = 0; i < str.size(); i++) {
    if (str[i] == 'J' && str[i + 1] == 'O' && str[i + 2] == 'I')
      cntJOI++;
    if (str[i] == 'I' && str[i + 1] == 'O' && str[i + 2] == 'I')
      cntIOI++;
  }
  cout << cntJOI << "\n" << cntIOI << "\n";

  return 0;
}
```
