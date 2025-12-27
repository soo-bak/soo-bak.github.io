---
layout: single
title: "[백준 2263] 트리의 순회 (C#, C++) - soo:bak"
date: "2025-12-01 19:03:00 +0900"
description: 인오더와 포스트오더가 주어졌을 때 인덱스 매핑과 분할 정복으로 프리오더를 복원하는 백준 2263번 트리의 순회 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2263
  - C#
  - C++
  - 알고리즘
keywords: "백준 2263, 백준 2263번, BOJ 2263, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2263번 - 트리의 순회](https://www.acmicpc.net/problem/2263)

## 설명

이진 트리의 순회 결과가 주어지는 상황에서, 노드의 개수 n (1 ≤ n ≤ 100,000)과 인오더(중위 순회) 결과, 포스트오더(후위 순회) 결과가 주어질 때, 프리오더(전위 순회) 결과를 구하는 문제입니다.

세 가지 순회 방식은 다음과 같습니다:
- 인오더(중위): 왼쪽 서브트리 → 루트 → 오른쪽 서브트리
- 포스트오더(후위): 왼쪽 서브트리 → 오른쪽 서브트리 → 루트
- 프리오더(전위): 루트 → 왼쪽 서브트리 → 오른쪽 서브트리

포스트오더의 마지막 원소가 루트이며, 인오더에서 루트의 위치를 찾으면 좌우 서브트리를 구분할 수 있습니다. 이 성질을 이용하여 재귀적으로 프리오더를 복원합니다.

<br>

## 접근법

분할 정복과 재귀를 사용하여 인오더와 포스트오더로부터 프리오더를 복원합니다.

<br>
먼저 인오더 배열에서 각 값의 인덱스를 저장하는 매핑을 만듭니다. 이렇게 하면 루트 노드를 찾았을 때 인오더에서의 위치를 O(1)에 찾을 수 있습니다.

재귀 함수를 정의합니다. 함수는 인오더의 구간 [inL, inR]과 포스트오더의 구간 [postL, postR]을 받습니다. 포스트오더의 마지막 원소 postorder[postR]이 현재 서브트리의 루트입니다. 이 루트를 프리오더 순서대로 먼저 출력합니다.

이후, 인오더에서 루트의 위치를 찾습니다. 루트의 인덱스를 idx라 하면, 왼쪽 서브트리의 크기는 idx - inL입니다. 이 크기를 이용하여 인오더와 포스트오더를 각각 왼쪽 서브트리와 오른쪽 서브트리 구간으로 나눕니다.

왼쪽 서브트리에 대해 재귀 호출을 먼저 수행하고, 그 다음 오른쪽 서브트리에 대해 재귀 호출합니다. 이렇게 하면 프리오더 순서(루트 → 왼쪽 → 오른쪽)로 출력됩니다.

<br>
예를 들어, 인오더가 [4, 2, 5, 1, 6, 3, 7], 포스트오더가 [4, 5, 2, 6, 7, 3, 1]인 경우:

포스트오더의 마지막 원소 1이 루트입니다. 인오더에서 1의 위치는 인덱스 3이므로, 왼쪽 서브트리는 [4, 2, 5] (크기 3), 오른쪽 서브트리는 [6, 3, 7]입니다.

왼쪽 서브트리의 포스트오더는 [4, 5, 2]이고 마지막 원소 2가 루트입니다. 이를 재귀적으로 반복하면 프리오더는 1 → 2 → 4 → 5 → 3 → 6 → 7 순서로 출력됩니다.

<br>
각 노드를 한 번씩만 방문하므로 시간 복잡도는 O(n)입니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

namespace Solution {
  class Program {
    static int[] inorder, postorder, pos;
    static StringBuilder sb = new StringBuilder();

    static void Solve(int inL, int inR, int postL, int postR) {
      if (inL > inR || postL > postR)
        return;

      var root = postorder[postR];
      sb.Append(root).Append(' ');

      var idx = pos[root];
      var leftSize = idx - inL;

      Solve(inL, idx - 1, postL, postL + leftSize - 1);
      Solve(idx + 1, inR, postL + leftSize, postR - 1);
    }

    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      inorder = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      postorder = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      pos = new int[n + 1];

      for (var i = 0; i < n; i++)
        pos[inorder[i]] = i;

      Solve(0, n - 1, 0, n - 1);
      Console.WriteLine(sb.ToString().TrimEnd());
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> inorder, postorder, posIdx;
ostringstream out;

void solve(int inL, int inR, int postL, int postR) {
  if (inL > inR || postL > postR)
    return;

  int root = postorder[postR];
  out << root << ' ';

  int idx = posIdx[root];
  int leftSize = idx - inL;

  solve(inL, idx - 1, postL, postL + leftSize - 1);
  solve(idx + 1, inR, postL + leftSize, postR - 1);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  inorder.resize(n);
  postorder.resize(n);
  posIdx.assign(n + 1, 0);

  for (int i = 0; i < n; i++)
    cin >> inorder[i];
  for (int i = 0; i < n; i++)
    cin >> postorder[i];
  for (int i = 0; i < n; i++)
    posIdx[inorder[i]] = i;

  solve(0, n - 1, 0, n - 1);
  string res = out.str();
  if (!res.empty() && res.back() == ' ')
    res.pop_back();
  cout << res << "\n";

  return 0;
}
```
