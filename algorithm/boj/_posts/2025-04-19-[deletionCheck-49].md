---
layout: single
title: "[백준 9243] 파일 삭제 (C#, C++) - soo:bak"
date: "2025-04-19 20:29:16 +0900"
description: 홀수 번째 삭제 시 비트 반전을 고려하여 문자열 비교를 수행하는 백준 9243번 파일 삭제 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9243
  - C#
  - C++
  - 알고리즘
keywords: "백준 9243, 백준 9243번, BOJ 9243, deletionCheck, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9243번 - 파일 삭제](https://www.acmicpc.net/problem/9243)

## 설명
**파일 삭제 연산이 홀수 번 수행된 경우 비트 반전이 발생한다는 조건을 기반으로, 원래 파일과 비교하여 삭제가 성공했는지를 판단하는 문제**입니다.<br>
<br>

- 삭제 연산이 `N`번 수행되며, 이 수가 홀수이면 모든 비트가 반전됩니다.<br>
- 원래 파일 상태와 현재 파일 상태가 주어졌을 때, 삭제 연산 결과가 올바른지 확인해야 합니다.<br>
- 이진 문자열로 표현된 두 파일 상태를 비교합니다.<br>

### 접근법
- 먼저 삭제 연산 횟수 `N`이 홀수인지 짝수인지 판단합니다.<br>
- 만약 홀수라면, 원래 문자열의 각 비트를 반전시켜 새로운 문자열을 생성합니다.<br>
- 짝수라면 반전 없이 원래 문자열을 그대로 유지합니다.<br>
- 변환된 문자열과 최종 문자열이 일치하면 `"Deletion succeeded"`, 그렇지 않으면 `"Deletion failed"`를 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    string before = Console.ReadLine();
    string after = Console.ReadLine();

    if (n % 2 == 1) {
      char[] flipped = new char[before.Length];
      for (int i = 0; i < before.Length; i++)
        flipped[i] = before[i] == '0' ? '1' : '0';
      before = new string(flipped);
    }

    Console.WriteLine("Deletion " + (before == after ? "succeeded" : "failed"));
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

  int n; cin >> n;
  n %= 2;

  string before, after; cin >> before >> after;

  if (n) {
    for (size_t i = 0; i < before.size(); i++) {
      if (before[i] == '0') before[i] = '1';
      else if (before[i] == '1') before[i] = '0';
    }
  }

  cout << "Deletion ";
  if (before == after) cout << "succeeded\n";
  else cout << "failed\n";

  return 0;
}
```
