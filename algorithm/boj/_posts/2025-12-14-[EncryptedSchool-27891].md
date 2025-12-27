---
layout: single
title: "[백준 27891] 특별한 학교 이름 암호화 (C#, C++) - soo:bak"
date: "2025-12-14 09:03:00 +0900"
description: 암호문을 0~25칸 회전해 각 학교 이름 접두사와 일치하는지를 찾아 약칭을 출력하는 백준 27891번 문제의 C#/C++ 풀이
tags:
  - 백준
  - BOJ
  - 27891
  - C#
  - C++
  - 알고리즘
keywords: "백준 27891, 백준 27891번, BOJ 27891, EncryptedSchool, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[27891번 - 특별한 학교 이름 암호화](https://www.acmicpc.net/problem/27891)

## 설명
시저 암호로 암호화된 학교 이름이 주어질 때, 어떤 학교인지 찾는 문제입니다.

후보는 NLCS, BHA, KIS, SJA 네 개이며, 정식 명칭에서 공백과 문장 부호를 제거하고 소문자로 만든 뒤 앞 10글자만 사용합니다.

<br>

## 접근법
먼저 네 학교의 전처리된 이름을 준비합니다.

이후 암호문을 0부터 25까지 회전해 보며 각 학교 이름과 비교합니다.

일치하는 학교를 찾으면 해당 약칭을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static string Rotate(string s, int n) {
    var arr = s.ToCharArray();
    for (var i = 0; i < arr.Length; i++)
      arr[i] = (char)((arr[i] - 'a' + n) % 26 + 'a');
    return new string(arr);
  }

  static string Decode(string name) {
    var full = new[] {
      "northlondoncollegiateschool",
      "branksomehallasia",
      "koreainternationalschool",
      "stjohnsburyacademy"
    };
    var abbr = new[] { "NLCS", "BHA", "KIS", "SJA" };
    for (var i = 0; i < 26; i++) {
      var decoded = Rotate(name, i);
      for (var j = 0; j < full.Length; j++) {
        if (full[j].Substring(0, 10) == decoded)
          return abbr[j];
      }
    }
    return "";
  }

  static void Main() {
    var name = Console.ReadLine()!;
    Console.WriteLine(Decode(name));
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<string> vs;

string rotate(string s, int n) {
  for (char& c : s)
    c = (c - 'a' + n) % 26 + 'a';
  return s;
}

string decode(string name) {
  vs full = {
    "northlondoncollegiateschool",
    "branksomehallasia",
    "koreainternationalschool",
    "stjohnsburyacademy"
  };
  vs abbr = {"NLCS", "BHA", "KIS", "SJA"};
  for (int i = 0; i < 26; ++i) {
    string decoded = rotate(name, i);
    for (size_t j = 0; j < full.size(); ++j) {
      if (full[j].substr(0, 10) == decoded)
        return abbr[j];
    }
  }
  return "";
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string name; cin >> name;
  cout << decode(name) << "\n";

  return 0;
}
```
