---
layout: single
title: "[백준 10384] The Hardest Problem Ever (C#, C++) - soo:bak"
date: "2025-04-29 05:30:00 +0900"
description: 시저 암호를 응용하여 5칸 왼쪽으로 이동해 복호화하는 백준 10384번 The Hardest Problem Ever 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10384번 - The Hardest Problem Ever](https://www.acmicpc.net/problem/10384)

## 설명
암호문을 해독하여 원래 문장을 복원하는 문제입니다.

이 문제에서는 고전 암호 기법 중 하나인 **시저 암호(Caesar cipher)**를 변형하여 사용합니다.

<br>
일반적인 시저 암호는 알파벳을 오른쪽으로 일정 칸 이동시키지만,

이 문제에서는 **암호문을 왼쪽으로 다섯 칸 이동시켜 복호화**해야 합니다.

<br>
변환 규칙은 다음과 같습니다:

- 알파벳 문자(`'A'~'Z'`)는 각각 왼쪽으로 `5`칸 이동합니다.
  - 예를 들어, `A`는 `V`로, `B`는 `W`로 복원됩니다.
- 알파벳이 아닌 문자(공백, 쉼표 등)는 변환하지 않고 그대로 출력합니다.

<br>
입력은 여러 데이터 단위로 구성되어 있으며,

각 데이터 단위는 `"START"`, `암호문 한 줄`, `"END"`로 구성됩니다.

마지막에는 `"ENDOFINPUT"`이 입력되어 전체 입력이 종료됩니다.

<br>

## 접근법

암호문을 한 줄씩 읽으면서 다음 과정을 수행합니다.

- `"START"`나 `"END"`라는 라인은 입력 처리에 사용될 뿐, 실제 복호화 대상은 아닙니다.
- 암호문 내부의 각 문자를 순회합니다.
  - 만약 문자가 `'A'` 이상 `'Z'` 사이에 있다면, 복호화 테이블을 이용해 `5`칸 왼쪽의 문자로 변환합니다.
  - 알파벳 이외의 문자는 변환하지 않고 그대로 출력합니다.
- `"ENDOFINPUT"`이 등장하면 입력을 종료합니다.

<br>
변환 과정은 각 문자를 독립적으로 처리하므로 시간 복잡도는 전체 입력 크기에 대해 $$O(N)$$입니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    string[] mapping = new [] {
      "V","W","X","Y","Z","A","B","C","D","E",
      "F","G","H","I","J","K","L","M","N","O",
      "P","Q","R","S","T","U"
    };

    while (true) {
      string header = Console.ReadLine();
      if (header == "ENDOFINPUT") break;
      if (header == "START") {
        string line = Console.ReadLine();
        foreach (char ch in line) {
          if ('A' <= ch && ch <= 'Z') Console.Write(mapping[ch - 'A']);
          else Console.Write(ch);
        }
        Console.WriteLine();
        Console.ReadLine();
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

  const string PLAIN = "VWXYZABCDEFGHIJKLMNOPQRSTU";

  string line;
  while (getline(cin, line)) {
    if (line == "START" || line == "END") continue;
    if (line == "ENDOFINPUT") break;

    for (char ch : line) {
      if ('A' <= ch && ch <= 'Z') cout << PLAIN[ch - 'A'];
      else cout << ch;
    }

    cout << "\n";
  }

  return 0;
}
```
