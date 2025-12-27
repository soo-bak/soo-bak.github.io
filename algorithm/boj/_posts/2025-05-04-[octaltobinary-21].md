---
layout: single
title: "[백준 1212] 8진수 2진수 (C#, C++) - soo:bak"
date: "2025-05-04 09:03:00 +0900"
description: 8진수를 입력받아 각 자릿수를 이진수로 변환해 출력하는 백준 1212번 8진수 2진수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1212
  - C#
  - C++
  - 알고리즘
keywords: "백준 1212, 백준 1212번, BOJ 1212, octaltobinary, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1212번 - 8진수 2진수](https://www.acmicpc.net/problem/1212)

## 설명

입력으로 주어진 **8진수 수를 2진수로 변환하는 문제**입니다.

<br>

## 접근법

- 각 8진수 자릿수는 **3자리 이진수로 변환**됩니다.
- 따라서 입력된 문자열을 앞에서부터 한 자리씩 읽고, <br>
  **각 자리 값을 이진수 3자리**로 바꾸면 됩니다.
- 단, **가장 앞자리의 경우에는 앞에 붙는 0을 생략**해야 하므로,
  변환된 이진수의 `앞부분에 포함된 0`을 제거한 뒤 출력합니다.
- 수가 `0` 하나만 주어진 경우를 제외하고는 반드시 `1`로 시작해야 합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    string s = Console.ReadLine();
    var sb = new StringBuilder();

    for (int i = 0; i < s.Length; i++) {
      int n = s[i] - '0';
      string bin = "";
      if (i == 0) {
        while (n > 0) {
          bin = (n % 2) + bin;
          n /= 2;
        }
        if (bin == "") bin = "0";
      } else {
        for (int j = 2; j >= 0; j--)
          bin += (n >> j & 1);
      }
      sb.Append(bin);
    }

    Console.WriteLine(sb.ToString());
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string toBin(int n) {
  string s;
  for (int i = 2; i >= 0; i--)
    s += (n >> i & 1) + '0';
  return s;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s; cin >> s;
  for (size_t i = 0; i < s.size(); i++) {
    string t = toBin(s[i] - '0');
    if (i == 0) {
      size_t j = 0;
      while (j < 2 && t[j] == '0') j++;
      t = t.substr(j);
    }
    cout << t;
  }
  cout << "\n";

  return 0;
}
```
