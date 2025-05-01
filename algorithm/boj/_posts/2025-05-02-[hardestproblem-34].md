---
layout: single
title: "[백준 9971] The Hardest Problem Ever (C#, C++) - soo:bak"
date: "2025-05-02 04:30:00 +0900"
description: 시저 암호로 인코딩된 문자열을 복호화하는 백준 9971번 The Hardest Problem Ever 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[9971번 - The Hardest Problem Ever](https://www.acmicpc.net/problem/9971)

## 설명
고대 암호 기법 중 하나인 **시저 암호(Caesar Cipher)**가 적용된 문자열이 주어졌을 때,

이 문자열을 원래의 평문으로 복호화하는 문제입니다.

<br>
암호화는 알파벳을 오른쪽으로 `5`칸 이동시켜 수행되며,

복호화를 위해서는 이를 **왼쪽으로 5칸** 되돌리는 과정을 적용해야 합니다.

<br>
예를 들어 `A`는 `F`로 암호화되므로, 복호화 시에는 `F`를 `A`로 되돌려야 합니다.

알파벳만 복호화 대상이며, 대문자 이외의 문자(공백, 쉼표 등)는 그대로 유지됩니다.

<br>

## 접근법

- `"START"`와 `"END"` 사이에 등장하는 문자열만 복호화합니다.
- 각 문자를 순회하면서 알파벳인 경우에는 알파벳 순서를 기준으로 **5칸 앞 문자를 대응**시킵니다.
- 알파벳이 아닌 문자는 그대로 출력합니다.
- `"ENDOFINPUT"`이 등장하면 모든 입력을 종료합니다.

단순한 문자 치환이므로 시간 복잡도는 전체 문자 수에 대해 $$O(N)$$입니다.

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
