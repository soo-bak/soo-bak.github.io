---
layout: single
title: "[백준 25192] 인사성 밝은 곰곰이 (C#, C++) - soo:bak"
date: "2025-12-07 01:05:00 +0900"
description: 곰곰티콘 사용 횟수를 구하는 백준 25192번 인사성 밝은 곰곰이 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[25192번 - 인사성 밝은 곰곰이](https://www.acmicpc.net/problem/25192)

## 설명
채팅 기록이 주어질 때, 곰곰티콘 사용 횟수를 구하는 문제입니다. ENTER가 나오면 새 세션이 시작되고, 각 세션에서 처음 채팅하는 사용자만 곰곰티콘으로 인사합니다.

<br>

## 접근법
먼저, 세션별로 등장한 닉네임을 집합에 저장합니다. 같은 세션에서 동일 닉네임은 한 번만 인사하므로 집합을 사용하면 중복이 자동으로 제거됩니다.

다음으로, ENTER가 나오면 현재 집합의 크기를 답에 더하고 집합을 비웁니다. 일반 닉네임이면 집합에 추가합니다.

이후, 입력이 끝나면 마지막 세션의 집합 크기를 답에 더합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var set = new HashSet<string>();
      var ans = 0;

      for (var i = 0; i < n; i++) {
        var s = Console.ReadLine()!;
        if (s == "ENTER") {
          ans += set.Count;
          set.Clear();
        } else set.Add(s);
      }

      ans += set.Count;
      Console.WriteLine(ans);
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
  unordered_set<string> st;
  int ans = 0;

  for (int i = 0; i < n; i++) {
    string s; cin >> s;
    if (s == "ENTER") {
      ans += st.size();
      st.clear();
    } else st.insert(s);
  }

  ans += st.size();
  cout << ans << "\n";

  return 0;
}
```
