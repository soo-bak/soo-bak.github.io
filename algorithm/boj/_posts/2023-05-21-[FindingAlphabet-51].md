---
layout: single
title: "[백준 10809] 알파벳 찾기 (C#, C++) - soo:bak"
date: "2023-05-21 12:39:00 +0900"
---

## 문제 링크
  [10809번 - 알파벳 찾기](https://www.acmicpc.net/problem/10809)

## 설명
입력으로 주어지는 단어에서 각 알파벳이 처음 등장하는 위치를 찾는 문제입니다. <br>

<br>
먼저, 알파벳의 개수인 `26` 개의 원소를 가진 배열을 생성하고, 각 원소를 `-1` 로 초기화합니다. <br>

이후, 입력된 단어를 첫 번째 문자부터 마지막 문자까지 순회하며 각 문자가 처음 등장하는 위치를 탐색합니다. <br>

이 때, 배열에 저장된 해당 알파벳의 위치가 아직 `-1` 인 경우에만 위치를 갱신합니다. <br>

탐색이 종료되면 알파벳 순서대로 배열의 원소를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var str = Console.ReadLine()!;

      var alphabet = Enumerable.Repeat(-1, 26).ToArray();
      for (int i = 0; i < str.Length; i++) {
        if (alphabet[str[i] - 'a'] == -1)
          alphabet[str[i] - 'a'] = i;
      }

      foreach (int idxFirst in alphabet)
        Console.Write($"{idxFirst} ");
      Console.WriteLine();

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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string str; cin >> str;

  vector<int> alphabet(26, -1);
  for (size_t i = 0; i < str.size(); i++) {
    if (alphabet[str[i] - 'a'] == -1)
      alphabet[str[i] - 'a'] = i;
  }

  for (const auto& idxFirst : alphabet)
    cout << idxFirst << " ";
  cout << "\n";

  return 0;
}
  ```
