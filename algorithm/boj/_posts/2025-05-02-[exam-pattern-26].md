---
layout: single
title: "[백준 10874] 이교수님의 시험 (C#, C++) - soo:bak"
date: "2025-05-02 06:16:00 +0900"
description: 정답 패턴을 기반으로 부정행위 가능성이 있는 만점자를 판별하는 백준 10874번 이교수님의 시험 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10874
  - C#
  - C++
  - 알고리즘
keywords: "백준 10874, 백준 10874번, BOJ 10874, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10874번 - 이교수님의 시험](https://www.acmicpc.net/problem/10874)

## 설명
시험 문제의 정답이 일정한 패턴을 따르는 상황에서,

**정답을 모두 맞힌 학생**을 찾아서 리스트업하는 문제입니다.

<br>
정답 패턴은 다음과 같습니다:

- 문제 번호 `j`에 대해 정답은 $$(j - 1) \mod 5 + 1$$
- 즉, 정답은 다음과 같이 반복됩니다: `1 2 3 4 5 1 2 3 4 5`

학생의 답안이 이 패턴과 정확히 일치하는 경우,

해당 학생은 **모든 문제를 정답으로 마킹한 것**이므로 재시험 대상자가 됩니다.

<br>

## 접근법

- 먼저 정답 패턴 `1 2 3 4 5 1 2 3 4 5`를 기준 배열로 고정합니다.
- 각 학생의 제출 답안을 입력받고, 정답 패턴과 일치하는지 비교합니다.
- 완벽히 일치하는 학생의 번호를 출력합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int[] correct = new int[10];
    for (int i = 0; i < 10; i++)
      correct[i] = i % 5 + 1;

    int n = int.Parse(Console.ReadLine());
    for (int i = 1; i <= n; i++) {
      var input = Console.ReadLine().Split();
      bool perfect = true;
      for (int j = 0; j < 10; j++) {
        if (int.Parse(input[j]) != correct[j]) {
          perfect = false;
          break;
        }
      }
      if (perfect) Console.WriteLine(i);
    }
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

  int ans[10];
  for (int i = 0; i < 10; i++)
    ans[i] = i % 5 + 1;

  int cntStud; cin >> cntStud;
  for (int s = 0; s < cntStud; s++) {
    int submits[10];
    bool isPerfect = true;
    for (int i = 0; i < 10; i++) {
      cin >> submits[i];
      if (submits[i] != ans[i]) isPerfect = false;
    }
    if (isPerfect) cout << s + 1 << "\n";
  }

  return 0;
}
```
