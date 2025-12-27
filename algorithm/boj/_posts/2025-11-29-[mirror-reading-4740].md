---
layout: single
title: "[백준 4740] 거울, 오! 거울 (C#, C++) - soo:bak"
date: "2025-11-29 22:00:00 +0900"
description: 줄 단위로 입력을 받아 *** 이전까지 각 문장을 뒤집어 출력하는 백준 4740번 거울 읽기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 4740
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 4740, 백준 4740번, BOJ 4740, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4740번 - 거울, 오! 거울](https://www.acmicpc.net/problem/4740)

## 설명

여러 줄의 문장이 입력으로 주어지는 상황에서, 각 줄의 문장(길이 1~80)과 종료 표시 `***`이 주어질 때, 각 문장을 거꾸로 뒤집어 출력하는 문제입니다.

`***`로 시작하는 줄이 입력되면 프로그램이 종료되며, 각 줄은 알파벳, 숫자, 공백, 구두점 등 ASCII 문자로만 구성됩니다.

<br>

## 접근법

각 줄을 입력받으면서 종료 표시인 `***`이 나올 때까지 처리합니다.

문자열을 뒤집는 것은 문자열의 처음과 끝을 교환하며 중앙으로 이동하는 방식으로 구현할 수 있습니다.

표준 라이브러리의 문자열 뒤집기 함수를 사용하면 간단하게 O(N) 시간에 처리할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      while (true) {
        var line = Console.ReadLine()!;
        if (line == "***")
          break;

        var chars = line.ToCharArray();
        Array.Reverse(chars);
        Console.WriteLine(chars);
      }
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

  while (true) {
    string line;
    getline(cin, line);
    
    if (line == "***")
      break;

    reverse(line.begin(), line.end());
    cout << line << "\n";
  }
  
  return 0;
}
```


