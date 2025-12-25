---
layout: single
title: "[백준 18245] 이상한 나라의 암호 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: i번째 줄을 i칸씩 건너뛰며 읽어 해석한 결과를 출력하는 문제
---

## 문제 링크
[18245번 - 이상한 나라의 암호](https://www.acmicpc.net/problem/18245)

## 설명
여러 줄의 문장이 주어질 때, i번째 줄은 첫 글자에서 시작해 i칸씩 건너뛰며 읽어 해석한 결과를 출력하는 문제입니다.

<br>

## 접근법
i번째 줄은 간격이 i칸이므로 실제로는 인덱스를 `i+1`씩 증가시키며 문자를 선택합니다.  
각 줄에 대해 0번 인덱스부터 `i+1` 간격으로 문자를 모아 출력하면 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var outSb = new StringBuilder();
    var idx = 1;

    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;
      if (line == "Was it a cat I saw?") break;

      var step = idx + 1;
      var sb = new StringBuilder();
      for (var i = 0; i < line.Length; i += step)
        sb.Append(line[i]);

      outSb.AppendLine(sb.ToString());
      idx++;
    }

    Console.Write(outSb);
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
  int idx = 1;
  while (getline(cin, line)) {
    if (line == "Was it a cat I saw?") break;
    int step = idx + 1;
    string res;
    for (int i = 0; i < (int)line.size(); i += step)
      res.push_back(line[i]);
    cout << res << "\n";
    idx++;
  }

  return 0;
}
```
