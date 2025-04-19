---
layout: single
title: "[백준 10820] 문자열 분석 (C#, C++) - soo:bak"
date: "2025-04-19 20:01:58 +0900"
description: 문자열에서 소문자, 대문자, 숫자, 공백의 개수를 세는 백준 10820번 문자열 분석 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10820번 - 문자열 분석](https://www.acmicpc.net/problem/10820)

## 설명
**문자열의 각 줄에 대해 소문자, 대문자, 숫자, 공백의 개수를 각각 세는 문자열 분석 문제**입니다.<br>
<br>

- 입력은 여러 줄로 주어지며, 각 줄마다 문자열이 포함되어 있습니다.<br>
- 각 줄마다 아래 네 가지 정보를 공백을 기준으로 구분하여 출력합니다:<br>
  - 소문자의 개수<br>
  - 대문자의 개수<br>
  - 숫자의 개수<br>
  - 공백의 개수<br>
- 입력이 끝날 때까지 반복적으로 처리해야 하며, 빈 줄 없이 주어집니다.<br>

### 접근법
- 각 줄을 입력받은 후, 해당 문자열을 처음부터 끝까지 순회합니다.<br>
- 문자의 종류를 판별하여 조건에 따라 각각의 개수를 누적합니다.<br>
- 소문자, 대문자, 숫자, 공백을 구분하는 판별 함수를 이용하여 구분합니다.<br>
- 한 줄마다 네 개의 값을 공백으로 구분하여 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    string line;
    while ((line = Console.ReadLine()) != null) {
      int lower = 0, upper = 0, digit = 0, space = 0;
      foreach (char ch in line) {
        if (char.IsLower(ch)) lower++;
        else if (char.IsUpper(ch)) upper++;
        else if (char.IsDigit(ch)) digit++;
        else if (char.IsWhiteSpace(ch)) space++;
      }
      Console.WriteLine($"{lower} {upper} {digit} {space}");
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

  while (true) {
    string str; getline(cin, str);
    if (cin.eof()) break ;

    int cntL = 0, cntU = 0, cntN = 0, cntS = 0;
    for (size_t i = 0; i < str.size(); i++) {
      if (islower(str[i])) cntL++;
      else if (isupper(str[i])) cntU++;
      else if (isdigit(str[i])) cntN++;
      else if (isspace(str[i])) cntS++;
    }
    cout << cntL << " " << cntU << " " << cntN << " " << cntS << "\n";
  }

  return 0;
}
```
