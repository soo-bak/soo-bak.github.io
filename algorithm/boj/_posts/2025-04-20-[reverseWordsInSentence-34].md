---
layout: single
title: "[백준 9093] 단어 뒤집기 (C#, C++) - soo:bak"
date: "2025-04-20 22:33:00 +0900"
description: 문장 속 단어들의 순서를 유지한 채 각 단어만 뒤집어서 출력하는 백준 9093번 단어 뒤집기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9093
  - C#
  - C++
  - 알고리즘
keywords: "백준 9093, 백준 9093번, BOJ 9093, reverseWordsInSentence, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9093번 - 단어 뒤집기](https://www.acmicpc.net/problem/9093)

## 설명
**주어진 문장에서 각 단어의 단위는 그대로 유지하되, 각 단어내의 문자들만을 반대로 뒤집어 출력하는 문제입니다.**
<br>

- 입력으로 주어지는 문장은 공백으로 구분된 여러 단어들로 이루어져 있습니다.
- 출력 시에는 단어들의 순서는 그대로 유지하고, 단어 내부의 문자 순서만 반전시킵니다.


## 접근법

- 테스트케이스 수를 입력받은 뒤, 각 문장을 한 줄씩 읽습니다.
- 한 줄을 공백 단위로 나누어 단어를 구분합니다.
- 각 단어를 문자열 단위로 뒤집고, 공백으로 연결해 출력합니다.
- 시간 복잡도는 입력 문자열의 총 길이를 `n`이라 할 때 `O(n)`이 됩니다.

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var sr = new StreamReader(Console.OpenStandardInput());
    var sb = new StringBuilder();

    int t = int.Parse(sr.ReadLine());
    while (t-- > 0) {
      string[] words = sr.ReadLine().Split(' ', StringSplitOptions.RemoveEmptyEntries);
        for (int i = 0; i < words.Length; i++) {
          char[] ch = words[i].ToCharArray();
          Array.Reverse(ch);
          sb.Append(ch);
          if (i < words.Length - 1) sb.Append(' ');
        }
        sb.Append('\n');
    }

      Console.Write(sb.ToString());
      sr.Close();
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
  cin.ignore();
  while (t--) {
    string line, word;
    getline(cin, line);
    istringstream iss(line);
    bool isFirst = true;
    while (iss >> word) {
      if (!isFirst) cout << " ";
      reverse(word.begin(), word.end());
      cout << word;
      isFirst = false;
    }
    cout << "\n";
  }

  return 0;
}
```
