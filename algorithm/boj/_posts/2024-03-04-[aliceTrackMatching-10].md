---
layout: single
title: "[백준 31428] 엘리스 트랙 매칭 (C#, C++) - soo:bak"
date: "2024-03-04 02:08:00 +0900"
description: 구현, 문자열 등을 주제로 하는 백준 31428번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 31428
  - C#
  - C++
  - 알고리즘
keywords: "백준 31428, 백준 31428번, BOJ 31428, aliceTrackMatching, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [31428번 - 엘리스 트랙 매칭](https://www.acmicpc.net/problem/31428)

## 설명
'헬로빗' 과 친구들이 지원하는 '엘리스 트랙' 정보를 바탕으로,<br>
<br>
헬로빗이 지원하는 트랙과 동일한 트랙을 지원하는 친구들의 수를 찾아내는 문제입니다.<br>
<br>
<br>
입력의 첫 줄에 주어지는 헬로빗의 친구 수를 바탕으로, 각 트랙 정보 `C`, `S`, `I`, `A` 중 헬로빗의 친구들의 트랙 정보를 입력받아 저장합니다.<br>
<br>
이후, 헬로빗이 지원하는 트랙 정보를 입력받아, 친구들의 트랙 정보를 순회하며 헬로빗의 트랙 정보와 동일한 경우를 탐색합니다.<br>
<br>
<br>
최종적으로, 헬로빗이 지원하는 트랙과 동일한 트랙을 지원하는 친구들의 수를 출력합니다.<br>

<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var friendsTracks = Console.ReadLine()!.Split(' ').Select(str => str.FirstOrDefault()).ToArray();
      var hellobitTrack = Console.ReadLine()!.FirstOrDefault();

      var sameTrackCount = friendsTracks.Count(track => track == hellobitTrack);

      Console.WriteLine(sameTrackCount);

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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vector<char> friendsTracks(n);
  for (int i = 0; i < n; i++)
    cin >> friendsTracks[i];

  char hellobitTrack; cin >> hellobitTrack;

  int sameTrackCount = 0;
  for (char track : friendsTracks) {
    if (track == hellobitTrack)
      sameTrackCount++;
  }

  cout << sameTrackCount << "\n";

  return 0;
}
  ```
