---
layout: single
title: "[백준 2422] 한윤정이 이탈리아에 가서 아이스크림을 사먹는데 (C#, C++) - soo:bak"
date: "2025-11-24 23:45:00 +0900"
description: 금지된 조합을 불리언 행렬로 표시한 뒤 세 가지 아이스크림을 삼중 루프로 검사해 가능한 경우의 수를 세는 백준 2422번 문제의 C# 및 C++ 풀이
---

## 문제 링크
[2422번 - 한윤정이 이탈리아에 가서 아이스크림을 사먹는데](https://www.acmicpc.net/problem/2422)

## 설명

N개의 아이스크림 종류가 있고, 특정 조합은 함께 먹으면 안 되는 금지 조합입니다.

M개의 금지 조합이 주어질 때, 서로 다른 세 가지 아이스크림을 선택하는 경우의 수를 구하는 문제입니다.

선택한 세 가지 중 어떤 두 가지도 금지 조합에 포함되지 않아야 합니다.

<br>

## 접근법

금지 조합을 2차원 배열에 표시하여 빠르게 확인할 수 있도록 합니다.

두 아이스크림 i와 j가 금지 조합이면 배열의 해당 위치를 참으로 표시합니다.

예를 들어, 1번과 2번이 금지 조합이면 배열[1][2]와 배열[2][1]을 모두 참으로 설정합니다.

<br>
서로 다른 세 가지 아이스크림을 선택하는 모든 조합을 삼중 반복문으로 확인합니다.

N이 최대 200이므로 O(N³) 시간 복잡도로 충분합니다.

<br>
반복문에서 i < j < k 순서를 유지하여 중복을 방지합니다.

세 개를 선택할 때, i와 j, i와 k, j와 k가 각각 금지 조합인지 확인합니다.

예를 들어, 1, 2, 3을 선택할 때 (1,2), (1,3), (2,3) 모두 금지 조합이 아니어야 가능한 경우입니다.

금지 조합이 하나라도 있으면 건너뛰고, 모두 통과하면 경우의 수를 증가시킵니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var first = Console.ReadLine()!.Split();
      var n = int.Parse(first[0]);
      var m = int.Parse(first[1]);

      var bad = new bool[n + 1, n + 1];

      for (var i = 0; i < m; i++) {
        var line = Console.ReadLine()!.Split();
        var a = int.Parse(line[0]);
        var b = int.Parse(line[1]);

        bad[a, b] = bad[b, a] = true;
      }

      var ans = 0;

      for (var i = 1; i <= n - 2; i++) {
        for (var j = i + 1; j <= n - 1; j++) {
          if (bad[i, j]) continue;

          for (var k = j + 1; k <= n; k++) {
            if (bad[i, k] || bad[j, k]) continue;

            ans++;
          }
        }
      }

      Console.WriteLine(ans);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<vector<bool>> vvb;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  vvb bad(n + 1, vector<bool>(n + 1, false));

  for (int i = 0; i < m; i++) {
    int a, b; cin >> a >> b;
    bad[a][b] = bad[b][a] = true;
  }

  int ans = 0;

  for (int i = 1; i <= n - 2; i++) {
    for (int j = i + 1; j <= n - 1; j++) {
      if (bad[i][j]) continue;

      for (int k = j + 1; k <= n; k++) {
        if (bad[i][k] || bad[j][k]) continue;

        ++ans;
      }
    }
  }

  cout << ans << "\n";

  return 0;
}
```

