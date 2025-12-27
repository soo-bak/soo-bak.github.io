---
layout: single
title: "[백준 28454] Gift Expire Date (C#, C++) - soo:bak"
date: "2023-08-19 11:09:00 +0900"
description: 문자열, 날짜 계산, 구현 등을 주제로 하는 백준 28454번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 28454
  - C#
  - C++
  - 알고리즘
keywords: "백준 28454, 백준 28454번, BOJ 28454, GiftExpireDate, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [28454번 - Gift Expire Date](https://www.acmicpc.net/problem/28454)

## 설명
문제의 목표는 주어지는 현재 날짜와 각 기프티콘의 유효기간을 비교하여, 유효한 기프티콘의 수를 세는 것입니다. <br>
<br>
문자열로부터 숫자를 파싱하고, 날짜로 변환하여 계산하는 부분이 조금 번거로울 뿐,<br>
<br>
차근 차근 변환 후 날짜를 비교해보면 되는 쉬운 구현 문제입니다. <br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    public struct Date {
      int Year { get; set; }
      int Month { get; set; }
      int Day { get; set; }

      public static Date ParseDate(string s) {
        return new Date {
          Year = int.Parse(s.Substring(0, 4)),
          Month = int.Parse(s.Substring(5, 2)),
          Day = int.Parse(s.Substring(8, 2))
        };
      }

      public bool IsAfterOrEqual(Date other) {
        if (Year != other.Year) return Year > other.Year;
        if (Month != other.Month) return Month > other.Month;
        return Day >= other.Day;
      }
    };

    static void Main(string[] args) {

      var currentDateStr = Console.ReadLine()!;
      Date currentDate = Date.ParseDate(currentDateStr);

      var n = int.Parse(Console.ReadLine()!);

      int validCount = 0;
      for (int i = 0; i < n; i++) {
        var giftDateStr = Console.ReadLine()!;
        Date giftDate = Date.ParseDate(giftDateStr);

        if (giftDate.IsAfterOrEqual(currentDate))
          validCount++;
      }

      Console.WriteLine(validCount);

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

struct Date {
  int year;
  int month;
  int day;

  static Date parseDate(const string& s) {
    return {
      stoi(s.substr(0, 4)),
      stoi(s.substr(5, 2)),
      stoi(s.substr(8, 2))
    };
  }

  bool isAfterOrEqual(const Date& other) const {
    if (year != other.year) return year > other.year;
    if (month != other.month) return month > other.month;
    return day >= other.day;
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string currentDateStr;
  cin >> currentDateStr;

  Date currentDate = Date::parseDate(currentDateStr);

  int n; cin >> n;

  int validCount = 0;
  while (n--) {
    string giftDateStr; cin >> giftDateStr;

    Date giftDate = Date::parseDate(giftDateStr);

    if (giftDate.isAfterOrEqual(currentDate))
      validCount++;
  }

  cout << validCount << "\n";

  return 0;
}
  ```
