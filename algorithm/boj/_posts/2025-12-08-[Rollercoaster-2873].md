---
layout: single
title: "[백준 2873] 롤러코스터 (C#, C++) - soo:bak"
date: "2025-12-08 01:20:00 +0900"
description: 격자 크기 홀짝에 따라 스네이크 경로를 만들고, 짝짝일 때는 제외할 칸을 골라 우회하는 백준 2873번 롤러코스터 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2873
  - C#
  - C++
  - 알고리즘
  - 구현
  - 그리디
  - 구성적
  - parity
keywords: "백준 2873, 백준 2873번, BOJ 2873, Rollercoaster, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2873번 - 롤러코스터](https://www.acmicpc.net/problem/2873)

## 설명
격자의 왼쪽 위에서 오른쪽 아래까지 이동하면서 최대한 많은 칸을 방문하여 기쁨의 합을 최대로 만드는 경로를 구하는 문제입니다.

<br>

## 접근법
모든 칸의 기쁨이 양수이므로, 기쁨의 합을 최대로 하려면 최대한 많은 칸을 방문해야 합니다. 핵심은 격자의 행과 열의 홀짝에 따라 모든 칸을 방문할 수 있는지가 달라진다는 점입니다.

<br>

먼저 행의 수가 홀수인 경우를 살펴봅니다. 예를 들어 3행 4열 격자라면 다음과 같이 이동합니다.

```
→ → → ↓
↓ ← ← ←
→ → → ◎
```

첫 행에서 오른쪽 끝까지 간 뒤 아래로 내려가고, 둘째 행에서 왼쪽 끝까지 간 뒤 다시 아래로 내려갑니다. 행이 홀수 개이면 마지막 행에서 오른쪽으로 가다가 도착점에서 끝나므로 모든 칸을 빠짐없이 방문할 수 있습니다.

<br>

다음으로 행의 수가 짝수이고 열의 수가 홀수인 경우입니다. 이번에는 열 방향으로 같은 패턴을 적용합니다. 예를 들어 4행 3열이라면 다음과 같습니다.

```
↓ ↑ ↓
↓ ↑ ↓
↓ ↑ ↓
→ → ◎
```

첫 열에서 아래 끝까지 간 뒤 오른쪽으로 이동하고, 둘째 열에서 위로 올라간 뒤 다시 오른쪽으로 이동합니다. 열이 홀수 개이면 마지막 열에서 아래로 가다가 도착점에서 끝나므로 역시 모든 칸을 방문합니다.

<br>

문제는 행과 열이 모두 짝수인 경우입니다. 2행 2열 격자를 생각해보면, 왼쪽 위에서 오른쪽 아래로 가면서 4칸을 모두 방문하는 경로는 존재하지 않습니다. 이것은 행과 열이 모두 짝수인 모든 격자에서 마찬가지입니다. 결국 정확히 한 칸을 건너뛰어야 합니다.

<br>

이때 아무 칸이나 건너뛸 수는 없습니다. 건너뛸 수 있는 칸은 행 번호와 열 번호의 합이 홀수인 칸들뿐입니다. 이 칸들 중에서 기쁨이 가장 작은 칸을 건너뛰면 됩니다.

<br>

경로를 만드는 방법은 다음과 같습니다. 건너뛸 칸이 포함된 연속한 두 행을 하나의 블록으로 묶어서 처리합니다. 그 위쪽 행들은 일반적인 지그재그로 내려오고, 그 아래쪽 행들도 마찬가지입니다.

핵심은 건너뛸 칸이 포함된 두 행입니다. 이 두 행에서는 세로로 왔다갔다 하면서 오른쪽으로 이동합니다. 건너뛸 칸 왼쪽에서는 아래로 내려갔다 오른쪽으로, 건너뛸 칸 오른쪽에서는 오른쪽으로 갔다 아래로 내려가는 식입니다.

예를 들어 4행 4열에서 0행 1열의 칸을 건너뛴다면 다음과 같이 이동합니다.

```
↓ X → →
→ → ↑ ↓
← ← ← ↓
→ → → ◎
```

0행 1열은 건너뛰고, 나머지 15칸을 모두 방문하여 도착점에 도달합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var r = int.Parse(first[0]);
    var c = int.Parse(first[1]);

    var joy = new int[r, c];
    var minVal = 1001;
    var minR = 0;
    var minC = 0;
    for (var i = 0; i < r; i++) {
      var parts = Console.ReadLine()!.Split();
      for (var j = 0; j < c; j++) {
        joy[i, j] = int.Parse(parts[j]);
        if (r % 2 == 0 && c % 2 == 0 && (i + j) % 2 == 1) {
          if (joy[i, j] < minVal) { minVal = joy[i, j]; minR = i; minC = j; }
        }
      }
    }

    var sb = new StringBuilder();

    if (r % 2 == 1) {
      for (var i = 0; i < r; i++) {
        for (var j = 0; j < c - 1; j++) sb.Append(i % 2 == 0 ? 'R' : 'L');
        if (i != r - 1) sb.Append('D');
      }
    } else if (c % 2 == 1) {
      for (var j = 0; j < c; j++) {
        for (var i = 0; i < r - 1; i++) sb.Append(j % 2 == 0 ? 'D' : 'U');
        if (j != c - 1) sb.Append('R');
      }
    } else {
      if (minR % 2 == 1) minR--;

      for (var i = 0; i < minR; i++) {
        for (var j = 0; j < c - 1; j++) sb.Append(i % 2 == 0 ? 'R' : 'L');
        sb.Append('D');
      }

      for (var j = 0; j < minC; j++) sb.Append(j % 2 == 0 ? "DR" : "UR");
      for (var j = minC; j < c - 1; j++) sb.Append(j % 2 == 0 ? "RD" : "RU");

      for (var i = minR + 2; i < r; i++) {
        sb.Append('D');
        for (var j = 0; j < c - 1; j++) sb.Append(i % 2 == 0 ? 'L' : 'R');
      }
    }

    Console.WriteLine(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<vi> vvi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int r, c; cin >> r >> c;
  vvi joy(r, vi(c));
  int minVal = 1001, minR = 0, minC = 0;
  for (int i = 0; i < r; i++) {
    for (int j = 0; j < c; j++) {
      cin >> joy[i][j];
      if (r % 2 == 0 && c % 2 == 0 && (i + j) % 2) {
        if (joy[i][j] < minVal) { minVal = joy[i][j]; minR = i; minC = j; }
      }
    }
  }

  string ans;
  if (r % 2) {
    for (int i = 0; i < r; i++) {
      for (int j = 0; j < c - 1; j++) ans.push_back(i % 2 ? 'L' : 'R');
      if (i != r - 1) ans.push_back('D');
    }
  } else if (c % 2) {
    for (int j = 0; j < c; j++) {
      for (int i = 0; i < r - 1; i++) ans.push_back(j % 2 ? 'U' : 'D');
      if (j != c - 1) ans.push_back('R');
    }
  } else {
    if (minR % 2) minR--;
    for (int i = 0; i < minR; i++) {
      for (int j = 0; j < c - 1; j++) ans.push_back(i % 2 ? 'L' : 'R');
      ans.push_back('D');
    }
    for (int j = 0; j < minC; j++) ans += (j % 2 ? "UR" : "DR");
    for (int j = minC; j < c - 1; j++) ans += (j % 2 ? "RU" : "RD");
    for (int i = minR + 2; i < r; i++) {
      ans.push_back('D');
      for (int j = 0; j < c - 1; j++) ans.push_back(i % 2 ? 'R' : 'L');
    }
  }

  cout << ans << "\n";

  return 0;
}
```
