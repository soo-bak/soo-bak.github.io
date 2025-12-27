---
layout: single
title: "[백준 17478] 재귀함수가 뭔가요? (C#, C++) - soo:bak"
date: "2025-12-07 03:05:00 +0900"
description: 재귀 깊이에 맞춰 들여쓰기를 늘리며 질문과 답변 대사를 출력하는 백준 17478번 재귀함수가 뭔가요 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17478
  - C#
  - C++
  - 알고리즘
keywords: "백준 17478, 백준 17478번, BOJ 17478, WhatIsRecursion, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17478번 - 재귀함수가 뭔가요?](https://www.acmicpc.net/problem/17478)

## 설명
N이 주어질 때, 재귀 구조로 질문과 답변 대사를 깊이에 따라 들여쓰기하며 출력하는 문제입니다.

<br>

## 접근법
재귀 함수를 사용하여 깊이에 따라 들여쓰기를 조절하며 대사를 출력합니다.

현재 깊이에 4를 곱한 만큼 언더스코어로 들여쓰기를 만듭니다. 먼저 질문을 출력하고, 깊이가 N에 도달하면 기저 답변을 출력한 뒤 반환합니다. 아직 N에 도달하지 않았다면 이야기 세 줄을 출력하고 깊이를 1 증가시켜 재귀 호출합니다.

재귀 호출이 반환된 후에는 해당 깊이의 들여쓰기로 마무리 대사를 출력합니다. 이렇게 하면 재귀가 깊어질수록 들여쓰기가 증가하고, 복귀하면서 역순으로 마무리됩니다.

<br>

- - -

## Code

### C#

```csharp
using System;

class Program {
  static int N;

  static void Dfs(int d) {
    string pre = new string('_', d * 4);
    Console.WriteLine($"{pre}\"재귀함수가 뭔가요?\"");
    if (d == N) {
      Console.WriteLine($"{pre}\"재귀함수는 자기 자신을 호출하는 함수라네\"");
      Console.WriteLine($"{pre}라고 답변하였지.");
      return;
    }
    Console.WriteLine($"{pre}\"잘 들어보게. 옛날옛날 한 산 꼭대기에 이세상 모든 지식을 통달한 선인이 있었어.");
    Console.WriteLine($"{pre}마을 사람들은 모두 그 선인에게 수많은 질문을 했고, 모두 지혜롭게 대답해 주었지.");
    Console.WriteLine($"{pre}그의 답은 대부분 옳았다고 하네. 그런데 어느 날, 그 선인에게 한 선비가 찾아와서 물었어.\"");
    Dfs(d + 1);
    Console.WriteLine($"{pre}라고 답변하였지.");
  }

  static void Main() {
    N = int.Parse(Console.ReadLine()!);
    Console.WriteLine("어느 한 컴퓨터공학과 학생이 유명한 교수님을 찾아가 물었다.");
    Dfs(0);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int N;

void dfs(int d) {
  string pre(d * 4, '_');
  cout << pre << "\"재귀함수가 뭔가요?\"\n";
  if (d == N) {
    cout << pre << "\"재귀함수는 자기 자신을 호출하는 함수라네\"\n";
    cout << pre << "라고 답변하였지.\n";
    return;
  }
  cout << pre << "\"잘 들어보게. 옛날옛날 한 산 꼭대기에 이세상 모든 지식을 통달한 선인이 있었어.\n";
  cout << pre << "마을 사람들은 모두 그 선인에게 수많은 질문을 했고, 모두 지혜롭게 대답해 주었지.\n";
  cout << pre << "그의 답은 대부분 옳았다고 하네. 그런데 어느 날, 그 선인에게 한 선비가 찾아와서 물었어.\"\n";
  dfs(d + 1);
  cout << pre << "라고 답변하였지.\n";
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> N;
  cout << "어느 한 컴퓨터공학과 학생이 유명한 교수님을 찾아가 물었다.\n";
  dfs(0);

  return 0;
}
```
