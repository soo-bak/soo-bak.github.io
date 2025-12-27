---
layout: single
title: "[백준 3460] 이진수 (C#, C++) - soo:bak"
date: "2025-04-16 02:07:00 +0900"
description: 정수를 이진수로 변환한 후 1이 등장하는 인덱스를 출력하는 백준 3460번 이진수 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 3460
  - C#
  - C++
  - 알고리즘
keywords: "백준 3460, 백준 3460번, BOJ 3460, binaryPosition, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3460번 - 이진수](https://www.acmicpc.net/problem/3460)

## 설명
**정수를 이진수로 변환한 후, 1이 등장하는 인덱스를 출력하는 문제**입니다.<br>
<br>

- 여러 개의 테스트케이스가 주어집니다.<br>
- 각 테스트케이스마다 주어진 정수를 이진수로 바꾸었을 때, **'1'이 등장하는 비트의 위치(인덱스)**를 출력해야 합니다.<br>
- 이진수는 **오른쪽에서 왼쪽으로 증가하는 인덱스 기준**으로 계산됩니다.<br>
  예: 13 → 이진수 1101 → 0번, 2번, 3번 위치에 1이 존재합니다.<br>

### 접근법
- 입력받은 정수를 2로 나누는 방식으로 이진수로 변환하며 동시에 1이 등장하는 위치를 기억합니다.<br>
- 이진수 문자열을 역순으로 만들고, '1'이 등장하는 위치를 왼쪽부터 출력합니다.<br>
- 모든 테스트케이스마다 줄을 바꿔 출력합니다.<br>
- 혹은, 직접 비트 연산자 `&` 와 `>>` 을 이용하여 풀이할 수도 있습니다.<br>

`C#` 코드는 비트 연산자를 활용하여, `C++` 코드는 문자열 변환을 활용하여 풀이하였습니다. <br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      int num = int.Parse(Console.ReadLine());
      int pos = 0;
      while (num > 0) {
        if ((num & 1) == 1)
          Console.Write($"{pos} ");
        num >>= 1;
        pos++;
      }
      Console.WriteLine();
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

  int t; cin >> t;
  while (t--) {
    int num; cin >> num;
    string binary = "";
    while (num) {
      binary += to_string(num % 2);
      num /= 2;
    }
    for (size_t i = 0; i < binary.size(); i++)
      if (binary[i] == '1') cout << i << " ";

    cout << "\n";
  }

  return 0;
}
```
