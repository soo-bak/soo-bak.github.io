---
layout: single
title: "[백준 1373] 2진수 8진수 (C#, C++) - soo:bak"
date: "2025-05-04 09:12:00 +0900"
description: 2진수를 3자리씩 나누어 8진수로 변환하는 과정을 구현하는 백준 1373번 2진수 8진수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1373
  - C#
  - C++
  - 알고리즘
  - 수학
  - 문자열
keywords: "백준 1373, 백준 1373번, BOJ 1373, binarytooctal, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1373번 - 2진수 8진수](https://www.acmicpc.net/problem/1373)

## 설명
2진수를 입력받아 8진수로 변환하는 문제입니다.

2진수를 **오른쪽에서부터 3자리씩 묶어** 각 묶음을 8진수의 한 자리로 바꾸면 됩니다.

3자리씩 묶을 수 없는 경우에는 앞쪽에 `0`을 추가하여 자릿수를 맞춰줍니다.

<br>

## 접근법

- 먼저 2진수 문자열을 입력받습니다.
- 전체 자릿수를 3의 배수로 맞추기 위해 앞에 `'0'`을 추가합니다.
- 이후 3자리씩 묶어서 문자열을 분리한 뒤, <br>
  각 묶음에 대해 2진수를 8진수로 변환한 결과를 차례대로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var bin = Console.ReadLine();
    while (bin.Length % 3 != 0)
      bin = "0" + bin;

    var sb = new StringBuilder();
    for (int i = 0; i < bin.Length; i += 3) {
      string tri = bin.Substring(i, 3);
      sb.Append(Convert.ToInt32(tri, 2));
    }

    Console.WriteLine(sb.ToString());
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef deque<char> dc;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  dc dq;
  char c;
  while (cin >> c) dq.push_back(c);

  int n = dq.size();
  while (n % 3) dq.push_front('0'), n++;

  for (int i = 0; i < n; i += 3) {
    string s = {dq[i], dq[i + 1], dq[i + 2]};
    if (s == "000") cout << 0;
    else if (s == "001") cout << 1;
    else if (s == "010") cout << 2;
    else if (s == "011") cout << 3;
    else if (s == "100") cout << 4;
    else if (s == "101") cout << 5;
    else if (s == "110") cout << 6;
    else cout << 7;
  }
  cout << "\n";

  return 0;
}
```
