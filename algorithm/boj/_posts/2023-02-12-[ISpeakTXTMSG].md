---
layout: single
title: "[백준 6841] I Speak TXTMSG (C#, C++) - soo:bak"
date: "2023-02-12 08:31:00 +0900"
description: 문자열 파싱을 주제로한 백준 6841번 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [6841번 - I Speak TXTMSG](https://www.acmicpc.net/problem/6841)

## 설명
  간단한 문자열 파싱과 구현 문제입니다.<br>

  입력되는 문자열들을 문제에서 주어진 조건에 맞추어 변환한 후 출력합니다.<br>

  주의해야 할 점은... <br>
  문제 본문의 표에서 Translation 문장들을 복사하여 풀이하면 `틀렸습니다.` 가 나옵니다. <br>

  그 이유는 `I'm happy`, `you're welcom` 등의 문자열에서 `'` 기호가 아닌, <br>
  특수문자 `’` 를 사용해야 하기 때문입니다...<br>

  `'` 가 아닌 `’` 특수문자는 문제 링크의 `예제 출력` 항목 혹은 `아래 코드` 에서 복사하실 수 있습니다. <br>
  ㅜㅜ...
  <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static string[] shortForm = {"CU", ":-)", ":-(", ";-)", ":-P", "(~.~)", "TA",
                                 "CCC", "CUZ", "TY", "YW", "TTYL"};
    static string[] translation = {"see you", "I’m happy", "I’m unhappy", "wink",
                                   "stick out my tongue", "sleepy", "totally awesome",
                                   "Canadian Computing Competition", "because", "thank-you",
                                   "you’re welcome", "talk to you later"};

    static string Translate(string str) {
      for (int i = 0; i < shortForm.Length; i++) {
        if (str == shortForm[i]) return translation[i];
      }
      return str;
    }

    static void Main(string[] args) {

      while (true) {
        string? input = Console.ReadLine();
        Console.WriteLine(Translate(input!));
        if (input == "TTYL") break ;
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

const string shortFrom[12] = {"CU", ":-)", ":-(", ";-)", ":-P", "(~.~)", "TA",
                              "CCC", "CUZ", "TY", "YW", "TTYL"};
const string translation[12] = {"see you", "I’m happy", "I’m unhappy", "wink",
                                "stick out my tongue", "sleepy", "totally awesome",
                                "Canadian Computing Competition", "because", "thank-you",
                                "you’re welcome", "talk to you later"};

string translate(const string& str) {
  for (int i = 0; i < 12; i++) {
    if (str == shortFrom[i])
      return translation[i];
  }
  return str;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  while (true){
    string input; cin >> input;
    cout << translate(input) << "\n";
    if (input == "TTYL") break ;
  }

  return 0;
}
  ```
