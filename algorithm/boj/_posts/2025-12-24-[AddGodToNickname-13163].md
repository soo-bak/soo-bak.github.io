---
layout: single
title: "[백준 13163] 닉네임에 갓 붙이기 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: 첫 음절을 god으로 바꾸고 나머지 음절을 붙이는 문제
---

## 문제 링크
[13163번 - 닉네임에 갓 붙이기](https://www.acmicpc.net/problem/13163)

## 설명
공백으로 나뉜 음절에서 첫 음절을 god으로 바꾸고 이어 붙이는 문제입니다.

<br>

## 접근법
각 줄에서 첫 번째 음절을 제외한 나머지 음절들을 공백 없이 이어 붙입니다.

이후 앞에 god을 붙여 새로운 닉네임을 만들어 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < n; i++) {
      var line = Console.ReadLine()!;
      var idx = line.IndexOf(' ');
      var rest = line.Substring(idx + 1).Replace(" ", "");
      Console.WriteLine("god" + rest);
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

  int n; cin >> n;
  string line;
  getline(cin, line);
  for (int i = 0; i < n; i++) {
    getline(cin, line);
    int pos = line.find(' ');
    string rest = line.substr(pos + 1);
    rest.erase(remove(rest.begin(), rest.end(), ' '), rest.end());
    cout << "god" << rest << "\n";
  }

  return 0;
}
```
