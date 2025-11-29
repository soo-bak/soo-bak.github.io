---
layout: single
title: "[백준 1991] 트리 순회 (C#, C++) - soo:bak"
date: "2025-11-29 15:10:00 +0900"
description: 전위, 중위, 후위 순회를 모두 출력하기 위해 각 노드의 좌우 자식을 저장한 뒤 재귀적으로 방문하는 백준 1991번 트리 순회 문제의 C# 및 C++ 풀이
---

## 문제 링크
[1991번 - 트리 순회](https://www.acmicpc.net/problem/1991)

## 설명

알파벳 대문자로 이름 붙은 이진 트리가 주어집니다. 항상 루트는 A이며, 각 노드의 왼쪽·오른쪽 자식이 문자로 제시되고 자식이 없으면 `.`으로 나타냅니다.  
입력된 트리를 기준으로

- 전위 순회 (루트 → 왼쪽 → 오른쪽)
- 중위 순회 (왼쪽 → 루트 → 오른쪽)
- 후위 순회 (왼쪽 → 오른쪽 → 루트)

결과를 한 줄씩 출력하면 됩니다.

<br>

## 접근법

- 노드 이름이 A부터 시작하므로 인덱스를 `node - 'A'`로 환산해 좌우 자식을 배열에 저장합니다.
- 재귀 함수를 각각 작성해 전위, 중위, 후위 순회를 수행합니다.  
  자식 문자가 `'.'`이면 더 내려가지 않습니다.
- 각 순회 결과를 차례대로 출력합니다.  
시간 복잡도 O(N), 추가 공간은 노드 저장용 O(N)입니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

namespace Solution {
  class Program {
    static readonly char[,] children = new char[26, 2];
    static readonly StringBuilder sb = new StringBuilder();

    static void Preorder(char node) {
      if (node == '.') return;
      sb.Append(node);
      int idx = node - 'A';
      Preorder(children[idx, 0]);
      Preorder(children[idx, 1]);
    }

    static void Inorder(char node) {
      if (node == '.') return;
      int idx = node - 'A';
      Inorder(children[idx, 0]);
      sb.Append(node);
      Inorder(children[idx, 1]);
    }

    static void Postorder(char node) {
      if (node == '.') return;
      int idx = node - 'A';
      Postorder(children[idx, 0]);
      Postorder(children[idx, 1]);
      sb.Append(node);
    }

    static void Main(string[] args) {
      int n = int.Parse(Console.ReadLine()!);
      for (int i = 0; i < n; i++) {
        var parts = Console.ReadLine()!.Split();
        int idx = parts[0][0] - 'A';
        children[idx, 0] = parts[1][0];
        children[idx, 1] = parts[2][0];
      }

      Preorder('A');
      sb.Append('\n');
      Inorder('A');
      sb.Append('\n');
      Postorder('A');

      Console.Write(sb.ToString());
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

char childNode[26][2];

void preorder(char node, string& out) {
  if (node == '.') return;
  out.push_back(node);
  int idx = node - 'A';
  preorder(childNode[idx][0], out);
  preorder(childNode[idx][1], out);
}

void inorder(char node, string& out) {
  if (node == '.') return;
  int idx = node - 'A';
  inorder(childNode[idx][0], out);
  out.push_back(node);
  inorder(childNode[idx][1], out);
}

void postorder(char node, string& out) {
  if (node == '.') return;
  int idx = node - 'A';
  postorder(childNode[idx][0], out);
  postorder(childNode[idx][1], out);
  out.push_back(node);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  for (int i = 0; i < n; i++) {
    char cur, left, right; 
    cin >> cur >> left >> right;
    int idx = cur - 'A';
    childNode[idx][0] = left;
    childNode[idx][1] = right;
  }

  string ans;
  preorder('A', ans);
  ans.push_back('\n');
  inorder('A', ans);
  ans.push_back('\n');
  postorder('A', ans);

  cout << ans;
  return 0;
}
```
