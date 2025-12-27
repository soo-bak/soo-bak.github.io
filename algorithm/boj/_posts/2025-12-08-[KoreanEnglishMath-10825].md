---
layout: single
title: "[백준 10825] 국영수 (C#, C++) - soo:bak"
date: "2025-12-08 03:00:00 +0900"
description: 다중 정렬 기준(국어↓, 영어↑, 수학↓, 이름 사전순↑)으로 학생 목록을 정렬하는 백준 10825번 국영수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10825
  - C#
  - C++
  - 알고리즘
keywords: "백준 10825, 백준 10825번, BOJ 10825, KoreanEnglishMath, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10825번 - 국영수](https://www.acmicpc.net/problem/10825)

## 설명
학생의 이름과 국어, 영어, 수학 점수가 주어질 때, 여러 기준에 따라 정렬하여 이름을 출력하는 문제입니다. 국어 점수가 높은 순으로 정렬하고, 국어가 같으면 영어가 낮은 순, 영어도 같으면 수학이 높은 순, 모두 같으면 이름 사전순으로 정렬합니다.

<br>

## 접근법
각 학생의 정보를 저장한 뒤, 비교 함수를 정의하여 정렬합니다. 비교 함수에서는 첫 번째 기준이 다르면 그 기준으로 순서를 정하고, 같으면 다음 기준으로 넘어갑니다. 네 가지 기준을 순서대로 확인하면 됩니다. 정렬 후 이름만 순서대로 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Student {
  public string Name = "";
  public int K, E, M;
}

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var list = new List<Student>(n);
    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      list.Add(new Student {
        Name = parts[0],
        K = int.Parse(parts[1]),
        E = int.Parse(parts[2]),
        M = int.Parse(parts[3])
      });
    }

    list.Sort((a, b) => {
      if (a.K != b.K) return b.K.CompareTo(a.K);
      if (a.E != b.E) return a.E.CompareTo(b.E);
      if (a.M != b.M) return b.M.CompareTo(a.M);
      return string.Compare(a.Name, b.Name, StringComparison.Ordinal);
    });

    foreach (var s in list) Console.WriteLine(s.Name);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Info {
  string name;
  int k, e, m;
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vector<Info> v(n);
  for (int i = 0; i < n; i++) cin >> v[i].name >> v[i].k >> v[i].e >> v[i].m;

  sort(v.begin(), v.end(), [](const Info& a, const Info& b) {
    if (a.k != b.k) return a.k > b.k;
    if (a.e != b.e) return a.e < b.e;
    if (a.m != b.m) return a.m > b.m;
    return a.name < b.name;
  });

  for (auto &s : v) cout << s.name << "\n";

  return 0;
}
```
