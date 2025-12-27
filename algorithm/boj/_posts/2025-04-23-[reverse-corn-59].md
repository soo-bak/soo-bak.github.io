---
layout: single
title: "[백준 11945] 뜨거운 붕어빵 (C#, C++) - soo:bak"
date: "2025-04-23 06:53:00 +0900"
description: 각 줄에 있는 문자를 거꾸로 뒤집어 출력하는 단순 문자열 처리 문제인 백준 11945번 뜨거운 붕어빵 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11945
  - C#
  - C++
  - 알고리즘
keywords: "백준 11945, 백준 11945번, BOJ 11945, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11945번 - 뜨거운 붕어빵](https://www.acmicpc.net/problem/11945)

## 설명
재미있게 붕어빵에 비유되었지만,<br>

결국, 문자들이 오른쪽에서 왼쪽으로 거꾸로 된 상태로 주어졌을 때, 이를 원래 방향으로 복원하는 문제입니다.<br><br>

- 입력으로 `행`의 개수와 `열`의 길이가 주어집니다.
- 각 줄에는 고정된 길이의 문자열이 한 줄씩 입력됩니다.
- 각 줄에 대해, 문자를 오른쪽에서 왼쪽으로 뒤집어 출력하면 됩니다.

## 접근법
- 먼저 전체 문자열을 2차원 리스트에 입력받습니다.
- 각 줄을 뒤에서부터 앞쪽으로 순회하며 출력하면 됩니다.
- 단순 문자열 뒤집기만 수행하면 되므로 추가적인 로직은 필요하지 않습니다.

시간 복잡도는 `O(N × M)`이며, 각 문자를 한 번씩만 순회하면 됩니다.

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    int n = int.Parse(input[0]), m = int.Parse(input[1]);

    var lines = new string[n];
    for (int i = 0; i < n; i++)
      lines[i] = Console.ReadLine();

    foreach (var line in lines) {
      char[] arr = line.ToCharArray();
      Array.Reverse(arr);
      Console.WriteLine(new string(arr));
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

  int cntLine, lenLine; cin >> cntLine >> lenLine;

  vector<string> line(cntLine);
  for (int i = 0; i < cntLine; i++) {
    cin >> line[i];
  }

  for (int i = 0; i < cntLine; i++) {
    for (int j = 0; j < lenLine; j++)
      cout << line[i][lenLine - 1 - j];
    cout << "\n";
  }

  return 0;
}
```
