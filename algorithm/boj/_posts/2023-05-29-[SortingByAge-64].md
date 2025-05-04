---
layout: single
title: "[백준 10814] 나이순 정렬 (C#, C++) - soo:bak"
date: "2023-05-29 20:44:00 +0900"
description: 정렬과 탐색 등을 주제로 하는 백준 10814번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [10814번 - 나이순 정렬](https://www.acmicpc.net/problem/10814)

## 설명
입력으로 주어지는 회원들의 나이와 이름을 정렬하는 문제입니다. <br>

정렬의 규칙은 다음과 같습니다. <br>

- 나이 순서대로 정렬 <br>
- 나이가 같다면 가입한 순서대로 정렬 <br>

이 때, 문제의 조건 중 <b>회원들이 가입한 순서는 입력의 순서와 같다</b> 는 조건이 있습니다. <br>

<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    class Member {
      public int Age { get; set; }
      public string? Name { get; set; }
      public int Order { get; set; }
    }

    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var members = new Member[n];
      for (int i = 0; i < n; i++) {
        var input = Console.ReadLine()!.Split(' ');
        members[i] = new Member { Age = int.Parse(input[0]), Name = input[1], Order = i};
      }

      var sortedMember = members
                        .OrderBy(m => m.Age)
                        .ThenBy(m => m.Order)
                        .ToArray();

      foreach (var member in sortedMember)
        Console.WriteLine($"{member.Age} {member.Name}");

    }
  }
}
  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

using namespace std;

typedef pair<int, string> pis;

bool comp(pis a, pis b) {
  return a.first < b.first;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vector<pis> members(n);
  for (int i = 0; i < n; i++)
    cin >> members[i].first >> members[i].second;

  stable_sort(members.begin(), members.end(), comp);

  for (const auto& member : members)
    cout << member.first << " " << member.second << "\n";

  return 0;
}
  ```
