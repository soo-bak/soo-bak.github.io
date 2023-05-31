---
layout: single
title: "[백준 26906] Vikingahackare (C#, C++) - soo:bak"
date: "2023-03-27 16:31:00 +0900"
description: 구현과 이진수를 다루는 것을 주제로 하는 백준 26906번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [26906번 - Vikingahackare](https://www.acmicpc.net/problem/26906)

## 설명
바이킹들의 `룬 문자` 를 해석한다는 내용의 재미있는 구현 문제입니다. <br>

문제의 목표는 바이킹이 사용한 `룬 문자`를 번역하는 것 입니다. <br>

번역을 위해서 `이진수` 로 구성된 문자열이 주어지며, 만약 번역할 수 없는 `룬 문자`라면 `?` 를 대신 출력합니다.

`룬 문자` 와 `이진수` 의 관계를 저장하기 위하여 `map(C++), dictionary(C#)` 자료구조를 선택하였습니다. <br>

이후, 번역해야 하는 문자열을 `4`자 단위로 자른 후, 해당 `이진수` 가 매핑되어 있는지 확인합니다. <br>

- `이진수` 가 매핑되어 있으면, 해당 `룬 문자` 를 결과 문자열에 추가합니다.
- `이진수` 가 매핑되어 있지 않으면, `?` 를 결과 문자열에 추가합니다.

<br>
최종적으로, 해독한 결과 문자열을 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {
      var cntCode = int.Parse(Console.ReadLine()!);

      var decodeDictionary = new Dictionary<string, char>();

      for (var i = 0; i < cntCode; i++) {
        var input = Console.ReadLine()?.Split(' ');
        var c = input![0][0];
        var code = input![1];
        decodeDictionary[code] = c;
      }

      var rune = Console.ReadLine()!;

      var ans = "";
      for (var i = 0; i < rune.Length; i += 4) {
        var subStr = rune.Substring(i, 4);
        if (decodeDictionary.ContainsKey(subStr))
          ans += decodeDictionary[subStr];
        else ans += "?";
      }

      Console.WriteLine(ans);

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

typedef map<string, char> msc;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntCode; cin >> cntCode;
  msc decodeMap;

  for (int i = 0; i < cntCode; ++i) {
    char c; string code; cin >> c >> code;
    decodeMap[code] = c;
  }

  string rune; cin >> rune;

  string ans = "";
  for (size_t i = 0; i < rune.length(); i += 4) {
    string substring = rune.substr(i, 4);
    if (decodeMap.find(substring) != decodeMap.end())
      ans += decodeMap[substring];
    else ans += "?";
  }

  cout << ans << "\n";

  return 0;
}
  ```
