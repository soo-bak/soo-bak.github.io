---
layout: single
title: "[백준 11365] !밀비 급일 (C#, C++) - soo:bak"
date: "2025-04-19 00:14:10 +0900"
description: 입력된 문자열을 뒤집어서 출력하는 역순 문자열 처리 문제인 백준 11365번 !밀비 급일 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[11365번 - !밀비 급일](https://www.acmicpc.net/problem/11365)

## 설명
**여러 줄의 문자열이 주어졌을 때, 각 줄을 뒤집어 출력하는 간단한 문자열 처리 문제**입니다.<br>
<br>

- 각 줄마다 입력된 문자열을 역순으로 출력하면 됩니다.<br>
- 입력은 `"END"`라는 단어가 등장할 때까지 계속됩니다. `"END"`는 처리하지 않고 종료 조건으로만 사용됩니다.<br>
- 단어 단위가 아니라 줄 전체를 뒤집습니다.<br>

### 접근법
- 표준 입력에서 한 줄씩 문자열을 입력받고, 문자열이 `"END"`와 같으면 종료합니다.<br>
- 그렇지 않다면 문자열을 뒤집고 그대로 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    while (true) {
      string input = Console.ReadLine();
      if (input == "END") break;

      var arr = input.ToCharArray();
      Array.Reverse(arr);
      Console.WriteLine(new string(arr));
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
    if (!str.compare("END")) break;

    reverse(str.begin(), str.end());
    cout << str << "\n";
  }

  return 0;
}
```
