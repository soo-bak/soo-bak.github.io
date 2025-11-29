---
layout: single
title: "[백준 9576] 책 나눠주기 (C#, C++) - soo:bak"
date: "2025-11-29 12:20:00 +0900"
description: 구간을 끝점 기준으로 정렬한 뒤 각 학생에게 구간 내 가장 작은 남은 책을 주는 그리디로 최대 배정 수를 구하는 백준 9576번 책 나눠주기 문제의 C# 및 C++ 풀이
---

## 문제 링크
[9576번 - 책 나눠주기](https://www.acmicpc.net/problem/9576)

## 설명

1번부터 N번까지 번호가 매겨진 N권의 책이 있고, M명의 학생이 각자 원하는 책의 범위를 제시하는 상황에서, 여러 테스트 케이스에 대해 N (1 ≤ N ≤ 1,000), M (1 ≤ M ≤ 1,000)과 각 학생이 원하는 범위 [a, b]가 주어질 때, 최대 몇 명의 학생에게 책을 나눠줄 수 있는지 구하는 문제입니다.

각 학생은 자신이 제시한 범위 내의 책 중 하나를 받을 수 있으며, 한 권의 책은 한 명에게만 줄 수 있습니다.

<br>

## 접근법

각 학생은 범위 내 아무 책이나 받을 수 있지만, 책의 개수가 제한되어 있어 모든 학생에게 줄 수 없는 경우가 있습니다.

최대한 많은 학생에게 책을 나눠주려면 선택 범위가 좁은 학생부터 처리해야 합니다.

<br>
선택 범위가 좁다는 것은 원하는 책의 끝 번호가 작다는 의미입니다.

끝 번호가 작을수록 선택지가 적고, 뒤로 미루면 다른 학생이 이미 가져가 받지 못할 확률이 높습니다.

<br>
예를 들어, 학생 A가 [1, 5]를, 학생 B가 [4, 5]를 원하는 경우를 생각해보면, 학생 A를 먼저 처리하여 5번을 주면 학생 B는 4번만 선택할 수 있지만, 학생 B를 먼저 처리하여 4번을 주면 학생 A는 1, 2, 3, 5번 중 선택할 수 있어 둘 다 책을 받을 수 있습니다.

<br>
따라서 모든 학생의 요청을 끝 번호 기준 오름차순으로 정렬하고, 끝 번호가 같다면 시작 번호 기준 오름차순으로 정렬합니다.

정렬된 순서대로 각 학생에게 범위 내에서 가장 번호가 작은 남은 책을 배정합니다.

<br>
예를 들어, N = 5이고 3명의 학생이 [1, 2], [2, 3], [3, 5]를 원하는 경우:

끝 번호 순서대로 이미 정렬되어 있으므로:
- [1, 2] → 1번 책 배정
- [2, 3] → 2번 책 배정 (3번도 가능하지만 작은 번호 선택)
- [3, 5] → 3번 책 배정
- 결과: 3명 모두 받음

<br>
다른 예로, N = 3이고 3명의 학생이 [1, 3], [1, 3], [1, 3]을 원하는 경우:

끝 번호가 모두 3이고 시작 번호도 같으므로 순서는 임의적이지만:
- 첫 번째 학생 → 1번 배정
- 두 번째 학생 → 2번 배정
- 세 번째 학생 → 3번 배정
- 결과: 3명 모두 받음

<br>
이 방법은 정렬에 O(M log M), 각 학생마다 최대 N권 확인에 O(M×N)이 소요되어 전체 시간 복잡도는 O(M log M + M×N)입니다.

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
      var t = int.Parse(Console.ReadLine()!);
      
      while (t-- > 0) {
        var input = Console.ReadLine()!.Split();
        var n = int.Parse(input[0]);
        var m = int.Parse(input[1]);
        
        var requests = new List<(int start, int end)>(m);
        for (var i = 0; i < m; i++) {
          var range = Console.ReadLine()!.Split();
          requests.Add((int.Parse(range[0]), int.Parse(range[1])));
        }

        requests.Sort((x, y) => x.end != y.end ? x.end.CompareTo(y.end) : x.start.CompareTo(y.start));

        var used = new bool[n + 1];
        var count = 0;

        foreach (var req in requests) {
          for (var book = req.start; book <= req.end; book++) {
            if (!used[book]) {
              used[book] = true;
              count++;
              break;
            }
          }
        }

        Console.WriteLine(count);
      }
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef pair<int, int> pii;
typedef vector<pii> vpii;
typedef vector<bool> vb;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  
  while (t--) {
    int n, m; cin >> n >> m;
    vpii requests(m);
    
    for (int i = 0; i < m; i++)
      cin >> requests[i].first >> requests[i].second;

    sort(requests.begin(), requests.end(), [](const pii& x, const pii& y) {
      if (x.second != y.second) return x.second < y.second;
      return x.first < y.first;
    });

    vb used(n + 1, false);
    int count = 0;

    for (const auto& req : requests) {
      for (int book = req.first; book <= req.second; book++) {
        if (!used[book]) {
          used[book] = true;
          count++;
          break;
        }
      }
    }

    cout << count << "\n";
  }
  
  return 0;
}
```

