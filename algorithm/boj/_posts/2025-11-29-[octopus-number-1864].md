---
layout: single
title: "[백준 1864] 문어 숫자 (C#, C++) - soo:bak"
date: "2025-11-29 13:10:00 +0900"
description: 특수 기호를 -1~7 숫자로 매핑해 8진법 자릿값을 곱해 십진수로 변환하는 백준 1864번 문어 숫자 문제의 C# 및 C++ 풀이
---

## 문제 링크
[1864번 - 문어 숫자](https://www.acmicpc.net/problem/1864)

## 설명

문어가 사용하는 8진법 숫자 체계가 주어지는 상황에서, 여러 줄의 문어 숫자(길이 1~8)와 종료 표시 `#`이 주어질 때, 각 문어 숫자를 10진수로 변환하여 출력하는 문제입니다.

문어 숫자는 다음과 같이 특수 기호로 표현됩니다:
- `-` → 0, `\` → 1, `(` → 2, `@` → 3, `?` → 4, `>` → 5, `&` → 6, `%` → 7, `/` → -1

`#`이 입력되면 종료됩니다.

<br>

## 접근법

8진법은 각 자리가 8의 거듭제곱을 나타냅니다.

오른쪽 끝 자리부터 8^0, 8^1, 8^2, ...의 자리값을 가지며, 각 자리의 숫자에 해당 자리값을 곱하여 모두 더하면 10진수가 됩니다.

각 기호를 대응하는 숫자로 변환한 후, 문자열의 오른쪽 끝부터 각 자리값을 곱하여 합산하면 10진수 변환이 완료됩니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static int ToDigit(char c) {
      return c switch {
        '-' => 0, '\\' => 1, '(' => 2, '@' => 3,
        '?' => 4, '>' => 5, '&' => 6, '%' => 7,
        '/' => -1,
        _ => 0
      };
    }

    static void Main(string[] args) {
      while (true) {
        var s = Console.ReadLine()!;
        if (s.StartsWith('#')) break;

        long result = 0, placeValue = 1;
        for (var i = s.Length - 1; i >= 0; i--) {
          result += ToDigit(s[i]) * placeValue;
          placeValue *= 8;
        }
        Console.WriteLine(result);
      }
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int toDigit(char c) {
  switch (c) {
    case '-': return 0;  case '\\': return 1;
    case '(': return 2;  case '@': return 3;
    case '?': return 4;  case '>': return 5;
    case '&': return 6;  case '%': return 7;
    case '/': return -1;
    default: return 0;
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s;
  while (cin >> s) {
    if (s[0] == '#') break;
    ll result = 0, placeValue = 1;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
      result += toDigit(s[i]) * placeValue;
      placeValue *= 8;
    }
    cout << result << "\n";
  }
  
  return 0;
}
```

