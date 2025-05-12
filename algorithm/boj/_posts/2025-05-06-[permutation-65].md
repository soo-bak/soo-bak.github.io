---
layout: single
title: "[백준 9742] 순열 (C#, C++) - soo:bak"
date: 2025-05-06 00:00:00 +0900
description: 사전순으로 정렬된 문자 집합에서 주어진 위치의 순열을 생성하는 백준 9742번 순열 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[9742번 - 순열](https://www.acmicpc.net/problem/9742)

## 설명
**서로 다른 문자들로 이루어진 문자열**과 **정수 위치**가 주어졌을 때,

해당 문자열로 만들 수 있는 모든 순열 중 사전순으로 정렬했을 경우 특정 위치에 해당하는 순열을 출력하는 문제입니다.

- 문자열 길이는 최대 `10`이며, 중복 문자가 없습니다.
- 사전순으로 순열을 구성하되, 주어진 위치에 해당하는 순열만 출력해야 합니다.
- 해당 위치의 순열이 존재하지 않으면 `"No permutation"`을 출력합니다.

<br>

## 접근법
- 먼저 문자열을 정렬한 뒤, 백트래킹을 통해 가능한 모든 순열을 한 번씩 탐색합니다.
- 매 순열마다 순서를 세어가며, 목표 위치에 도달했을 때 해당 순열을 출력합니다.
- 문제에서 요구하는 특정 위치의 순열을 찾기 위한 전체 흐름은 다음과 같습니다:
  - 문자들을 정렬한 후 백트래킹을 시작합니다.
  - 순열이 완성될 때마다 개수를 누적하며, 누적 수가 목표 위치와 일치하면 해당 순열을 출력합니다.
  - 만약 끝까지 찾지 못하면 `"No permutation"`을 출력합니다.

<br>
> 참고 : [백트래킹(Backtracking)의 개념과 구조적 사고 - soo:bak](https://soo-bak.github.io/algorithm/theory/backTracking/)

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;
using System.Linq;
using System.Collections.Generic;

class Program {
  static int k, cnt;
  static bool found;
  static StringBuilder sb = new ();
  static List<char> p = new ();

  static void Backtrack(string s, bool[] used) {
    if (p.Count == s.Length) {
      if (++cnt == k) {
        found = true;
        foreach (var c in p) sb.Append(c);
        sb.AppendLine();
      }
      return;
    }
    for (int i = 0; i < s.Length; i++) {
      if (!used[i]) {
        used[i] = true;
        p.Add(s[i]);
        Backtrack(s, used);
        p.RemoveAt(p.Count - 1);
        used[i] = false;
      }
    }
  }

  static void Main() {
    string line;
    while ((line = Console.ReadLine()) != null) {
      var tokens = line.Split();
      var s = tokens[0].ToCharArray();
      k = int.Parse(tokens[1]);
      Array.Sort(s);
      var sortedStr = new string(s);

      cnt = 0;
      found = false;
      p.Clear();
      sb.Append(tokens[0]).Append(" ").Append(k).Append(" = ");
      Backtrack(sortedStr, new bool[s.Length]);
      if (!found) sb.AppendLine("No permutation");
    }
    Console.Write(sb);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<char> vc;
typedef vector<bool> vb;

int k, cnt;
bool found;
vc p;

void backtrack(string& s, vb& used) {
  if (p.size() == s.size()) {
    if (++cnt == k) {
      found = true;
      for (char c : p) cout << c;
      cout << "\n";
    }
    return;
  }
  for (size_t i = 0; i < s.size(); i++) {
    if (!used[i]) {
      used[i] = true;
      p.push_back(s[i]);
      backtrack(s, used);
      p.pop_back();
      used[i] = false;
    }
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s;
  while (cin >> s >> k) {
    cout << s << " " << k << " = ";
    p.clear();
    vb used(s.size());
    cnt = 0;
    found = false;
    sort(s.begin(), s.end());
    backtrack(s, used);
    if (!found) cout << "No permutation\n";
  }
  return 0;
}
```
