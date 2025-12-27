---
layout: single
title: "[백준 27930] 당신은 운명을 믿나요? (C#, C++) - soo:bak"
date: "2025-12-27 15:15:00 +0900"
description: "백준 27930번 C#, C++ 풀이 - 문자열에서 YONSEI와 KOREA 중 먼저 완성되는 부분수열을 찾는 문제"
tags:
  - 백준
  - BOJ
  - 27930
  - C#
  - C++
  - 알고리즘
keywords: "백준 27930, 백준 27930번, BOJ 27930, DoYouBelieveInDestiny, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[27930번 - 당신은 운명을 믿나요?](https://www.acmicpc.net/problem/27930)

## 설명
점괘 문자열에서 순서를 유지한 채 글자를 제거해 YONSEI 또는 KOREA를 만들 수 있는지 확인합니다. 먼저 완성되는 학교를 출력하는 문제입니다.

<br>

## 접근법
문자열을 앞에서부터 순회하며 두 단어의 진행 상태를 동시에 관리합니다.

현재 글자가 각 단어의 다음 글자와 일치하면 해당 인덱스를 증가시키고, 먼저 완성되는 단어를 반환합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static string GetSchool(string s) {
    var yonsei = "YONSEI";
    var korea = "KOREA";
    var yIdx = 0;
    var kIdx = 0;

    foreach (var ch in s) {
      if (yIdx < yonsei.Length && ch == yonsei[yIdx]) {
        yIdx++;
        if (yIdx == yonsei.Length) return yonsei;
      }
      if (kIdx < korea.Length && ch == korea[kIdx]) {
        kIdx++;
        if (kIdx == korea.Length) return korea;
      }
    }
    return "";
  }

  static void Main() {
    var s = Console.ReadLine()!;
    Console.WriteLine(GetSchool(s));
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

string getSchool(const string& s) {
  string yonsei = "YONSEI", korea = "KOREA";
  int yIdx = 0, kIdx = 0;

  for (char ch : s) {
    if (ch == yonsei[yIdx]) {
      yIdx++;
      if (yIdx == (int)yonsei.size()) return yonsei;
    }
    if (ch == korea[kIdx]) {
      kIdx++;
      if (kIdx == (int)korea.size()) return korea;
    }
  }

  return "";
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s; cin >> s;
  cout << getSchool(s) << "\n";

  return 0;
}
```

