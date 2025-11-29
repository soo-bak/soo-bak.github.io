---
layout: single
title: "[백준 1991] 트리 순회 (C#, C++) - soo:bak"
date: "2025-11-29 22:00:00 +0900"
description: 전위, 중위, 후위 순회를 모두 출력하기 위해 각 노드의 좌우 자식을 저장한 뒤 재귀적으로 방문하는 백준 1991번 트리 순회 문제의 C# 및 C++ 풀이
---

## 문제 링크
[1991번 - 트리 순회](https://www.acmicpc.net/problem/1991)

## 설명

이진 트리의 구조가 주어지는 상황에서, 노드의 개수 N (1 ≤ N ≤ 26)과 각 노드의 정보(노드 이름, 왼쪽 자식, 오른쪽 자식)가 주어질 때, 전위 순회, 중위 순회, 후위 순회 결과를 각각 한 줄씩 출력하는 문제입니다.

노드는 A부터 순서대로 알파벳 대문자로 표현되며, 항상 A가 루트 노드입니다. 자식이 없는 경우에는 `.`으로 표시됩니다.

<br>

## 접근법

이진 트리의 세 가지 순회 방식은 각각 다음과 같습니다:

- **전위 순회(Preorder)**: 루트 → 왼쪽 서브트리 → 오른쪽 서브트리
- **중위 순회(Inorder)**: 왼쪽 서브트리 → 루트 → 오른쪽 서브트리
- **후위 순회(Postorder)**: 왼쪽 서브트리 → 오른쪽 서브트리 → 루트

<br>
각 노드의 왼쪽 자식과 오른쪽 자식 정보를 저장한 후, 재귀적으로 트리를 순회하면 됩니다.

재귀 함수는 현재 노드를 방문하고, 순회 방식에 따라 노드를 출력하는 시점을 달리합니다.

자식이 없는 경우(`.`으로 표시된 경우)는 더 이상 내려가지 않고 종료합니다.

<br>
예를 들어, 다음과 같은 트리가 있다면:

```
    A
   / \
  B   C
 / \
D   E
```

- 전위 순회: A → B → D → E → C
- 중위 순회: D → B → E → A → C
- 후위 순회: D → E → B → C → A

<br>
각 노드를 한 번씩만 방문하므로 시간 복잡도는 O(N)입니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Text;

namespace Solution {
  class Program {
    static readonly Dictionary<char, (char left, char right)> tree = new();
    static readonly StringBuilder result = new();

    static void Preorder(char node) {
      if (node == '\0') return;
      result.Append(node);
      var (left, right) = tree[node];
      Preorder(left);
      Preorder(right);
    }

    static void Inorder(char node) {
      if (node == '\0') return;
      var (left, right) = tree[node];
      Inorder(left);
      result.Append(node);
      Inorder(right);
    }

    static void Postorder(char node) {
      if (node == '\0') return;
      var (left, right) = tree[node];
      Postorder(left);
      Postorder(right);
      result.Append(node);
    }

    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      for (var i = 0; i < n; i++) {
        var input = Console.ReadLine()!.Split();
        var node = input[0][0];
        var left = input[1][0] == '.' ? '\0' : input[1][0];
        var right = input[2][0] == '.' ? '\0' : input[2][0];
        tree[node] = (left, right);
      }

      Preorder('A');
      result.Append('\n');
      Inorder('A');
      result.Append('\n');
      Postorder('A');

      Console.Write(result.ToString());
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef map<char, pair<char, char>> Tree;

Tree tree;

void preorder(char node) {
  if (node == '\0') return;
  cout << node;
  preorder(tree[node].first);
  preorder(tree[node].second);
}

void inorder(char node) {
  if (node == '\0') return;
  inorder(tree[node].first);
  cout << node;
  inorder(tree[node].second);
}

void postorder(char node) {
  if (node == '\0') return;
  postorder(tree[node].first);
  postorder(tree[node].second);
  cout << node;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  for (int i = 0; i < n; i++) {
    char node, left, right;
    cin >> node >> left >> right;
    if (left == '.') left = '\0';
    if (right == '.') right = '\0';
    tree[node] = {left, right};
  }

  preorder('A');
  cout << "\n";
  inorder('A');
  cout << "\n";
  postorder('A');
  cout << "\n";
  
  return 0;
}
```


