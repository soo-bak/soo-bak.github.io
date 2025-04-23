---
layout: single
title: "[백준 10769] 행복한지 슬픈지 (C#, C++) - soo:bak"
date: "2025-04-23 00:43:00 +0900"
description: 문자열에서 등장하는 감정 이모티콘의 개수를 기준으로 전체 감정 상태를 판별하는 백준 10769번 행복한지 슬픈지 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10769번 - 행복한지 슬픈지](https://www.acmicpc.net/problem/10769)

## 설명
문자열 속에서 특정 감정을 나타내는 기호들을 세어, 전체 분위기가 어떤지를 판별하는 간단한 문자열 처리 문제입니다.<br><br>

- 감정을 나타내는 이모티콘은 다음 두 가지입니다:
  - `:-)` → 웃는 얼굴 (happy)
  - `:-(` → 슬픈 얼굴 (sad)

- 주어진 문자열 전체에서 위 두 가지 이모티콘이 각각 몇 번 등장하는지를 세어야 합니다.
- 감정 판정 기준은 다음과 같습니다:
  - 두 이모티콘 모두 없으면 `"none"`
  - 웃는 얼굴이 더 많으면 `"happy"`
  - 슬픈 얼굴이 더 많으면 `"sad"`
  - 같으면 `"unsure"`

문자열의 길이는 최대 `255`자이며, 줄 단위로 한 번에 입력됩니다.

## 접근법
- 입력 문자열을 한 줄 통째로 읽어 들입니다.
- 세 글자씩 끊어서 순차적으로 확인하면서 이모티콘 패턴이 등장하는지를 검사합니다.
- 패턴이 `":-)"`이면 `happy` 카운트를, `":-("`이면 `sad` 카운트를 증가시킵니다.
- 최종적으로 두 개의 카운트를 비교해 해당하는 결과 문자열을 출력합니다.

이 문제는 문자열 탐색만 수행하므로, 시간 복잡도는 `O(n)` 입니다.

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    string s = Console.ReadLine();
    int happy = 0, sad = 0;

    for (int i = 0; i + 2 < s.Length; i++) {
      if (s[i] == ':' && s[i + 1] == '-') {
        if (s[i + 2] == ')') happy++;
        else if (s[i + 2] == '(') sad++;
      }
    }

    if (happy == 0 && sad == 0) Console.WriteLine("none");
    else if (happy > sad) Console.WriteLine("happy");
    else if (happy < sad) Console.WriteLine("sad");
    else Console.WriteLine("unsure");
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

  string s; getline(cin, s);

  int happy = 0, sad = 0;
  for (size_t i = 0; i + 2 < s.size(); i++) {
    if (s[i] == ':' && s[i + 1] == '-') {
      if (s[i + 2] == ')') happy++;
      else if (s[i + 2] == '(') sad++;
    }
  }

  if (happy == 0 && sad == 0) cout << "none\n";
  else if (happy > sad) cout << "happy\n";
  else if (happy < sad) cout << "sad\n";
  else cout << "unsure\n";

  return 0;
}
```
