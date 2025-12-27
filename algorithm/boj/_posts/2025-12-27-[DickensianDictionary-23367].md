---
layout: single
title: "[백준 23367] Dickensian Dictionary (C#, C++) - soo:bak"
date: "2025-12-27 01:55:00 +0900"
description: "백준 23367번 C#, C++ 풀이 - 왼손과 오른손이 번갈아 나오는 단어인지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 23367
  - C#
  - C++
  - 알고리즘
keywords: "백준 23367, 백준 23367번, BOJ 23367, DickensianDictionary, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23367번 - Dickensian Dictionary](https://www.acmicpc.net/problem/23367)

## 설명
영문 소문자 단어가 왼손(`qwertasdfgzxcvb`)과 오른손(`yuiophjklnm`) 타이핑이 번갈아가며 나타나는지 판단해, 맞으면 "yes", 아니면 "no"를 출력하는 문제입니다.

<br>

## 접근법
각 문자가 왼손인지 오른손인지 판별한 뒤, 인접한 두 문자의 손이 같으면 실패입니다.

끝까지 번갈아 나오면 "yes"를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static bool IsLeft(char c) {
    const string left = "qwertasdfgzxcvb";
    return left.IndexOf(c) != -1;
  }

  static void Main() {
    var s = Console.ReadLine()!;
    var prevLeft = IsLeft(s[0]);
    var ok = true;

    for (var i = 1; i < s.Length; i++) {
      var curLeft = IsLeft(s[i]);
      if (curLeft == prevLeft) {
        ok = false;
        break;
      }
      prevLeft = curLeft;
    }

    Console.WriteLine(ok ? "yes" : "no");
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

bool isLeft(char c) {
  static const string left = "qwertasdfgzxcvb";
  return left.find(c) != string::npos;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s; cin >> s;
  bool prev_left = isLeft(s[0]);
  bool ok = true;

  for (size_t i = 1; i < s.size(); i++) {
    bool cur_left = isLeft(s[i]);
    if (cur_left == prev_left) {
      ok = false;
      break;
    }
    prev_left = cur_left;
  }

  cout << (ok ? "yes" : "no") << "\n";
  return 0;
}
```
