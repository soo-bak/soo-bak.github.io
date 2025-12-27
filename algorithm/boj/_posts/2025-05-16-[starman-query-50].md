---
layout: single
title: "[백준 12791] Starman (C#, C++) - soo:bak"
date: "2025-05-16 21:11:00 +0900"
description: 데이빗 보위의 앨범 목록 중 주어진 연도 구간에 포함되는 항목을 필터링하는 백준 12791번 Starman 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 12791
  - C#
  - C++
  - 알고리즘
  - 구현
  - precomputation
keywords: "백준 12791, 백준 12791번, BOJ 12791, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12791번 - Starman](https://www.acmicpc.net/problem/12791)

## 설명

**David Bowie의 앨범 발매 연도 정보 중, 특정 연도 구간에 포함되는 앨범들을 출력하는 문제입니다.**

주어진 질의는 다음 형식을 따릅니다:

- `S E`: `S년 1월 1일`부터 `E년 12월 31일`까지의 범위 내에서 발매된 앨범 목록을 찾는 질의

<br>
각 질의에 대해 조건을 만족하는 앨범의 수를 먼저 출력하고,

이후 해당 앨범들의 **발매 연도와 제목**을 입력 순서대로 출력합니다.

<br>
앨범 이름은 문제에 주어진 그대로 출력해야 하며, 띄어쓰기나 대소문자도 정확히 일치해야 합니다.

<br>

## 접근법

- 데이빗 보위의 앨범 정보를 `{연도, 제목}` 형태의 배열로 미리 정의해둡니다.
- 각 질의마다 `S`와 `E`를 입력받고, 이 구간에 속하는 앨범만 추출합니다.
- 출력 시에는 조건에 맞는 앨범 수를 먼저 출력하고, 이어서 줄마다 `"연도 제목"` 형식으로 출력합니다.

입력 질의 수는 최대 `100개`이므로, 단순 선형 탐색으로도 충분히 빠르게 처리할 수 있습니다.

<br>

---

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var albums = new List<(int, string)> {
      (1967, "DavidBowie"), (1969, "SpaceOddity"), (1970, "TheManWhoSoldTheWorld"),
      (1971, "HunkyDory"), (1972, "TheRiseAndFallOfZiggyStardustAndTheSpidersFromMars"),
      (1973, "AladdinSane"), (1973, "PinUps"), (1974, "DiamondDogs"),
      (1975, "YoungAmericans"), (1976, "StationToStation"), (1977, "Low"),
      (1977, "Heroes"), (1979, "Lodger"), (1980, "ScaryMonstersAndSuperCreeps"),
      (1983, "LetsDance"), (1984, "Tonight"), (1987, "NeverLetMeDown"),
      (1993, "BlackTieWhiteNoise"), (1995, "1.Outside"), (1997, "Earthling"),
      (1999, "Hours"), (2002, "Heathen"), (2003, "Reality"),
      (2013, "TheNextDay"), (2016, "BlackStar")
    };

    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var parts = Console.ReadLine().Split();
      int s = int.Parse(parts[0]), e = int.Parse(parts[1]);

      var res = new List<(int, string)>();
      foreach (var album in albums) {
        if (album.Item1 >= s && album.Item1 <= e)
          res.Add(album);
      }

      Console.WriteLine(res.Count);
      foreach (var (year, title) in res)
        Console.WriteLine($"{year} {title}");
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef pair<int, string> pis;
typedef vector<pis> vpis;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  pis albums[] = {
    {1967, "DavidBowie"}, {1969, "SpaceOddity"}, {1970, "TheManWhoSoldTheWorld"},
    {1971, "HunkyDory"}, {1972, "TheRiseAndFallOfZiggyStardustAndTheSpidersFromMars"},
    {1973, "AladdinSane"}, {1973, "PinUps"}, {1974, "DiamondDogs"}, {1975, "YoungAmericans"},
    {1976, "StationToStation"}, {1977, "Low"}, {1977, "Heroes"}, {1979, "Lodger"},
    {1980, "ScaryMonstersAndSuperCreeps"}, {1983, "LetsDance"}, {1984, "Tonight"}, {1987, "NeverLetMeDown"},
    {1993, "BlackTieWhiteNoise"}, {1995, "1.Outside"}, {1997, "Earthling"}, {1999, "Hours"},
    {2002, "Heathen"}, {2003, "Reality"}, {2013, "TheNextDay"}, {2016, "BlackStar"}
  };

  int t; cin >> t;
  while (t--) {
    int s, e; cin >> s >> e;
    vpis res;
    for (auto& [year, name] : albums)
      if (year >= s && year <= e) res.emplace_back(year, name);

    cout << res.size() << "\n";
    for (const auto& [year, name] : res)
      cout << year << " " << name << "\n";
  }

  return 0;
}
```
