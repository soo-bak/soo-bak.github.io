---
layout: single
title: "[백준 3417] Vigenère Cipher Encryption (C#, C++) - soo:bak"
date: "2025-12-26 00:42:46 +0900"
description: "백준 3417번 C#, C++ 풀이 - 키를 반복하며 평문을 시프트해 암호문을 만드는 문제"
tags:
  - 백준
  - BOJ
  - 3417
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 3417, 백준 3417번, BOJ 3417, VigenereCipherEncryption, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3417번 - Vigenère Cipher Encryption](https://www.acmicpc.net/problem/3417)

## 설명
키와 평문이 주어질 때 규칙에 따라 시저 방식으로 변환한 암호문을 출력하는 문제입니다.

<br>

## 접근법
먼저 키를 평문 길이에 맞게 반복하며 대응되는 키 문자를 준비합니다.

다음으로 각 위치에서 키 문자의 이동량만큼 평문 문자를 앞으로 이동시킵니다.

이후 알파벳 범위를 넘으면 처음으로 돌아오도록 처리합니다.

마지막으로 0이 나올 때까지 각 입력을 반복해 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var sb = new StringBuilder();
    while (true) {
      var key = Console.ReadLine();
      if (key == null || key == "0") break;
      var text = Console.ReadLine()!;

      var outSb = new StringBuilder(text.Length);
      for (var i = 0; i < text.Length; i++) {
        var k = key[i % key.Length] - 'A' + 1;
        var v = text[i] - 'A' + k;
        v %= 26;
        outSb.Append((char)('A' + v));
      }

      sb.AppendLine(outSb.ToString());
    }

    Console.Write(sb);
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

  string key;
  while (cin >> key) {
    if (key == "0") break;
    string text; cin >> text;

    string out;
    out.reserve(text.size());
    for (int i = 0; i < (int)text.size(); i++) {
      int k = key[i % (int)key.size()] - 'A' + 1;
      int v = text[i] - 'A' + k;
      v %= 26;
      out.push_back(char('A' + v));
    }

    cout << out << "\n";
  }

  return 0;
}
```
