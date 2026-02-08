---
layout: single
title: "[백준 5222] Vigenère Cipher (C#, C++) - soo:bak"
date: "2026-02-08 20:03:00 +0900"
description: "백준 5222번 C#, C++ 풀이 - 키워드를 반복해 비즈네르 암호로 평문을 암호화하는 문제"
tags:
  - 백준
  - BOJ
  - 5222
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 5222, 백준 5222번, BOJ 5222, Vigenere Cipher, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5222번 - Vigenère Cipher](https://www.acmicpc.net/problem/5222)

## 설명
대문자 키워드를 평문 길이에 맞춰 반복해 겹친 뒤, 각 자리에서 평문 문자에 키워드 문자를 더해 26으로 나눈 값으로 암호문을 만드는 비즈네르 암호화 문제입니다.

<br>

## 접근법
키 길이를 k라 두고 i번째 글자마다 키의 i % k번째 문자가 정해주는 칸수(문자-'A')만큼 알파벳을 원형으로 미는 시저 시프트를 적용합니다.

즉 (평문 - 'A' + shift) % 26에 다시 'A'를 더해 암호 문자를 구합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();
    for (int caseIdx = 0; caseIdx < t; caseIdx++) {
      var parts = Console.ReadLine()!.Split();
      var key = parts[0];
      var plain = parts[1];
      int k = key.Length;
      var outSb = new StringBuilder(plain.Length);
      for (int i = 0; i < plain.Length; i++) {
        int shift = key[i % k] - 'A';
        int c = (plain[i] - 'A' + shift) % 26 + 'A';
        outSb.Append((char)c);
      }
      sb.Append("Ciphertext: ").Append(outSb).Append('\n');
    }
    Console.Write(sb.ToString());
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

  int T; cin >> T;
  while (T--) {
    string key, plain; cin >> key >> plain;
    int k = key.size();
    string out;
    out.reserve(plain.size());
    for (size_t i = 0; i < plain.size(); i++) {
      int shift = key[i % k] - 'A';
      char c = char((plain[i] - 'A' + shift) % 26 + 'A');
      out.push_back(c);
    }
    cout << "Ciphertext: " << out << "\n";
  }

  return 0;
}
```
