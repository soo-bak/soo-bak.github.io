---
layout: single
title: "[백준 15916] 가희는 그래플러야!! (C#, C++) - soo:bak"
date: "2025-11-29 11:55:00 +0900"
description: 구간 점화로 그린 꺾은선 f(x)와 직선 y=kx의 교점을 찾기 위해 정수 지점에서의 부호 변화를 확인해 O(n)에 판정하는 백준 15916번 문제의 C# 및 C++ 풀이
---

## 문제 링크
[15916번 - 가희는 그래플러야!!](https://www.acmicpc.net/problem/15916)

## 설명

좌표평면에서 n개의 y 좌표 값 y₁, y₂, ..., yₙ과 정수 k가 주어지는 상황에서, n (1 ≤ n ≤ 100,000)과 각 y 좌표 (|yᵢ| ≤ 2³⁰), k (|k| ≤ 2³⁰)가 주어질 때, 특정 조건으로 만들어진 꺾은선 그래프와 직선 y = kx가 원점 외의 점에서 교차하는지 판별하는 문제입니다.

두 그래프가 원점이 아닌 다른 점에서 만나면 "T"를, 만나지 않으면 "F"를 출력합니다.

<br>

## 접근법

꺾은선 그래프는 원점 (0, 0)을 지나 각 정수 x = i마다 점 (i, yᵢ)를 연결한 것입니다.

직선 y = kx와의 교점을 찾기 위해, 각 점에서의 기울기를 관찰합니다.

<br>
원점에서 점 (i, yᵢ)로 이어지는 선분의 기울기는 yᵢ / i입니다.

만약 직선의 기울기 k가 이러한 기울기들 중 하나와 같다면, 그 점에서 교차합니다.

더 일반적으로, k가 모든 기울기들의 최솟값과 최댓값 사이에 있다면, 꺾은선의 어딘가에서 반드시 교차합니다.

<br>
구체적으로:
- 각 점 (i, yᵢ)에 대해 기울기 gᵢ = yᵢ / i를 계산
- 모든 기울기 중 최솟값 gₘᵢₙ과 최댓값 gₘₐₓ를 구함
- gₘᵢₙ ≤ k ≤ gₘₐₓ이면 교차함

<br>
예를 들어, n = 3, y = [3, 4, 3], k = 1일 때:
- 점 (1, 3): 기울기 = 3/1 = 3
- 점 (2, 4): 기울기 = 4/2 = 2
- 점 (3, 3): 기울기 = 3/3 = 1
- 기울기 범위: [1, 3]
- k = 1은 범위 내 → "T"

다른 예로, n = 2, y = [2, 4], k = 3일 때:
- 점 (1, 2): 기울기 = 2/1 = 2
- 점 (2, 4): 기울기 = 4/2 = 2
- 기울기 범위: [2, 2]
- k = 3은 범위 밖 → "F"

<br>
이 방법은 각 점의 기울기를 한 번씩만 확인하므로 O(n) 시간에 해결할 수 있습니다.

<br>

> 관련 문제: [[백준 12781] PIZZA ALVOLOC (C#, C++) - soo:bak](https://soo-bak.github.io/algorithm/boj/pizza-cross-12781)

> 관련 문제: [[백준 10255] 교차점 (C#, C++) - soo:bak](https://soo-bak.github.io/algorithm/boj/segment-rectangle-10255)

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var input = Console.ReadLine()!.Split();
      
      var gradientMin = double.MaxValue;
      var gradientMax = double.MinValue;
      
      for (var i = 1; i <= n; i++) {
        var y = double.Parse(input[i - 1]);
        var gradient = y / i;
        gradientMin = Math.Min(gradientMin, gradient);
        gradientMax = Math.Max(gradientMax, gradient);
      }
      
      var k = double.Parse(Console.ReadLine()!);
      
      if (k >= gradientMin && k <= gradientMax)
        Console.WriteLine("T");
      else
        Console.WriteLine("F");
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
  double gradientMin = INT_MAX;
  double gradientMax = 0;
  
  for (int i = 1; i <= n; i++) {
    double y; cin >> y;
    double gradient = y / i;
    gradientMin = min(gradientMin, gradient);
    gradientMax = max(gradientMax, gradient);
  }
  
  double k; cin >> k;
  
  if (k >= gradientMin && k <= gradientMax) cout << "T\n";
  else cout << "F\n";
    
  return 0;
}
```

