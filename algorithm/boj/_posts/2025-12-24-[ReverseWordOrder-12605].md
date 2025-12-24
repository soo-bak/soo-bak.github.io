---
layout: single
title: "[백준 12605] 단어순서 뒤집기 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: 문장을 단어 단위로 뒤집어 출력하는 문제
---

## 문제 링크
[12605번 - 단어순서 뒤집기](https://www.acmicpc.net/problem/12605)

## 설명
각 문장의 단어 순서를 반대로 뒤집어 출력하는 문제입니다.

<br>

## 접근법
문장을 공백 기준으로 나누고, 역순으로 이어 출력합니다.

케이스 번호 형식에 맞춰 `"Case #x: "`를 앞에 붙입니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var tc = 1; tc <= t; tc++) {
      var line = Console.ReadLine()!;
      var parts = line.Split(' ');
      Array.Reverse(parts);
      Console.WriteLine($"Case #{tc}: {string.Join(" ", parts)}");
    }
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

  int t; cin >> t;
  string line;
  getline(cin, line);

  for (int tc = 1; tc <= t; tc++) {
    getline(cin, line);
    stringstream ss(line);
    vector<string> words;
    string w;
    while (ss >> w) words.push_back(w);
    reverse(words.begin(), words.end());

    cout << "Case #" << tc << ": ";
    for (int i = 0; i < (int)words.size(); i++) {
      if (i) cout << " ";
      cout << words[i];
    }
    cout << "\n";
  }

  return 0;
}
```
