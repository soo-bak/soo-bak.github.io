---
layout: single
title: "[백준 27058] Message Decowding (C#, C++) - soo:bak"
date: "2026-03-02 20:04:00 +0900"
description: "백준 27058번 C#, C++ 풀이 - 치환 암호 키를 이용해 메시지를 복호화하는 문제"
tags:
  - 백준
  - BOJ
  - 27058
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 27058, 백준 27058번, BOJ 27058, Message Decowding, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[27058번 - Message Decowding](https://www.acmicpc.net/problem/27058)

## 설명
알파벳 소문자 26개로 이루어진 복호화 키와 암호문이 주어질 때, 각 문자를 대응되는 원래 문자로 바꾸어 메시지를 복원하는 문제입니다. 공백은 그대로 두고, 대문자와 소문자는 원래 형태를 유지해야 합니다.

<br>

## 접근법
키의 각 위치는 암호문 알파벳이 어떤 문자로 복호화되는지를 뜻합니다. 따라서 알파벳 26개에 대한 대응표를 만든 뒤, 메시지를 왼쪽부터 보면서 알파벳이면 대응되는 문자로 바꾸고 공백은 그대로 출력하면 됩니다. 대문자는 복호화한 뒤 다시 대문자로 바꾸면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var key = Console.ReadLine()!;
    var message = Console.ReadLine()!;

    var map = new char[26];
    for (var i = 0; i < 26; i++)
      map[i] = key[i];

    var sb = new StringBuilder();
    foreach (var ch in message) {
      if (ch == ' ') {
        sb.Append(' ');
      } else if ('a' <= ch && ch <= 'z') {
        sb.Append(map[ch - 'a']);
      } else {
        var lower = (char)(ch - 'A' + 'a');
        var decoded = map[lower - 'a'];
        sb.Append((char)(decoded - 'a' + 'A'));
      }
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

  string key, message;
  getline(cin, key);
  getline(cin, message);

  char mp[26];
  for (int i = 0; i < 26; i++)
    mp[i] = key[i];

  string answer;
  answer.reserve(message.size());
  for (char ch : message) {
    if (ch == ' ') {
      answer.push_back(' ');
    } else if ('a' <= ch && ch <= 'z') {
      answer.push_back(mp[ch - 'a']);
    } else {
      char lower = char(ch - 'A' + 'a');
      char decoded = mp[lower - 'a'];
      answer.push_back(char(decoded - 'a' + 'A'));
    }
  }

  cout << answer << "\n";

  return 0;
}
```
