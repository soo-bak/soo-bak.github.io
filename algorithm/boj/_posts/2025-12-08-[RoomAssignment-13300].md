---
layout: single
title: "[백준 13300] 방 배정 (C#, C++) - soo:bak"
date: "2025-12-08 03:55:00 +0900"
description: 성별·학년별 인원을 세어 방 정원 k로 나눈 올림을 합산하는 백준 13300번 방 배정 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[13300번 - 방 배정](https://www.acmicpc.net/problem/13300)

## 설명
학생들을 방에 배정할 때, 같은 성별과 같은 학년끼리만 같은 방을 쓸 수 있습니다. 한 방에 최대 k명까지 들어갈 수 있을 때 필요한 방의 최소 개수를 구하는 문제입니다.

<br>

## 접근법
성별과 학년 조합별로 인원을 셉니다. 성별은 2가지, 학년은 6가지이므로 총 12개의 그룹이 있습니다.

각 그룹의 인원을 방 정원으로 나눈 뒤 올림하면 그 그룹에 필요한 방 수가 됩니다. 모든 그룹의 방 수를 더하면 답이 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var k = int.Parse(first[1]);
    var cnt = new int[2, 7];
    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var s = int.Parse(parts[0]);
      var y = int.Parse(parts[1]);
      cnt[s, y]++;
    }
    var rooms = 0;
    for (var s = 0; s < 2; s++) {
      for (var y = 1; y <= 6; y++) {
        var c = cnt[s, y];
        if (c > 0) rooms += (c + k - 1) / k;
      }
    }
    Console.WriteLine(rooms);
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

  int n, k; cin >> n >> k;
  int cnt[2][7] = {0};
  for (int i = 0; i < n; i++) {
    int s, y; cin >> s >> y;
    cnt[s][y]++;
  }
  int rooms = 0;
  for (int s = 0; s < 2; s++) {
    for (int y = 1; y <= 6; y++) {
      int c = cnt[s][y];
      if (c > 0) rooms += (c + k - 1) / k;
    }
  }
  cout << rooms << "\n";

  return 0;
}
```
