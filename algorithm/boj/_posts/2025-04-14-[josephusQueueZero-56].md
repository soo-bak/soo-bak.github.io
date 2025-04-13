---
layout: single
title: "[백준 11866] 요세푸스 문제 0 (C#, C++) - soo:bak"
date: "2025-04-14 01:55:19 +0900"
description: 큐 자료구조를 활용해 순환적으로 사람을 제거하는 요세푸스 문제를 해결하는 백준 11866번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[11866번 - 요세푸스 문제 0](https://www.acmicpc.net/problem/11866)

## 설명
이 문제는 고전적인 **요세푸스 문제**를 큐 자료구조로 구현하는 문제입니다.
`N` 명의 사람이 원을 이루고 있을 때, `K` 번째 사람을 제거하는 것을 반복하여 제거 순서를 출력해야 합니다.

### 접근법
- 큐에 `1` 부터 `N` 까지의 수를 모두 삽입합니다.
- `K-1` 번 앞의 사람을 뒤로 보내고, `K` 번째 사람을 제거하여 출력합니다.
- 큐의 크기가 `1` 이 될 때까지 반복합니다.

`< >`로 감싸고, 각 숫자는 `, `로 구분해야 하는 출력 형식에 주의합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System.Text;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var input = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      var num = input[0];
      var ord = input[1];

      var q = new Queue<int>(Enumerable.Range(1, num));
      var sb = new StringBuilder();
      sb.Append('<');

      while (q.Count > 1) {
        for (int i = 0; i < ord - 1; i++) {
          q.Enqueue(q.Dequeue());
        }
        sb.Append(q.Dequeue()).Append(", ");
      }
      sb.Append(q.Dequeue()).Append('>');
      Console.WriteLine(sb.ToString());
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int num, ord; cin >> num >> ord;

  queue<int> q;
  for (int i = 1; i <= num; i++)
    q.push(i);

  cout << '<';

  while (q.size() != 1) {
    int cnt = 1;
    while (cnt < ord) {
      q.push(q.front());
      q.pop();
      cnt++;
    }
    cout << q.front() << ", ";
    q.pop();
  }
  cout << q.front() << ">
";

  return 0;
}
```
