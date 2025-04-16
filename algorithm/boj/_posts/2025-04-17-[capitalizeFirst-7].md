---
layout: single
title: "[백준 4458] 첫 글자를 대문자로 (C#, C++) - soo:bak"
date: "2025-04-17 01:06:35 +0900"
description: 각 문장의 첫 글자만 대문자로 바꾸어 출력하는 문자열 처리 문제인 백준 4458번 첫 글자를 대문자로 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[4458번 - 첫 글자를 대문자로](https://www.acmicpc.net/problem/4458)

## 설명
**여러 줄의 문장 중 각 줄의 첫 글자만 대문자로 바꾸어 출력하는 간단한 문자열 문제**입니다.<br>
<br>

- 입력으로는 여러 줄의 문자열이 주어집니다.<br>
- 각 줄마다 **첫 글자가 영문 소문자라면 대문자로 바꾸고**, 나머지는 그대로 유지한 채 출력합니다.<br>
- 줄 단위로 입력을 받아 처리하며, 대소문자 변환은 `islower()` 및 `toupper()` 또는 ASCII 연산을 활용할 수 있습니다.<br>

### 접근법
- 첫 번째 문자를 검사해 소문자인 경우 대문자로 변환하고 출력합니다.<br>
- 전체 문자열 중 나머지 문자는 그대로 출력합니다.<br>
- `getline()`으로 줄 단위 입력을 받아야 공백 포함 문자열도 처리할 수 있습니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());

    for (int i = 0; i < n; i++) {
      string line = Console.ReadLine();
      if (char.IsLower(line[0]))
        line = char.ToUpper(line[0]) + line.Substring(1);
      Console.WriteLine(line);
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

  int n; cin >> n;
  cin.ignore();

  while (n--) {
    string line; getline(cin, line);

    if (!line.empty() && islower(line[0]))
      line[0] = toupper(line[0]);

    cout << line << "\n";
  }

  return 0;
}
```
