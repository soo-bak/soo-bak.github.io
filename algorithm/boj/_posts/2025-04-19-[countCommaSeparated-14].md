---
layout: single
title: "[백준 10821] 정수의 개수 (C#, C++) - soo:bak"
date: "2025-04-19 00:16:10 +0900"
description: 콤마로 구분된 정수의 개수를 계산하여 출력하는 백준 10821번 정수의 개수 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10821번 - 정수의 개수](https://www.acmicpc.net/problem/10821)

## 설명
**콤마(,)로 구분된 정수들의 개수를 세는 간단한 문자열 문제**입니다.<br>
<br>

- 입력은 하나의 문자열이며, `정수1,정수2,정수3,...` 형태로 주어집니다.<br>
- 콤마로 구분된 정수의 **총 개수**를 출력하면 됩니다.<br>
- 각 정수는 0 이상 100 이하의 값이며, 입력에 공백은 포함되지 않습니다.<br>

### 접근법
- 입력 문자열에서 `','`의 개수를 셉니다.<br>
- 콤마 개수는 정수 개수보다 항상 하나 작기 때문에 `콤마 개수 + 1`이 정답이 됩니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    string input = Console.ReadLine();
    int count = 1;

    foreach (char c in input)
      if (c == ',') count++;

    Console.WriteLine(count);
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

  string str; cin >> str;
  int cntComma = 0;
  for (size_t i = 0; i < str.size(); i++) {
    if (str[i] == ',') cntComma++;
  }
  cout << cntComma + 1 << "\n";

  return 0;
}
```
