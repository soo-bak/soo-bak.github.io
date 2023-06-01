---
layout: single
title: "[백준 1966] 프린터 큐 (C#, C++) - soo:bak"
date: "2023-06-01 17:31:00 +0900"
description: 큐, 우선순위 큐 등을 주제로 하는 백준 1966번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [1966번 - 프린터 큐](https://www.acmicpc.net/problem/1966)

## 설명
`큐(Queue)` 자료구조를 주제로 하는 문제입니다. <br>

문제의 입력으로 주어지는 각 문서들의 중요도를 고려하여, 특정 문서가 인쇄되는 순서를 알아내는 문제입니다. <br>

중요도를 고려하여 인쇄되는 순서에 관한 규칙은 다음과 같습니다. <br>

- 현재 Queue 의 가장 앞에 있는 문서의 중요도를 확인<br>
- 나머지 문서들 중 현재 문서보다 중요도가 높은 문서가 하나라도 존재한다면, 해당 문서를 인쇄하지 않고 Queue 의 가장 뒤로 재배치,<br>
  그렇지 않다면 바로 인쇄<br>

위 규칙에 따라서 특정 문서가 인쇄되는 순서를 확인한 후 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    public class Document {
      public int Index { get; set; }
      public int Priority { get; set; }
    }

    static void Main(string[] args) {

      var cntCase = int.Parse(Console.ReadLine()!);

      for (int c = 0; c < cntCase; c++) {
        var input = Console.ReadLine()!.Split(' ');
        var n = int.Parse(input[0]);
        var m = int.Parse(input[1]);
        var priorities = Console.ReadLine()!.Split(' ');

        Queue<Document> queue = new Queue<Document>();
        List<int> sortedPriorities = new List<int>();
        for (int i = 0; i < n; i++) {
          var document = new Document {
            Index = i,
            Priority = int.Parse(priorities[i])
          };

          queue.Enqueue(document);
          sortedPriorities.Add(document.Priority);
        }

        sortedPriorities.Sort();
        sortedPriorities.Reverse();

        int ans = 0;
        while (queue.Count > 0) {
          var currentDocument = queue.Dequeue();

          if (currentDocument.Priority == sortedPriorities[0]) {
            ans++;
            sortedPriorities.RemoveAt(0);

            if (currentDocument.Index == m) {
              Console.WriteLine(ans);
              break ;
            }
          } else queue.Enqueue(currentDocument);
        }
      }

    }
  }
}
  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

using namespace std;

typedef pair<int, int> pii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntCase; cin >> cntCase;

  for (int c = 0; c < cntCase; c++) {
    int n, m; cin >> n >> m;

    queue<pii> q;
    priority_queue<int> pq;
    for (int i = 0; i < n; i++) {
      int val; cin >> val;
      q.push({i, val});
      pq.push(val);
    }

    int ans = 0;
    while (!q.empty()) {
      int idx = q.front().first;
      int val = q.front().second;

      q.pop();

      if (pq.top() == val) {
        pq.pop();
        ans++;
        if (idx == m) {
          cout << ans << "\n";
          break ;
        }
      } else q.push({idx, val});
    }
  }

  return 0;
}
  ```
