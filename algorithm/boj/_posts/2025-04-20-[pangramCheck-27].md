---
layout: single
title: "[백준 5704] 팬그램 (C#, C++) - soo:bak"
date: "2025-04-20 03:24:00 +0900"
description: 주어진 문장이 팬그램인지 판별하는 로직을 구현하는 백준 5704번 팬그램 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[5704번 - 팬그램](https://www.acmicpc.net/problem/5704)

## 설명
**팬그램이란 알파벳 a부터 z까지 모든 문자가 적어도 한 번 이상 등장하는 문장을 의미합니다.**
이 때, 입력으로 주어지는 문자열에 대하여 해당 문자열이 팬그램 문자열인지 아닌지를 판별하는 문제입니다. <br>
<br>

- 입력은 여러 줄로 이루어지며, 각 줄은 공백을 포함한 문장입니다.
- 각 문장마다 해당 문장의 팬그램 여부를 판별합니다.
- 각 문장에 대해서, 해당 문장이 팬그램이면 `Y`를, 아니면 `N`을 출력해야 합니다.
- 입력의 마지막에는 `*` 문자가 주어집니다.


## 접근법

1. 줄 단위로 문자열을 입력받습니다.
2. 각 줄에 대해 알파벳 등장 여부를 확인합니다.
   - `a`부터 `z`까지의 등장 여부를 모두 체크합니다.
3. 알파벳 26자가 모두 등장했는지 판단하고, 결과에 따라 `Y` 또는 `N`을 출력합니다.
4. 입력이 `*`인 경우 처리를 종료합니다.


## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    while (true) {
      string line = Console.ReadLine();
      if (line == "*") break;

      var seen = new bool[26];
      foreach (char c in line.ToLower())
        if (char.IsLetter(c)) seen[c - 'a'] = true;

      Console.WriteLine(seen.All(x => x) ? "Y" : "N");
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
  while (getline(cin, s) && s != "*") {
    bitset<26> seen;
    for (char c : s)
      if (isalpha(c)) seen[c - 'a'] = 1;
    cout << (seen.all() ? "Y" : "N") << "\n";
  }

  return 0;
}
```
