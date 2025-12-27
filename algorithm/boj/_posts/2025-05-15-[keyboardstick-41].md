---
layout: single
title: "[백준 7120] String (C#, C++) - soo:bak"
date: "2025-05-15 09:31:00 +0900"
description: 연속된 동일 문자를 제거하여 원래 문자열을 복원하는 백준 7120번 String 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 7120
  - C#
  - C++
  - 알고리즘
keywords: "백준 7120, 백준 7120번, BOJ 7120, keyboardstick, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[7120번 - String](https://www.acmicpc.net/problem/7120)

## 설명
**연속된 동일 문자를 하나로 줄여 원래 문자열을 복원하는 문제입니다.**

<br>

## 접근법

입력된 문자열을 왼쪽에서부터 차례로 읽으며,

앞선 문자와 같은 글자가 반복되는 경우에는 한 번만 출력하도록 처리합니다.

즉, 연속된 문자가 있을 때는 **맨 앞의 문자만 남기고 나머지는 모두 건너뜁니다.**

이 과정을 처음부터 끝까지 순차적으로 진행하면,

오작동된 키보드 입력을 원래의 형태로 복원할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    string word = Console.ReadLine();
    var sb = new StringBuilder();
    sb.Append(word[0]);

    for (int i = 1; i < word.Length; i++) {
      if (word[i] != word[i - 1])
        sb.Append(word[i]);
    }

    Console.WriteLine(sb.ToString());
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

  string word; cin >> word;

  string ans = "";
  ans += word[0];
  for (size_t i = 1; i < word.size(); i++) {
    if (word[i] != word[i - 1])
      ans += word[i];
  }

  cout << ans << "\n";
  return 0;
}
```
