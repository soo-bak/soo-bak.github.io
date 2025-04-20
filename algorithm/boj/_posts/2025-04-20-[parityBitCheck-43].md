---
layout: single
title: "[백준 4597] 패리티 (C#, C++) - soo:bak"
date: "2025-04-20 23:59:00 +0900"
description: 주어진 이진 문자열에 짝수 또는 홀수 패리티를 맞추어 마지막 자리를 채우는 백준 4597번 패리티 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[4597번 - 패리티](https://www.acmicpc.net/problem/4597)

## 설명
**이진 문자열의 마지막 비트를 패리티 조건에 맞추어 보정하는 문제입니다.**<br>
<br>

- 문자열은 `'0'`과 `'1'`로 이루어진 이진수이며, 마지막 자리는 `'e'` 또는 `'o'`로 주어집니다.
  - `'e'`는 **짝수 패리티(even parity)**를 의미하며, `전체 1의 개수`가 `짝수`여야 함을 뜻합니다.
  - `'o'`는 **홀수 패리티(odd parity)**를 의미하며, `전체 1의 개수`가 `홀수`여야 함을 뜻합니다.
- 주어진 문자열을 읽고, 마지막 자리에 `'0'` 또는 `'1'`을 적절히 채워 패리티 조건을 만족시키도록 완성해야 합니다.
- `#`가 입력되면 프로그램을 종료합니다.


## 접근법

- 입력된 문자열에서 마지막 문자를 기준으로 `'e'` 또는 `'o'` 여부를 확인합니다.
- 문자열 내 `'1'`의 개수를 세어 패리티 조건을 만족하도록 마지막 자리를 `'0'` 또는 `'1'`로 채웁니다.
- 짝수 패리티일 경우, `'1'`의 개수가 **짝수여야 하므로**, 현재 개수에 따라 `'0'` 또는 `'1'`을 추가합니다.
- 문자열 전체를 위과 같이 수정한 뒤 출력합니다.


## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string s;
    while ((s = Console.ReadLine()) != "#") {
      int ones = 0;
      for (int i = 0; i < s.Length - 1; i++)
        if (s[i] == '1') ones++;

      bool isEven = s[^1] == 'e';
      s = s[..^1] + ((ones % 2 == (isEven ? 0 : 1)) ? "0" : "1");
      Console.WriteLine(s);
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

  string s;
  while (cin >> s && s != "#") {
    int ones = count(s.begin(), s.end(), '1');
    s.back() = (ones % 2 == (s.back() == 'e') ? '1' : '0');
    cout << s << "\n";
  }

  return 0;
}
```
