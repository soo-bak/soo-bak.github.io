---
layout: single
title: "[백준 15460] My Cow Ate My Homework (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: suffix의 합과 최솟값으로 각 K별 제거 후 평균을 구해 최대 평균을 만드는 K들을 찾는 문제
tags:
  - 백준
  - BOJ
  - 15460
  - C#
  - C++
  - 알고리즘
keywords: "백준 15460, 백준 15460번, BOJ 15460, MyCowAteMyHomework, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15460번 - My Cow Ate My Homework](https://www.acmicpc.net/problem/15460)

## 설명
N개의 점수에서 앞의 K개를 제거한 뒤, 남은 점수 중 최솟값 하나를 추가로 제거하고 평균을 구할 때, 이 평균이 최대가 되는 모든 K를 찾는 문제입니다.

<br>

## 접근법
앞에서 K개를 제거한 뒤 남은 점수들 중 최솟값을 하나 더 빼고 평균을 구합니다. 점수가 3, 1, 9, 2, 7이고 K = 2라면 앞의 2개를 제거해 9, 2, 7이 남고, 최솟값 2를 빼면 9와 7만 남아 평균은 8이 됩니다.

K는 1부터 N - 2까지 가능합니다. K가 0이면 아무것도 제거하지 않는 것이고, K가 N - 1 이상이면 남은 원소가 2개 미만이라 최솟값을 빼면 평균을 낼 수 없기 때문입니다.

각 K에 대해 남은 구간의 합과 최솟값을 매번 처음부터 계산하면 시간이 오래 걸립니다. K = 1일 때는 인덱스 1부터 끝까지, K = 2일 때는 인덱스 2부터 끝까지를 봐야 하는데, 이 구간들은 모두 끝이 같고 시작만 다릅니다. 끝이 고정된 구간들의 합과 최솟값은 뒤에서부터 누적하면 한 번에 구할 수 있습니다.

인덱스 i에서 끝까지의 합은 인덱스 i + 1에서 끝까지의 합에 현재 값을 더한 것입니다. 최솟값도 마찬가지로, 인덱스 i + 1에서 끝까지의 최솟값과 현재 값 중 작은 것이 인덱스 i에서 끝까지의 최솟값이 됩니다. 이렇게 미리 계산해두면 각 K에 대해 해당 구간의 합과 최솟값을 바로 알 수 있습니다.

K개를 제거하면 남은 원소는 N - K개이고, 최솟값 하나를 빼므로 평균은 (구간 합 - 구간 최솟값) / (N - K - 1)로 계산됩니다. 모든 K에 대해 평균을 계산하여 최댓값을 찾고, 그 최댓값과 같은 평균을 만드는 K들을 모두 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var arr = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);

    var sumSuf = new int[n + 1];
    var minSuf = new int[n];
    sumSuf[n] = 0;
    var curMin = int.MaxValue;
    for (var i = n - 1; i >= 0; i--) {
      sumSuf[i] = sumSuf[i + 1] + arr[i];
      if (arr[i] < curMin) curMin = arr[i];
      minSuf[i] = curMin;
    }

    var best = -1.0;
    var ans = new List<int>();
    for (var k = 1; k <= n - 2; k++) {
      var len = n - k;
      var avg = (double)(sumSuf[k] - minSuf[k]) / (len - 1);
      if (avg > best + 1e-12) {
        best = avg;
        ans.Clear();
        ans.Add(k);
      } else if (Math.Abs(avg - best) <= 1e-12) ans.Add(k);
    }

    foreach (var k in ans)
      Console.WriteLine(k);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vi a(n);
  for (int i = 0; i < n; i++) cin >> a[i];

  vi sumSuf(n + 1, 0), minSuf(n);
  int curMin = INT_MAX;
  for (int i = n - 1; i >= 0; i--) {
    sumSuf[i] = sumSuf[i + 1] + a[i];
    curMin = min(curMin, a[i]);
    minSuf[i] = curMin;
  }

  double best = -1;
  vi ans;
  for (int k = 1; k <= n - 2; k++) {
    int len = n - k;
    double avg = double(sumSuf[k] - minSuf[k]) / double(len - 1);
    if (avg > best + 1e-12) {
      best = avg;
      ans.clear();
      ans.push_back(k);
    } else if (fabs(avg - best) <= 1e-12) ans.push_back(k);
  }

  for (int k : ans)
    cout << k << "\n";

  return 0;
}
```
