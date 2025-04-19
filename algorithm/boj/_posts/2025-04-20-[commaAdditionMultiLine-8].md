---
layout: single
title: "[백준 10823] 더하기 2 (C#, C++) - soo:bak"
date: "2025-04-20 03:05:00 +0900"
description: 여러 줄에 걸쳐 입력된 콤마 구분 숫자들을 모두 합산하는 백준 10823번 더하기 2 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10823번 - 더하기 2](https://www.acmicpc.net/problem/10823)

## 설명
**여러 줄에 걸쳐 입력된 숫자들을 콤마(**`,`**) 기준으로 분리하여 모두 합산하는 문제입니다.**
<br>

- 입력은 한 줄이 아니라 여러 줄에 걸쳐 주어질 수 있습니다.
- 전체 입력을 연결하여 하나의 문자열로 만든 뒤, 콤마 기준으로 정수들을 분리해야 합니다.
- 그 후, 모든 정수를 더한 결과를 출력합니다.

예시:
```
10,20
30,40
50
```
→ 출력: `150`

## 접근법

1. 입력이 끝날 때까지 문자열을 이어붙입니다.
2. 최종 문자열에서 `,` 기준으로 나눕니다.
3. 나눠진 문자열을 정수로 바꾸어 모두 더합니다.
4. 합을 출력합니다.

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    string input = Console.In.ReadToEnd().Replace("\r", "").Replace("\n", "");
    int sum = input.Split(',').Select(int.Parse).Sum();
    Console.WriteLine(sum);
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

  string s, num;
  while (getline(cin, num)) s += num;

  int sum = 0;
  stringstream ss(s);
  while (getline(ss, num, ',')) sum += stoi(num);

  cout << sum << "\n";

  return 0;
}
```
