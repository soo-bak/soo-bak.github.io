---
layout: single
title: "[백준 26264] 빅데이터? 정보보호! (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 문자열에서 bigdata/security 개수를 세어 비교해 출력하는 백준 26264번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[26264번 - 빅데이터? 정보보호!](https://www.acmicpc.net/problem/26264)

## 설명
문자열에서 bigdata와 security의 등장 횟수를 비교하는 문제입니다.

<br>

## 접근법
bigdata는 길이 7, security는 길이 8입니다.

문자열을 순회하며 시작 문자가 b인지 s인지 확인하고, 해당 단어 길이만큼 건너뛰며 개수를 셉니다.

이후, 개수 비교 결과에 따라 적절한 문자열을 출력합니다.

<br>

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;
    var cntB = 0;
    var cntS = 0;
    for (var i = 0; i < s.Length; ) {
      if (s[i] == 'b') { cntB++; i += 7; }
      else { cntS++; i += 8; }
    }
    if (cntB > cntS) Console.WriteLine("bigdata?");
    else if (cntB < cntS) Console.WriteLine("security!");
    else Console.WriteLine("bigdata? security!");
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

  int n; cin >> n;
  string s; cin >> s;
  int cntB = 0, cntS = 0;
  for (size_t i = 0; i < s.size(); ) {
    if (s[i] == 'b') { cntB++; i += 7; }
    else { cntS++; i += 8; }
  }
  if (cntB > cntS) cout << "bigdata?\n";
  else if (cntB < cntS) cout << "security!\n";
  else cout << "bigdata? security!\n";

  return 0;
}
```
