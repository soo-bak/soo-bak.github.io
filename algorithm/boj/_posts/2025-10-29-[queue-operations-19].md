---
layout: single
title: "[백준 18258] 큐 2 (C#, C++) - soo:bak"
date: "2025-10-29 00:30:00 +0900"
description: 배열 기반 큐를 직접 구현하여 선입선출 연산을 빠르게 처리하는 백준 18258번 큐 2 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 18258
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 큐
keywords: "백준 18258, 백준 18258번, BOJ 18258, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18258번 - 큐 2](https://www.acmicpc.net/problem/18258)

## 설명

큐 자료구조의 기본 연산인 `push`, `pop`, `size`, `empty`, `front`, `back`을 직접 구현하는 문제입니다.<br>

최대 `2,000,000`개의 명령이 주어지며, 각 명령에 대한 결과를 순서대로 출력해야 합니다.<br>

큐가 비어 있을 때 `pop`, `front`, `back` 명령이 주어지면 `-1`을 출력합니다.<br>

<br>

## 접근법

배열 기반 큐를 직접 구현하여 문제를 해결합니다.

고정 크기 배열과 `front`, `rear` 인덱스를 사용하여 선입선출 구조를 구현합니다.

`push`는 `rear` 위치에 원소를 추가하고, `pop`은 `front` 위치의 원소를 제거합니다.

명령 개수가 최대 `2,000,000`개로 많기 때문에 빠른 입출력 처리가 필수적입니다.

출력 버퍼를 사용하여 모든 결과를 모았다가 한 번에 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var queue = new int[2_000_000];
    
    int n = int.Parse(Console.ReadLine()!);
    int front = 0, rear = 0;
    var output = new StringBuilder();

    for (int i = 0; i < n; i++) {
      var input = Console.ReadLine()!.Split();
      var cmd = input[0];

      if (cmd == "push")
        queue[rear++] = int.Parse(input[1]);
      else if (cmd == "pop")
        output.AppendLine(front < rear ? queue[front++].ToString() : "-1");
      else if (cmd == "size")
        output.AppendLine((rear - front).ToString());
      else if (cmd == "empty")
        output.AppendLine(front == rear ? "1" : "0");
      else if (cmd == "front")
        output.AppendLine(front < rear ? queue[front].ToString() : "-1");
      else if (cmd == "back")
        output.AppendLine(front < rear ? queue[rear - 1].ToString() : "-1");
    }

    Console.Write(output);
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

  int queue[2'000'000] = {0, };
  
  int front = 0, rear = 0;
  string output = "";

  int n; cin >> n;
  output.reserve(n * 10);

  while (n--) {
    string cmd; cin >> cmd;

    if (cmd == "push") {
      int x; cin >> x;
      queue[rear++] = x;
    } else if (cmd == "pop") {
      if (front < rear) output += to_string(queue[front++]) + '\n';
      else output += "-1\n";
    } else if (cmd == "size") {
      output += to_string(rear - front) + '\n';
    } else if (cmd == "empty") {
      output += (front == rear ? "1\n" : "0\n");
    } else if (cmd == "front") {
      if (front < rear) output += to_string(queue[front]) + '\n';
      else output += "-1\n";
    } else if (cmd == "back") {
      if (front < rear) output += to_string(queue[rear - 1]) + '\n';
      else output += "-1\n";
    }
  }

  cout << output << "\n";
  
  return 0;
}
```

 