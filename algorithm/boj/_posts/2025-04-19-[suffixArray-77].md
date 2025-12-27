---
layout: single
title: "[백준 11656] 접미사 배열 (C#, C++) - soo:bak"
date: "2025-04-19 19:04:42 +0900"
description: 문자열의 모든 접미사를 사전순으로 정렬하는 백준 11656번 접미사 배열 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11656
  - C#
  - C++
  - 알고리즘
  - 문자열
  - 정렬
keywords: "백준 11656, 백준 11656번, BOJ 11656, suffixArray, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11656번 - 접미사 배열](https://www.acmicpc.net/problem/11656)

## 설명
**주어진 문자열로부터 가능한 모든 접미사를 추출한 후, 이를 사전순으로 정렬하여 출력하는 문자열 처리 문제**입니다.<br>
<br>

- 하나의 문자열이 입력으로 주어집니다.<br>
- 이 문자열의 각 문자 위치에서 시작하여 끝까지 이어지는 부분 문자열을 접미사라고 합니다.<br>
  예를 들어 문자열 `banana`라면 접미사는 `banana`, `anana`, `nana`, `ana`, `na`, `a`가 됩니다.<br>
- 이 모든 접미사를 추출한 뒤, **사전에서 단어를 정렬하는 방식과 같은 순서**로 정렬합니다.<br>
- 정렬된 접미사들을 한 줄씩 출력하면 됩니다.<br>

### 접근법
- 문자열의 길이만큼 반복하면서 각 위치에서 시작하는 접미사를 하나씩 만들어 리스트에 담습니다.<br>
- 이후 그 리스트를 알파벳 순으로 정렬합니다.<br>
- 정렬된 결과를 그대로 출력하여 문제를 해결할 수 있습니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;
using System.Collections.Generic;

class Program {
  static void Main() {
    string input = Console.ReadLine();
    var suffixes = new List<string>();

    for (int i = 0; i < input.Length; i++)
      suffixes.Add(input.Substring(i));

    suffixes.Sort();
    foreach (var s in suffixes)
      Console.WriteLine(s);
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string str; cin >> str;

  vs ans(str.size());

  for (size_t i = 0; i < str.size(); i++)
    ans[i] = str.substr(i);

  sort(ans.begin(), ans.end());

  for (auto i : ans) cout << i << "\n";

  return 0;
}
```
