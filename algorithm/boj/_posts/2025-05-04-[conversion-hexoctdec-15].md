---
layout: single
title: "[백준 11816] 8진수, 10진수, 16진수 (C#, C++) - soo:bak"
date: "2025-05-04 00:15:00 +0900"
description: 다양한 진법 표기 형식을 해석하여 10진수로 변환하는 문제인 백준 11816번 8진수, 10진수, 16진수 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[11816번 - 8진수, 10진수, 16진수](https://www.acmicpc.net/problem/11816)

## 설명
숫자 `X`가 입력될 때, 해당 수가 **8진수**, **10진수**, 혹은 **16진수** 형식 중 하나로 주어졌다고 가정하고,

이를 **10진수로 변환하여 출력**하는 문제입니다.

<br>

입력 형식은 아래와 같이 주어집니다:

- `0x`로 시작하면 **16진수**
- `0`으로 시작하면 **8진수**
- 이외의 경우는 **10진수**로 간주합니다.

따라서 접두사에 따라 수의 진법을 판단한 뒤, 그에 맞는 방식으로 계산하며 10진수로 변환해야 합니다.

<br>

## 접근법

- 먼저 입력된 문자열이 어떤 진법으로 주어졌는지를 확인합니다.
  - `0x`로 시작하면 16진수, `0`으로 시작하면 8진수, 그 외는 10진수입니다.
- 각 진법에 따라 문자열을 해석하여 10진수로 변환합니다.
  - 16진수의 경우 `A`~`F` 또는 `a`~`f` 문자를 숫자 `10`~`15`로 해석해야 합니다.
- 변환된 결과를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine();
    int result;

    if (s.StartsWith("0x"))
      result = Convert.ToInt32(s.Substring(2), 16);
    else if (s.StartsWith("0") && s.Length > 1)
      result = Convert.ToInt32(s.Substring(1), 8);
    else result = int.Parse(s);

    Console.WriteLine(result);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s; cin >> s;

  int ans = 0;
  if (s[0] == '0' && s.size() > 1 && s[1] == 'x') {
    vi pow(s.size() - 2);
    pow[0] = 1;
    for (int i = 1; i < pow.size(); i++)
      pow[i] = pow[i - 1] * 16;
    for (int i = 2; i < s.size(); i++)
      ans += (isalpha(s[i]) ? tolower(s[i]) - 'a' + 10 : s[i] - '0') * pow[s.size() - 1 - i];
  } else if (s[0] == '0' && s.size() > 1) {
    vi pow(s.size() - 1);
    pow[0] = 1;
    for (int i = 1; i < pow.size(); i++)
      pow[i] = pow[i - 1] * 8;
    for (int i = 1; i < s.size(); i++)
      ans += (s[i] - '0') * pow[s.size() - 1 - i];
  } else ans = stoi(s);

  cout << ans << "\n";

  return 0;
}
```
