---
layout: single
title: "[백준 11944] NN (C#, C++) - soo:bak"
date: "2025-04-17 01:09:35 +0900"
description: 숫자 N을 N번 반복하여 출력하되 최대 길이를 제한하는 문자열 처리 문제인 백준 11944번 NN 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11944
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 11944, 백준 11944번, BOJ 11944, repeatNumCut, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11944번 - NN](https://www.acmicpc.net/problem/11944)

## 설명
**입력으로 주어진 수** `N`**을** `N`**번 반복하여 출력하되, 최대 출력 길이를** `M`**으로 제한하는 문자열 문제**입니다.<br>
<br>

- 입력은 정수 `N`과 정수 `M`이 주어집니다.<br>
- 숫자 `N`을 문자열로 보아 `N`번 반복한 문자열을 만듭니다.<br>
- 단, 반복된 전체 문자열이 길이 `M`을 초과하면 **앞에서부터** `M`**길이만큼 자른 문자열**을 출력해야 합니다.<br>

### 접근법
- 먼저 `N`을 `문자열`로 입력받아 반복에 사용합니다.<br>
- 반복 횟수에 대해서는 `N`이 정수 값으로 활용되므로, 문자열로 저장한 `N`을 정수값으로 변환하여 사용합니다.<br>
- 반복하여 문자열을 누적한 뒤, 길이가 `M`을 초과하는 경우 문자열의 길이가 `M` 이 되도록 자릅니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var inputs = Console.ReadLine().Split();
    string n = inputs[0];
    int m = int.Parse(inputs[1]);
    int repeat = int.Parse(n);

    var sb = new StringBuilder();
    for (int i = 0; i < repeat && sb.Length <= m; i++)
      sb.Append(n);

    if (sb.Length > m)
      sb.Length = m;

    Console.WriteLine(sb.ToString());
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

  string n; size_t m; cin >> n >> m;

  int repeats = stoi(n), printed = 0;
  string ans = "";
  while (printed != repeats) {
    ans += n;
    printed++;
  }

  if (ans.size() > m) ans.resize(m);

  cout << ans << "\n";

  return 0;
}
```
