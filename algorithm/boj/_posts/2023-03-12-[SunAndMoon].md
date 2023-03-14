---
layout: single
title: "[백준 27590] Sun and Moon (C#, C++) - soo:bak"
date: "2023-03-12 13:54:00 +0900"
---

## 문제 링크
  [27590번 - Sun and Moon](https://www.acmicpc.net/problem/27590)

## 설명
  시뮬레이션과 구현을 주제로 하는 문제입니다. <br>

  문제의 목표는 `다음 일식이 일어날 연도` 를 구하는 것입니다.<br>

  문제의 조건에 따르면,<br>
  해와 달이 `특정한 위치` 에서 일직선으로 정렬되어야 일식을 관측할 수 있다고 합니다. <br>

  또한, 문제의 입력으로는 다음과 같은 정보들이 주어집니다.<br>
  1. `태양이 몇 년 전에 '특정한 위치' 에 있었는 지`
  2. `태양이 다시 그 위치로 돌아오는 데에 몇 년이 걸리는 지`
  3. `달이 몇 년 전에 '특정한 위치' 에 있었는 지`
  4. `달이 다시 그 위치로 돌아오는 데에 몇 년이 걸리는 지`

  <br>

  따라서, 태양과 달이 `특정한 위치` 에 돌아오는 연도를 모두 구한 후, <br>
  태양과 달이 `특정한 위치` 에 돌아오는 가장 빠른 '같은 연도' 를 구하면,<br>
  다음 일식이 일어날 연도를 알 수 있게 됩니다. <br>

  또한, 문제의 추가 조건에 `5000 년` 안에는 무조건 일식이 일어난다는 가정이 있습니다.<br>

  따라서 비교적 탐색할 범위가 작기 때문에,<br>
  태양과 달이 `특정한 위치` 에 돌아오는 연도에 대해서는 단순히 완전 탐색을 이용하여 탐색을 진행했습니다.<br>

  <br>
  이어서 구해야 할 것은 다음과 같습니다.
  - 태양이 `특정한 위치` 에 돌아오는 연도들과, 달이 `특정한 위치` 에 돌아오는 연도들 중에서 `가장 빠르면서도 같은 연도`

  해당 값을 탐색하는 과정은 비교적 빠른 탐색이 가능하도록 `Hash-table` 을 사용하였습니다.<br>

  (`C++` 에서는 `unordered_set` 이 내부적으로 `Hash-table` 을 사용하며, `C#` 에서는 `HashSet` 이 내부적으로 `Hash-table` 을 사용합니다.)<br>

  물론, `이중 for 문` 을 이용하여 탐색을 진행할 수도 있지만, 이런 경우 최악의 경우에서 시간 복잡도가 `O(N^2)` 가 됩니다.

  하지만, `Hash-table` 을 사용하면 최악의 경우 `O(N)` 의 시간복잡도를,<br>
  평균적인 경우 `O(1)` 의 시간복잡도를 통해 탐색을 진행할 수 있게 됩니다.<br>

  최종적으로, 탐색을 완료한 `가장 빠르면서도 같은 연도` 를 출력 조건에 맞추어 출력하여 문제를 해결합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    public record YEARS(int lastCorrectPosYear, int backToCorrectPosYear);

    const int SUN = 0,
              MOON = 1;

    public static void Main() {

      var SunInput = Console.ReadLine()?.Split();
      var MoonInput = Console.ReadLine()?.Split();

      YEARS[] years = new YEARS[2] {
        new YEARS(int.Parse(SunInput![0]), int.Parse(SunInput![1])),
        new YEARS(int.Parse(MoonInput![0]), int.Parse(MoonInput![1]))
      };

      int nextSunEclipse = -years[SUN].lastCorrectPosYear + years[SUN].backToCorrectPosYear;
      int nextMoonEclipse = -years[MOON].lastCorrectPosYear + years[MOON].backToCorrectPosYear;

      List<int> sunEclipses = new List<int> {nextSunEclipse};
      List<int> moonEclipses = new List<int> {nextMoonEclipse};

      const int MAX_YEAR = 5000;
      while (true) {
          if (nextSunEclipse > MAX_YEAR && nextMoonEclipse > MAX_YEAR) break;

          if (nextSunEclipse <= MAX_YEAR) {
            nextSunEclipse += years[SUN].backToCorrectPosYear;
            sunEclipses.Add(nextSunEclipse);
          }

          if (nextMoonEclipse <= MAX_YEAR) {
            nextMoonEclipse += years[MOON].backToCorrectPosYear;
            moonEclipses.Add(nextMoonEclipse);
          }
      }

      HashSet<int> sunHashSet = new HashSet<int>(sunEclipses);

      foreach (int element in moonEclipses) {
        if (sunHashSet.Contains(element)) {
          Console.WriteLine(element);
          break;
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

constexpr int SUN = 0;
constexpr int MOON = 1;

struct YEARS {
  int lsatCorrectPosYear,
      backToCorrectPosYear;
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  YEARS years[2];

  cin >> years[SUN].lsatCorrectPosYear >> years[SUN].backToCorrectPosYear;
  cin >> years[MOON].lsatCorrectPosYear >> years[MOON].backToCorrectPosYear;

  int nextSunEclipse = -years[SUN].lsatCorrectPosYear + years[SUN].backToCorrectPosYear,
      nextMoonEclipse = -years[MOON].lsatCorrectPosYear + years[MOON].backToCorrectPosYear;

  vector<int> sunEclipses, moonEclipses;
  sunEclipses.push_back(nextSunEclipse);
  moonEclipses.push_back(nextMoonEclipse);

  const int MAX_YEAR = 5000;
  while (true) {
    if (nextSunEclipse > MAX_YEAR && nextMoonEclipse > MAX_YEAR) break ;

    if (nextSunEclipse <= MAX_YEAR) {
      nextSunEclipse += years[SUN].backToCorrectPosYear;
      sunEclipses.push_back(nextSunEclipse);
    }

    if (nextMoonEclipse <= MAX_YEAR) {
      nextMoonEclipse += years[MOON].backToCorrectPosYear;
      moonEclipses.push_back(nextMoonEclipse);
    }
  }

  unordered_set<int> sunSet(sunEclipses.begin(), sunEclipses.end());

  for (auto& element : moonEclipses) {
    if (sunSet.find(element) != sunSet.end()) {
      cout << element << "\n";
      break ;
    }
  }

  return 0;
}
  ```
