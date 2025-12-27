---
layout: single
title: "[백준 9946] 단어 퍼즐 (C#, C++) - soo:bak"
date: "2025-04-20 04:09:00 +0900"
description: 두 단어가 동일한 알파벳 조합으로 이루어져 있는지 정렬을 통해 비교하는 백준 9946번 단어 퍼즐 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9946
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
  - 정렬
keywords: "백준 9946, 백준 9946번, BOJ 9946, anagramCheck, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9946번 - 단어 퍼즐](https://www.acmicpc.net/problem/9946)

## 설명
**주어진 두 단어가 동일한 알파벳을 같은 개수로 가지고 있는지 판별하는 문제입니다.**
<br>

- 두 단어가 동일한 알파벳 조합으로 구성되어 있다면 `same`을 출력합니다.
- 그렇지 않다면 `different`를 출력합니다.
- 각 테스트케이스는 `"Case x:"` 형식으로 번호를 붙여 출력합니다.


## 접근법

1. 반복문을 통해 두 개의 단어를 입력받습니다.
2. 두 단어의 각 문자들을 오름차순 정렬하여 비교합니다.
   - 정렬 결과가 같다면 `same`, 다르면 `different`을 형식에 맞게 출력합니다.


## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int caseNum = 1;
    while (true) {
      string w = Console.ReadLine();
      string p = Console.ReadLine();
      if (w == "END" && p == "END") break;

      var wSorted = string.Concat(w.OrderBy(c => c));
      var pSorted = string.Concat(p.OrderBy(c => c));

      Console.WriteLine($"Case {caseNum++}: {(wSorted == pSorted ? "same" : "different")}");
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

  for (int i = 1;; i++) {
    string w, p; cin >> w >> p;
    if (w == "END" && p == "END") break;

    sort(w.begin(), w.end());
    sort(p.begin(), p.end());

    cout << "Case " << i << ": " << (w == p ? "same" : "different") << "\n";
  }

  return 0;
}
```
