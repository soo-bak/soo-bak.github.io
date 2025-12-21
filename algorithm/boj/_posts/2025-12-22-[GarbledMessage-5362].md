---
layout: single
title: "[백준 5362] Garbled Message (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: iiing을 th로 치환해 원문을 복원하는 문제
---

## 문제 링크
[5362번 - Garbled Message](https://www.acmicpc.net/problem/5362)

## 설명
문장에서 iiing을 모두 th로 바꿔 원문을 복원하는 문제입니다.

<br>

## 접근법
입력을 한 줄씩 읽어 iiing을 th로 치환한 결과를 그대로 출력합니다.

이후 입력이 끝날 때까지 반복합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string? line;
    while ((line = Console.ReadLine()) != null) {
      Console.WriteLine(line.Replace("iiing", "th"));
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

  string line;
  while (getline(cin, line)) {
    string res;
    for (int i = 0; i < (int)line.size(); ) {
      if (i + 5 <= (int)line.size() && line.substr(i, 5) == "iiing") {
        res += "th";
        i += 5;
      } else {
        res.push_back(line[i]);
        i++;
      }
    }
    cout << res << "\n";
  }

  return 0;
}
```
