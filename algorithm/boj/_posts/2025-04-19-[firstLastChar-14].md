---
layout: single
title: "[백준 9086] 문자열 (C#, C++) - soo:bak"
date: "2025-04-19 00:18:10 +0900"
description: 여러 문자열에서 첫 글자와 마지막 글자를 추출하여 출력하는 백준 9086번 문자열 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[9086번 - 문자열](https://www.acmicpc.net/problem/9086)

## 설명
**여러 개의 문자열이 주어졌을 때, 각 문자열의 첫 번째 문자와 마지막 문자를 출력하는 단순 구현 문제**입니다.<br>
<br>

- 각 테스트케이스마다 문자열 하나가 주어집니다.<br>
- 해당 문자열의 **첫 글자**와 **마지막 글자**를 차례대로 이어서 출력합니다.<br>
- 문자열의 길이는 항상 1 이상이므로 별도의 예외 처리는 필요하지 않습니다.<br>

### 접근법
- 문자열을 입력받은 뒤, 첫 번째 문자와 마지막 문자를 추출합니다.<br>
- 두 문자를 순서대로 이어서 출력하면 됩니다.<br>

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
      string str = Console.ReadLine();
      Console.WriteLine($@"{str[0]}{str[str.Length - 1]}");
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
    string str; cin >> str;
    cout << str[0] << str[str.size() - 1] << "\n";
  }

  return 0;
}
```
